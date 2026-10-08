#!/usr/bin/env python3
"""PreToolUse hook (Bash): the shell counterpart of restrict-writes.sh.

Finds every path a command would write, create, move or delete and allows the
command only when each one is inside one of the directories given as arguments
(relative to the project root; '*' matches one path segment, as in
restrict-writes.sh). interfaces/_template/ is never writable. /tmp and /dev/null
style devices are always allowed. Anything the check cannot verify (a target
built from a variable, writes through xargs or find -exec, inline interpreter
code that writes files, running a script stored in the project, git commands
that change the working tree) is blocked, so the role uses the Write and Edit
tools instead. Exit code 2 blocks the tool call; stderr is shown to the agent.
"""
import json
import os
import re
import shlex
import sys

OPERATORS = re.compile(r">>|>&|>\||&>>|&>|<<<|<<-|<<|<>|<&|&&|\|\||;;|[;&|()<>{}]")
SEPARATORS = {";", ";;", "&", "&&", "||", "|", "(", ")", "{", "}"}
REDIRECTS = {">", ">>", ">&", ">|", "&>", "&>>", "<>"}
SAFE_PATHS = {"/dev/null", "/dev/stdout", "/dev/stderr", "/dev/tty"}
PREFIX_WORDS = {"if", "then", "else", "elif", "do", "while", "until", "!", "time",
                "nohup", "command", "builtin", "exec", "sudo", "doas", "stdbuf", "nice"}
SHELLS = {"bash", "sh", "zsh", "dash", "ksh"}
INTERPRETERS = {"python", "python3", "node", "perl", "ruby", "php", "deno", "bun"}
INLINE_FLAGS = {"-c", "-e", "-E", "-r", "--eval", "-p"}
INLINE_WRITES = re.compile(
    r"open\s*\(|write|unlink|remove|os\.replace|rename|rmtree|shutil|mkdir|makedirs|"
    r"truncate|chmod|chown|symlink|copy|move|touch|system|popen|subprocess|exec|spawn|fs\.")
READONLY_GIT = {"status", "log", "diff", "show", "ls-files", "ls-tree", "blame", "rev-parse",
                "grep", "cat-file", "describe", "shortlog", "remote", "config"}
EDITORS = {"vi", "vim", "nvim", "nano", "emacs", "ed", "ex", "patch", "yq"}


