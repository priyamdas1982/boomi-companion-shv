#!/usr/bin/env bash
# PreToolUse hook (Bash) for read-only roles.
# Blocks every Boomi skill script, or subcommand, that changes the platform:
# create, update, deploy, undeploy, execute, or write extension values.
# Read-only scripts (pull, search, list, check, query, diff) are allowed.
# Exit code 2 blocks the tool call; stderr is shown to the agent.

input="$(cat)"
if ! command -v jq >/dev/null 2>&1; then
  echo "Blocked: jq is not installed, so the command cannot be checked." >&2
  exit 2
fi
cmd="$(printf '%s' "$input" | jq -r '.tool_input.command // empty')"
[ -z "$cmd" ] && exit 0

block() {
  echo "Blocked: '$1' changes the Boomi platform. This role is read-only." >&2
  exit 2
}

# Whole scripts that only mutate or execute.
for s in boomi-component-create boomi-component-push boomi-folder-create \
         boomi-deploy boomi-undeploy boomi-test-execute boomi-wss-test; do
  printf '%s' "$cmd" | grep -Eq "(^|[^[:alnum:]_-])${s}(\.sh)?([^[:alnum:]_-]|$)" && block "$s"
done

# Mixed scripts: block only the mutating subcommands.
printf '%s' "$cmd" | grep -Eq 'boomi-extensions(\.sh)?[[:space:]](.*[[:space:]])?set([[:space:]]|$)' \
  && block "boomi-extensions set"
printf '%s' "$cmd" | grep -Eq 'boomi-branch(\.sh)?[[:space:]]+(create|delete|merge|merge-execute|merge-revert|merge-delete)([[:space:]]|$)' \
  && block "boomi-branch (create/delete/merge)"
printf '%s' "$cmd" | grep -Eq 'event-streams-setup(\.sh)?[[:space:]]+(create-token|provision-connection|create-topic|create-subscription|rest-produce)([[:space:]]|$)' \
  && block "event-streams-setup (create/provision/produce)"

# No direct platform calls around the scripts.
printf '%s' "$cmd" | grep -Eq '(^|[^[:alnum:]_-])boomi-common(\.sh)?([^[:alnum:]_-]|$)' && block "boomi-common (raw API helper)"
printf '%s' "$cmd" | grep -Eq '(^|[^[:alnum:]_-])(curl|wget)([^[:alnum:]_-]|$)' && block "curl/wget"

exit 0
