#!/usr/bin/env bash
# PreToolUse hook registered in .claude/settings.json for all tools.
# Hooks declared in agent frontmatter do not fire in every environment, so
# this one entry point applies each pipeline role's rules. Claude Code adds
# agent_type to the hook input when the call comes from a subagent; calls from
# the main conversation (no agent_type) and from other agents pass through.
# Exit code 2 blocks the tool call; stderr is shown to the agent.

input="$(cat)"
if ! command -v jq >/dev/null 2>&1; then
  echo "Blocked: jq is not installed, so the request cannot be checked." >&2
  exit 2
fi
role="$(printf '%s' "$input" | jq -r '.agent_type // empty')"
role="${role##*:}"   # tolerate a plugin-namespaced agent name
tool="$(printf '%s' "$input" | jq -r '.tool_name // empty')"
dir="$(dirname "$0")"

run() { printf '%s' "$input" | bash "$dir/$1" "${@:2}" || exit $?; }

case "$tool" in Write|Edit|MultiEdit|NotebookEdit) write=1 ;; *) write=0 ;; esac

case "$role" in
  designer)
    [ "$write" = 1 ] && run restrict-writes.sh "interfaces/*/design"
    ;;
  developer)
    [ "$write" = 1 ] && run restrict-writes.sh "interfaces/*/build" "active-development"
    [ "$tool" = Bash ] && run restrict-shell-writes.sh "interfaces/*/build" "active-development"
    ;;
  reviewer)
    [ "$write" = 1 ] && run restrict-writes.sh "interfaces/*/review"
    [ "$tool" = Bash ] && run block-boomi-mutations.sh
    [ "$tool" = Bash ] && run restrict-shell-writes.sh "interfaces/*/review"
    ;;
  tester)
    [ "$write" = 1 ] && run restrict-writes.sh "interfaces/*/test" "active-development"
    case "$tool" in Read|Grep|Glob|Bash) run deny-build-log.sh ;; esac
    [ "$tool" = Bash ] && run restrict-shell-writes.sh "interfaces/*/test" "active-development"
    ;;
esac
exit 0
