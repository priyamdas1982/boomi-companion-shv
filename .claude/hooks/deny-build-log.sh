#!/usr/bin/env bash
# PreToolUse hook (Read|Grep|Bash) for the tester.
# Test cases must come from the design spec and mapping, not from the
# developer's build log or fix responses, so the tester cannot open them.
# Exit code 2 blocks the tool call; stderr is shown to the agent.

input="$(cat)"
if ! command -v jq >/dev/null 2>&1; then
  echo "Blocked: jq is not installed, so the request cannot be checked." >&2
  exit 2
fi
target="$(printf '%s' "$input" | jq -r '[.tool_input.file_path, .tool_input.path, .tool_input.command, .tool_input.glob] | map(select(. != null)) | join(" ")')"

if printf '%s' "$target" | grep -Eq '(build-log|fix-response)\.md'; then
  echo "Blocked: the tester derives tests from design/ only and may not read build/build-log.md or build/fix-response.md." >&2
  exit 2
fi
# A search rooted at a build/ folder would also return the build log.
if printf '%s' "$target" | grep -Eq 'interfaces/[^/[:space:]]+/build/?([[:space:]]|$)'; then
  echo "Blocked: search a specific file under build/components/ instead of the whole build/ folder." >&2
  exit 2
fi
exit 0