class Checker:
    def __init__(self, root, allowed):
        self.root = root
        self.allowed = [a.rstrip("/") for a in allowed]
        self.problems = []

    def block(self, why):
        if why not in self.problems:
            self.problems.append(why)

    # ---- paths ----------------------------------------------------------
    def target(self, path, cwd, dir_ok=False):
        """Check one path the command writes. dir_ok lets it equal an allowed dir."""
        shown = path
        path = re.sub(r"\$\{?CLAUDE_PROJECT_DIR\}?", self.root, path)
        if path.startswith("~"):
            path = os.path.expanduser(path)
        if re.search(r"[$`{}?\[\]]|__SUBST__", path):
            return self.block(f"cannot verify the write target '{shown}'")
        if path in SAFE_PATHS or path.startswith("/dev/fd/"):
            return
        if not os.path.isabs(path):
            if cwd is None:
                return self.block(f"cannot verify '{shown}' after a cd the hook cannot follow")
            path = os.path.join(cwd, path)
        real = os.path.realpath(path)
        if real == "/tmp" or real.startswith("/tmp/"):
            return
        rel = os.path.relpath(real, self.root)
        if rel == ".." or rel.startswith("../"):
            return self.block(f"'{shown}' is outside the project")
        if rel.startswith("interfaces/_template/") or rel == "interfaces/_template":
            return self.block("interfaces/_template/ is read-only for pipeline roles")
        for a in self.allowed:
            pat = re.escape(a).replace(r"\*", "[^/]+")
            if re.fullmatch(pat + ("(/.+)?" if dir_ok else "/.+"), rel):
                return
        self.block(f"'{rel}' is outside {' '.join(self.allowed)}")

    def in_project(self, path, cwd):
        base = cwd or self.root
        real = os.path.realpath(os.path.join(base, path))
        return not os.path.relpath(real, self.root).startswith("..")

    # ---- text -----------------------------------------------------------
    def check(self, text, cwd):
        text = text.replace("\\\n", "")
        text = self.strip_heredocs(text)
        text = self.substitutions(text)
        try:
            lex = shlex.shlex(text.replace("\n", " ; "), posix=True, punctuation_chars=True)
            lex.whitespace_split = True
            raw = list(lex)
        except ValueError as e:
            return self.block(f"could not parse the command ({e})")
        tokens = []
        for t in raw:
            tokens.extend(OPERATORS.findall(t) if t and set(t) <= set(";&|()<>{}") else [t])
        self.walk(tokens, cwd)

    def strip_heredocs(self, text):
        out, lines, i = [], text.split("\n"), 0
        while i < len(lines):
            line = lines[i]
            out.append(line)
            i += 1
            for strip, quote, word in re.findall(r"(?<!<)<<(-?)\s*(['\"]?)(\w+)\2", line):
                body = []
                while i < len(lines) and (lines[i].strip() if strip else lines[i]) != word:
                    body.append(lines[i])
                    i += 1
                i += 1
                if not quote:  # unquoted heredocs still run $(...) and `...`
                    for m in re.finditer(r"\$\(|`", "\n".join(body)):
                        self.block("command substitution inside a heredoc")
                        break
        return "\n".join(out)

    def substitutions(self, text):
        """Check $(...), `...`, <(...) and >(...) recursively; replace them."""
        out, i, n, quote = [], 0, len(text), None
        while i < n:
            c = text[i]
            if quote == "'":
                out.append(c)
                quote = None if c == "'" else quote
                i += 1
                continue
            if c == "\\" and i + 1 < n:
                out.append(text[i:i + 2])
                i += 2
                continue
            if c == '"':
                quote = None if quote == '"' else '"'
            elif c == "'" and quote is None:
                quote = "'"
            elif c == "#" and quote is None and (i == 0 or text[i - 1] in " \t\n;&|("):
                while i < n and text[i] != "\n":
                    i += 1
                continue
            elif c == ">" and quote is None:
                k = len(out)
                while k and out[k - 1].isdigit():
                    k -= 1
                if k < len(out) and (k == 0 or out[k - 1] in " \t\n;&|("):
                    del out[k:]  # drop the fd number in 2>file
            if text.startswith("$(", i) or (quote is None and c in "<>" and text.startswith("(", i + 1)):
                end = self.match_paren(text, i + 2)
                if end is None:
                    self.block("unbalanced $( or <( in the command")
                    return ""
                self.check(text[i + 2:end], None)
                out.append("__SUBST__" if c == "$" else "/dev/fd/63")
                i = end + 1
                continue
            if c == "`":
                end = text.find("`", i + 1)
                if end < 0:
                    self.block("unbalanced backtick in the command")
                    return ""
                self.check(text[i + 1:end], None)
                out.append("__SUBST__")
                i = end + 1
                continue
            out.append(c)
            i += 1
        return "".join(out)

    @staticmethod
    def match_paren(text, i):
        depth, quote = 1, None
        while i < len(text):
            c = text[i]
            if quote:
                quote = None if c == quote else quote
            elif c in "'\"":
                quote = c
            elif c == "\\":
                i += 1
            elif c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0:
                    return i
            i += 1
        return None

    # ---- commands -------------------------------------------------------
    def walk(self, tokens, cwd):
        stack, seg, prev_sep = [], [], None
        has_or = "||" in tokens
        for tok in tokens + [";"]:
            if tok in SEPARATORS:
                cwd = self.segment(seg, cwd, piped=(prev_sep == "|" or tok == "|"), has_or=has_or)
                seg = []
                if tok in ("(", "{"):
                    stack.append(cwd)
                elif tok in (")", "}") and stack:
                    cwd = stack.pop() if tok == ")" else cwd
                prev_sep = tok
            else:
                seg.append(tok)

    def segment(self, seg, cwd, piped=False, has_or=False):
        words, i = [], 0
        while i < len(seg):
            if seg[i] in REDIRECTS and i + 1 < len(seg):
                op, tgt = seg[i], seg[i + 1]
                if not (op == ">&" and re.fullmatch(r"\d+|-", tgt)):
                    self.target(tgt, cwd)
                i += 2
            elif seg[i] in ("<", "<<", "<<-", "<<<", "<&") and i + 1 < len(seg):
                i += 2
            else:
                words.append(seg[i])
                i += 1
        return self.command(words, cwd, piped, has_or)

    def command(self, w, cwd, piped=False, has_or=False, from_stdin=False):
        # skip assignments and wrapper words
        while w and (re.match(r"^[A-Za-z_]\w*=", w[0]) or w[0] in PREFIX_WORDS):
            w = w[1:]
            while w and w[0].startswith("-") and len(w) > 1:  # wrapper flags (sudo -u x etc.)
                w = w[1:]
        if w and w[0] in ("env", "timeout"):
            if any(x in ("-C", "--chdir") for x in w):
                cwd = None
            w = w[1:]
            while w and (w[0].startswith("-") or re.match(r"^[A-Za-z_]\w*=|^\d", w[0])):
                w = w[1:]
        if not w:
            return cwd
        name, args = os.path.basename(w[0]), w[1:]
        pos = [a for a in args if not a.startswith("-") or a == "-"]

        if re.search(r"[$`]|__SUBST__", w[0]):
            self.block("the command name is built at run time")
        elif name in ("cd", "pushd"):
            if piped or has_or or not pos or pos[0] == "-":
                return None
            if re.search(r"[$`{}?\[\]*]|__SUBST__", pos[0]):
                return None
            base = cwd if cwd is not None else None
            if base is None and not os.path.isabs(pos[0]):
                return None
            return os.path.realpath(os.path.join(base or "/", os.path.expanduser(pos[0])))
        elif name == "popd":
            return None
        elif from_stdin and name in WRITERS:
            self.block(f"'{name}' gets its paths from xargs or find, which the hook cannot see")
        elif name in ("xargs", "parallel"):
            rest = [a for a in args if not a.startswith("-")]
            self.command(rest, cwd, from_stdin=True)
        elif name == "find":
            self.find(args, cwd)
        elif name in ("eval",):
            self.check(" ".join(args), cwd)
        elif name in SHELLS:
            if "-c" in args and args.index("-c") + 1 < len(args):
                self.check(args[args.index("-c") + 1], cwd)
            elif pos:
                self.script(pos[0], args, cwd)
        elif name in ("source", "."):
            if pos and self.in_project(pos[0], cwd):
                self.block("running a script stored in the project")
        elif re.match(r"^(python|python3(\.\d+)?|node|perl|ruby|php|deno|bun)$", name):
            self.interpreter(name, args, cwd)
        elif "/" in w[0] and self.in_project(w[0], cwd):
            self.block("running a script stored in the project")
        elif name in WRITERS:
            WRITERS[name](self, args, pos, cwd)
        elif name == "git":
            self.git(args)
        elif name in EDITORS:
            self.block(f"'{name}' edits files; use the Edit tool")
        return cwd

    def script(self, path, args, cwd):
        if self.in_project(path, cwd):
            return self.block("running a script stored in the project")
        if re.search(r"boomi-[\w-]+\.sh$", path) and "--target-path" in args:
            i = args.index("--target-path")
            if i + 1 < len(args):
                self.target(args[i + 1], cwd, dir_ok=True)

    def interpreter(self, name, args, cwd):
        for i, a in enumerate(args):
            if a in INLINE_FLAGS and i + 1 < len(args):
                if INLINE_WRITES.search(args[i + 1]):
                    self.block(f"inline {name} code that may write files; use the Write or Edit tool")
                if name == "perl" and any(re.fullmatch(r"-\w*i\S*", x) for x in args):
                    self.block("perl -i edits files in place; use the Edit tool")
                return
            if not a.startswith("-"):
                if self.in_project(a, cwd):
                    return self.block("running a script stored in the project")
                if a.endswith("boomi-profile-inspect.py") and i + 1 < len(args):
                    self.target(os.path.join(os.path.dirname(args[i + 1]) or ".", "distilled.json"), cwd)
                return

    def find(self, args, cwd):
        for i, a in enumerate(args):
            if a == "-delete":
                self.block("find -delete")
            elif a in ("-exec", "-execdir", "-ok", "-okdir"):
                self.command(args[i + 1:], cwd, from_stdin=True)
            elif a in ("-fprint", "-fprint0", "-fprintf", "-fls") and i + 1 < len(args):
                self.target(args[i + 1], cwd)

    def git(self, args):
        i = 0
        while i < len(args) and args[i].startswith("-"):
            i += 2 if args[i] in ("-C", "-c") else 1
        if i < len(args) and args[i] not in READONLY_GIT:
            self.block(f"'git {args[i]}' can change files; pipeline roles use read-only git only")


