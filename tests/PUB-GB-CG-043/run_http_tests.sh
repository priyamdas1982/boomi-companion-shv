#!/usr/bin/env bash
# HTTP test runner for PUB-GB-CG-043 (DEV only).
#
# Prerequisites
#   - Process and [PUB-GB-CG-043] Leads API deployed to 1-DEV (both are separate deployments)
#   - SERVER_BASE_URL = the DEV runtime's shared web server (e.g. https://shv-energy-test.boomi.cloud)
#   - SERVER_AUTH_TYPE + credentials for that listener port (see boomi-wss-test.sh)
#   - Outbound HTTPS to the SERVER_BASE_URL host allowed from where this runs
#
# Usage: bash tests/PUB-GB-CG-043/run_http_tests.sh <skill-path> [TC-01 TC-05 ...]
set -uo pipefail

SKILL="${1:-/root/.claude/skills/boomi-integration}"; shift || true
WSS="$SKILL/scripts/boomi-wss-test.sh"
DIR="$(cd "$(dirname "$0")" && pwd)/payloads"
ROUTE=/ws/rest/gb-cg/leads

# id | description | method | path | payload | auth override | expected HTTP
CASES=(
  "TC-01|Valid full payload (design doc sample, corrected)|POST|$ROUTE|tc01_valid_full.json||200"
  "TC-02|Minimal payload, email only|POST|$ROUTE|tc02_minimal.json||200"
  "TC-03|Special characters and unicode|POST|$ROUTE|tc03_special_chars.json||200"
  "TC-04|Multi-value lead-channel / lead-source arrays|POST|$ROUTE|tc04_multi_value_arrays.json||200"
  "TC-05|No credentials|POST|$ROUTE|tc01_valid_full.json|none|401"
  "TC-06|Wrong HTTP method (GET)|GET|$ROUTE|||404"
  "TC-07|Unknown path|POST|/ws/rest/gb-cg/lead|tc01_valid_full.json||404"
  "TC-09|Design doc sample verbatim (invalid JSON)|POST|$ROUTE|tc09_doc_sample_invalid_json.txt||4xx/5xx"
)

want=("$@"); pass=0; fail=0
for c in "${CASES[@]}"; do
  IFS='|' read -r id desc method path payload auth expect <<<"$c"
  if ((${#want[@]})) && [[ ! " ${want[*]} " =~ " $id " ]]; then continue; fi
  args=(--path "$path" --method "$method")
  [[ -n "$payload" ]] && args+=(--data "$DIR/$payload")
  if [[ -n "$auth" ]]; then out=$(SERVER_AUTH_TYPE="$auth" bash "$WSS" "${args[@]}" 2>&1)
  else out=$(bash "$WSS" "${args[@]}" 2>&1); fi
  code=$(grep -o 'HTTP [0-9]\{3\}' <<<"$out" | tail -1 | cut -d' ' -f2)
  case "$expect" in
    4xx/5xx) [[ "$code" =~ ^[45] ]] && ok=1 || ok=0 ;;
    *)       [[ "$code" == "$expect" ]] && ok=1 || ok=0 ;;
  esac
  ((ok)) && { echo "PASS  $id  $desc  (HTTP $code)"; ((pass++)); } \
         || { echo "FAIL  $id  $desc  (expected $expect, got HTTP ${code:-none})"; ((fail++)); }
done
echo; echo "$pass passed, $fail failed"
echo "Next: bash $SKILL/scripts/boomi-execution-query.sh --process-id 1b208fa6-9aa8-4014-b77d-51be59717e91"
echo "      then --execution-id <id> --logs, and check the gb-cg.q.leads.in.insert topic (see TEST_CASES.md)."
((fail == 0))
