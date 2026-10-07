#!/usr/bin/env bash
# Feeds simulated PreToolUse input to role-dispatch.sh and checks each verdict.
# Usage: bash .claude/hooks/tests/run-hook-tests.sh   (from anywhere)
# Exit code is the number of failed cases.

hooks="$(cd "$(dirname "$0")/.." && pwd)"
export CLAUDE_PROJECT_DIR="$(cd "$hooks/../.." && pwd)"
S=/root/.claude/skills/boomi-integration/scripts
fail=0 pass=0

# expect <allow|block> <role> <tool> <tool_input json>
expect() {
  local want="$1" role="$2" tool="$3" ti="$4" got err
  err="$(jq -nc --arg r "$role" --arg t "$tool" --argjson ti "$ti" --arg cwd "$CLAUDE_PROJECT_DIR" \
          '{agent_type: (if $r == "" then null else $r end), tool_name: $t, tool_input: $ti, cwd: $cwd}' \
        | bash "$hooks/role-dispatch.sh" 2>&1 >/dev/null)"
  case $? in 0) got=allow ;; 2) got=block ;; *) got="error($?)" ;; esac
  if [ "$got" = "$want" ]; then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
    printf 'FAIL  %-9s %-5s want=%-5s got=%-5s %s\n      %s\n' "${role:-main}" "$tool" "$want" "$got" "$ti" "$err"
  fi
}
w() { jq -nc --arg p "$1" '{file_path: $p}'; }
b() { jq -nc --arg c "$1" '{command: $c}'; }

# main conversation and unknown agents are never restricted
expect allow ""        Write "$(w CLAUDE.md)"
expect allow ""        Bash  "$(b "rm -rf interfaces/X")"
expect allow Explore   Write "$(w CLAUDE.md)"

# Write/Edit path rules
expect allow designer  Write "$(w interfaces/A/design/spec.md)"
expect block designer  Write "$(w interfaces/A/build/x.xml)"
expect block designer  Edit  "$(w interfaces/_template/design/spec.md)"
expect block designer  Write "$(w interfaces/A/design/../../../CLAUDE.md)"
expect allow developer Write "$(w active-development/process/p.xml)"
expect block developer Write "$(w interfaces/A/review/findings.md)"
expect allow reviewer  Write "$(w interfaces/A/review/findings.md)"
expect block reviewer  Write "$(w interfaces/A/build/probe.md)"
expect allow tester    Write "$(w interfaces/A/test/cases.md)"
expect block tester    Edit  "$(w interfaces/A/design/spec.md)"

# reviewer: no Boomi mutations
expect allow reviewer  Bash  "$(b "bash $S/boomi-component-pull.sh --component-id x")"
expect block reviewer  Bash  "$(b "echo boomi-deploy.sh")"
expect block reviewer  Bash  "$(b "bash $S/boomi-extensions.sh set --file a.json")"
expect block reviewer  Bash  "$(b "curl https://api.boomi.com")"

# tester: no build log
expect allow tester    Read  "$(w interfaces/A/build/components/p.xml)"
expect block tester    Read  "$(w interfaces/A/build/build-log.md)"
expect block tester    Grep  '{"pattern":"x","path":"interfaces/A/build"}'
expect block tester    Bash  "$(b "cat interfaces/A/build/fix-response.md")"

# shell writes: allowed
expect allow reviewer  Bash  "$(b "ls -la interfaces; cat interfaces/A/design/spec.md | grep -n x")"
expect allow reviewer  Bash  "$(b "jq '.a > 3' f.json 2>/dev/null")"
expect allow reviewer  Bash  "$(b "echo 'a > b' > interfaces/A/review/notes.md")"
expect allow reviewer  Bash  "$(b "grep -c x f > /tmp/out.txt 2>&1")"
expect allow reviewer  Bash  "$(b "git diff --stat && git log -3")"
expect allow developer Bash  "$(b "mkdir -p active-development/process && cp a.xml interfaces/A/build/components/")"
expect allow developer Bash  "$(b "mkdir -p interfaces/A/build")"
expect allow developer Bash  "$(b "bash $S/boomi-component-pull.sh --component-id x --target-path interfaces/A/build/components")"
expect allow developer Bash  "$(b "cd interfaces/A/build && echo x > notes.txt")"
expect allow tester    Bash  "$(b "bash $S/boomi-test-execute.sh --process-id x > interfaces/A/test/run1.txt")"
expect allow developer Bash  "$(b "python3 -c 'import json,sys; print(json.load(sys.stdin)[\"id\"])' < a.json")"
expect allow developer Bash  "$(b "echo \$(date) >> active-development/log.txt")"

# shell writes: blocked
expect block reviewer  Bash  "$(b "echo x > CLAUDE.md")"
expect block reviewer  Bash  "$(b "echo x >> interfaces/A/build/probe.md")"
expect block reviewer  Bash  "$(b "echo x | tee interfaces/A/design/spec.md")"
expect block reviewer  Bash  "$(b "rm -rf active-development")"
expect block reviewer  Bash  "$(b "mv interfaces/A/build/x.xml interfaces/A/review/x.xml")"
expect block reviewer  Bash  "$(b "cp x.md interfaces/A/design/")"
expect block reviewer  Bash  "$(b "sed -i 's/a/b/' interfaces/A/design/spec.md")"
expect block reviewer  Bash  "$(b "touch interfaces/_template/x")"
expect block reviewer  Bash  "$(b "cd interfaces/A/review && echo x > ../../../CLAUDE.md")"
expect block reviewer  Bash  "$(b "cd \$HOME && echo x > f")"
expect block reviewer  Bash  "$(b "bash -c 'echo x > CLAUDE.md'")"
expect block reviewer  Bash  "$(b "x=\$(echo y > CLAUDE.md)")"
expect block reviewer  Bash  "$(b "echo x > \$F")"
expect block reviewer  Bash  "$(b "ls | xargs rm")"
expect block reviewer  Bash  "$(b "find . -name '*.xml' -delete")"
expect block reviewer  Bash  "$(b "find . -exec rm {} \\;")"
expect block reviewer  Bash  "$(b "python3 -c \"open('CLAUDE.md','w').write('x')\"")"
expect block reviewer  Bash  "$(b "git checkout -- CLAUDE.md")"
expect block reviewer  Bash  "$(b "dd if=/dev/zero of=CLAUDE.md count=1")"
expect block reviewer  Bash  "$(b "awk '{print > \"out.txt\"}' f")"
expect block reviewer  Bash  "$(b "bash interfaces/A/review/run.sh")"
expect block reviewer  Bash  "$(b "cat <<EOF > CLAUDE.md
hello
EOF")"
expect block developer Bash  "$(b "cp a.xml interfaces/A/review/")"
expect block developer Bash  "$(b "bash $S/boomi-component-pull.sh --component-id x --target-path interfaces/A/design")"
expect block tester    Bash  "$(b "echo x > interfaces/A/build/components/p.xml")"

echo "passed: $pass  failed: $fail"
exit "$fail"