def _value(args, flags):
    """Values of options such as -t DIR, --target-directory=DIR."""
    vals = []
    for i, a in enumerate(args):
        for f in flags:
            if a == f and i + 1 < len(args):
                vals.append(args[i + 1])
            elif f.startswith("--") and a.startswith(f + "="):
                vals.append(a.split("=", 1)[1])
    return vals


def _positional(args, valued=()):
    out, skip = [], False
    for a in args:
        if skip:
            skip = False
        elif a in valued:
            skip = True
        elif not a.startswith("-") or a == "-":
            out.append(a)
    return out


def w_all(dir_ok=False, valued=(), skip_first=False):
    def f(c, args, pos, cwd):
        p = _positional(args, valued)
        for t in (p[1:] if skip_first else p):
            c.target(t, cwd, dir_ok)
    return f


def w_copy(move=False):
    def f(c, args, pos, cwd):
        dests = _value(args, ("-t", "--target-directory"))
        p = _positional(args, ("-t", "-S", "--suffix", "-m", "-o", "-g"))
        if "-d" in args and not move and not dests:  # install -d DIRS
            return [c.target(t, cwd, True) for t in p]
        if dests:
            srcs = p
        else:
            dests, srcs = p[-1:], p[:-1]
        for d in dests:
            c.target(d, cwd, dir_ok=True)
        if move:
            for s in srcs:
                c.target(s, cwd)
    return f


