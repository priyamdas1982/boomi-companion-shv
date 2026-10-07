#!/usr/bin/env bash
# PreToolUse hook (Write|Edit|NotebookEdit).
# Allows a write only when the target path is inside one of the directories
# given as arguments, relative to the project root. In an argument, '*' matches
# exactly one path segment, so 'interfaces/*/review' means
# interfaces/<ID>/review/ for any <ID>. interfaces/_template/ is never writable.
# Exit code 2 blocks the tool call; stderr is shown to the agent.

input="$(cat)"
if ! command -v jq >/dev/null 2>&1; then
  echo "Blocked: jq is not installed, so the write target cannot be checked." >&2
  exit 2
fi
path="$(printf '%s' "$input" | jq -r '.tool_input.file_path // .tool_input.notebook_path // empty')"
[ -z "$path" ] && { echo "Blocked: no file path in tool input." >&2; exit 2; }

root="${CLAUDE_PROJECT_DIR:-$(pwd)}"
root="$(realpath -m "$root")"
case "$path" in /*) ;; *) path="$root/$path" ;; esac
abs="$(realpath -m "$path")"
rel="${abs#"$root"/}"

if [ "$rel" = "$abs" ]; then
  echo "Blocked: $abs is outside the project." >&2; exit 2
fi
case "$rel" in interfaces/_template/*)
  echo "Blocked: interfaces/_template/ is read-only for pipeline roles." >&2; exit 2 ;;
esac

for allowed in "$@"; do
  re="^$(printf '%s' "${allowed%/}" | sed -e 's/[.[\^$+?(){}|]/\\&/g' -e 's/\*/[^\/]+/g')/.+"
  printf '%s' "$rel" | grep -Eq "$re" && exit 0
done

echo "Blocked: this role may only write inside: $*. Target was: $rel" >&2
exit 2
