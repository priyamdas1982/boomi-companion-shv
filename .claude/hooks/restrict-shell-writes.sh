#!/usr/bin/env bash
# PreToolUse hook (Bash). Wrapper for restrict-shell-writes.py, which allows a
# shell command only when every path it writes is inside the directories given
# as arguments. Fails closed: exit code 2 blocks the tool call.
if ! command -v python3 >/dev/null 2>&1; then
  echo "Blocked: python3 is not installed, so the command cannot be checked." >&2
  exit 2
fi
exec python3 "$(dirname "$0")/restrict-shell-writes.py" "$@"