def w_sed(c, args, pos, cwd):
    if not any(a.startswith("--in-place") or re.fullmatch(r"-[a-zA-Z]*i\S*", a) for a in args):
        return
    has_script = any(a in ("-e", "-f", "--expression", "--file") or a.startswith(("--expression=", "--file="))
                     for a in args)
    p = _positional(args, ("-e", "-f", "--expression", "--file", "-l"))
    for t in (p if has_script else p[1:]):
        c.target(t, cwd)


def w_awk(c, args, pos, cwd):
    if "inplace" in args:
        c.block("awk -i inplace edits files; use the Edit tool")
    progs = [] if "-f" in args else _positional(args, ("-F", "-v"))[:1]
    for prog in progs:
        if re.search(r"system\s*\(|\|\s*getline|printf?[^;}\n]*(>|\|)", prog):
            c.block("awk program that writes files or runs commands")


def w_dd(c, args, pos, cwd):
    for a in args:
        if a.startswith("of="):
            c.target(a[3:], cwd)


def w_curl(c, args, pos, cwd):
    for t in _value(args, ("-o", "--output", "-D", "--dump-header", "-c", "--cookie-jar",
                           "--trace", "--trace-ascii", "--output-dir")):
        c.target(t, cwd, dir_ok=True)
    if any(a in ("-O", "--remote-name", "--remote-name-all") or re.fullmatch(r"-[a-zA-Z]*O", a) for a in args):
        c.target(".", cwd, dir_ok=True)


def w_wget(c, args, pos, cwd):
    outs = _value(args, ("-O", "--output-document", "-o", "--output-file", "-a", "--append-output"))
    for t in outs:
        if t != "-":
            c.target(t, cwd)
    if not any(a in ("-O", "--output-document") for a in args) and "--spider" not in args:
        for d in _value(args, ("-P", "--directory-prefix")) or ["."]:
            c.target(d, cwd, dir_ok=True)


def w_tar(c, args, pos, cwd):
    flags = "".join(a.lstrip("-") for a in args[:1] if not a.startswith("--")) + \
            "".join(a[1:] for a in args if re.fullmatch(r"-[a-zA-Z]+", a))
    long = set(args)
    if "x" in flags or long & {"--extract", "--get"}:
        for d in _value(args, ("-C", "--directory")) or ["."]:
            c.target(d, cwd, dir_ok=True)
    if re.search("[cruA]", flags) or long & {"--create", "--append", "--update"}:
        files = _value(args, ("-f", "--file"))
        if not files and "f" in flags:
            p = _positional(args)
            files = p[1:2] if args and not args[0].startswith("-") else p[:1]
        for f in files:
            if f != "-":
                c.target(f, cwd)


def w_unzip(c, args, pos, cwd):
    if any(a in ("-l", "-t", "-p", "-Z") for a in args):
        return
    for d in _value(args, ("-d",)) or ["."]:
        c.target(d, cwd, dir_ok=True)


def w_compress(c, args, pos, cwd):
    if any(a in ("-c", "--stdout", "-l", "--list", "-t", "--test") or re.fullmatch(r"-[a-zA-Z]*c[a-zA-Z]*", a)
           for a in args):
        return
    for t in _positional(args, ("-S", "--suffix")):
        c.target(t, cwd)


WRITERS = {
    "rm": w_all(), "rmdir": w_all(), "unlink": w_all(), "shred": w_all(),
    "truncate": w_all(valued=("-s", "--size", "-r", "--reference")),
    "chmod": w_all(skip_first=True), "chown": w_all(skip_first=True), "chgrp": w_all(skip_first=True),
    "touch": w_all(dir_ok=True, valued=("-d", "-r", "-t")),
    "mkdir": w_all(dir_ok=True, valued=("-m", "--mode")),
    "tee": w_all(), "sponge": w_all(), "mkfifo": w_all(), "split": w_all(skip_first=True),
    "cp": w_copy(), "ln": w_copy(), "install": w_copy(), "rsync": w_copy(), "scp": w_copy(),
    "mv": w_copy(move=True),
    "sed": w_sed, "gsed": w_sed,
    "awk": w_awk, "gawk": w_awk, "mawk": w_awk, "nawk": w_awk,
    "dd": w_dd, "curl": w_curl, "wget": w_wget, "tar": w_tar, "unzip": w_unzip,
    "gzip": w_compress, "gunzip": w_compress, "bzip2": w_compress, "xz": w_compress, "zstd": w_compress,
}


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        print("Blocked: the hook input is not valid JSON.", file=sys.stderr)
        return 2
    cmd = (data.get("tool_input") or {}).get("command") or ""
    root = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    cwd = os.path.realpath(data.get("cwd") or root)
    checker = Checker(root, sys.argv[1:])
    checker.check(cmd, cwd)
    if checker.problems:
        print("Blocked: this role may only change files inside: " + " ".join(sys.argv[1:]) +
              " (and /tmp). Use the Write or Edit tool for files. Problems: " +
              "; ".join(checker.problems), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
