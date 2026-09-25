# PUB-GB-CG-043 Web to Lead Publisher: test cases

**Process:** `[Publisher]-[PUB-GB-CG-043]-[CreateLead]-[Customer Portal]-[GB-CG]` (`1b208fa6-9aa8-4014-b77d-51be59717e91`)
**API:** `[PUB-GB-CG-043] Leads API` (`bd886149-18b9-4900-9376-bb9c05b741b6`), `POST /ws/rest/gb-cg/leads`
**Folder:** `BC/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-leads`
**Test environment:** 1-DEV only (never production)

## Last run: 2026-09-25

| Area | Result |
|---|---|
| Static design checks (TC-10, TC-12) | **24/24 passed** (`static_checks.py`) |
| Deployment to 1-DEV (TC-11) | **Passed.** Process package `37309217-…`, API package `2dd04901-…` |
| HTTP tests (TC-01 to TC-09) | **Not run.** The DEV runtime host (`shv-energy-test.boomi.cloud`) is not reachable from the build container (HTTP 000). `SERVER_BASE_URL` in the environment is a placeholder and no listener credentials are set. |
| Runtime checks (TC-08, TC-12.3, TC-13) | **Not run.** They depend on the HTTP tests. |

## How to run

```bash
# Static checks: pulls the platform versions and checks them against the SHV rules
python3 tests/PUB-GB-CG-043/static_checks.py <skill-path>

# HTTP tests: needs SERVER_BASE_URL, SERVER_AUTH_TYPE and listener credentials for the DEV runtime
bash tests/PUB-GB-CG-043/run_http_tests.sh <skill-path>            # all cases
bash tests/PUB-GB-CG-043/run_http_tests.sh <skill-path> TC-01 TC-05 # selected cases
```

## Functional tests (HTTP, via the API Service Component)

| ID | Scenario | Input | Expected result | Status |
|---|---|---|---|---|
| TC-01 | Happy path | `tc01_valid_full.json`: the design doc sample with its JSON errors fixed | HTTP 200, empty body. Execution COMPLETE. One message on `gb-cg.q.leads.in.insert` with the payload unchanged and message key `testleadapitesting1@calor.co.uk` | Not run |
| TC-02 | Minimal payload | `tc02_minimal.json`: email and comment only | HTTP 200. Published unchanged; data validation is out of scope per the doc | Not run |
| TC-03 | Special characters | `tc03_special_chars.json`: accents, apostrophe, quotes, `&`, `<>`, `£`, `%` | HTTP 200. Kafka message byte-identical to the request (UTF-8 kept) | Not run |
| TC-04 | Multi-value arrays | `tc04_multi_value_arrays.json` | HTTP 200. Both array values kept in order | Not run |
| TC-05 | Unauthorised (doc exception 002) | TC-01 payload, no credentials | HTTP 401. No execution record | Not run |
| TC-06 | Wrong method | `GET /ws/rest/gb-cg/leads` | HTTP 404 (Boomi returns 404, not 405, for an unconfigured method). No execution | Not run |
| TC-07 | Unknown path | `POST /ws/rest/gb-cg/lead` | HTTP 404. No execution | Not run |
| TC-08 | Kafka failure (doc exception 003) | TC-01 payload with extension `DPP_KAFKA_TOPIC` set to a topic the principal cannot write to (or the broker list pointed at an unreachable host); reset afterwards | Try path attempted 4 times (1 + 3 retries). Catch path sets `DDP_MED_NS_Msg`, calls the CACHE Notification Facade, then the Exception step fails the execution. HTTP 500 whose message contains the email. Execution ERROR | Not run |
| TC-09 | Invalid JSON (doc exception 001) | `tc09_doc_sample_invalid_json.txt`: the doc's sample verbatim, with unquoted email and a missing comma | Record the actual behaviour. The listener takes a single JSON document but the process does no validation, so a 4xx rejection or a pass-through to Kafka are both possible. If it passes through, raise it with the design owner: validation is marked out of scope, but the subscriber will get unparseable JSON | Not run |

## Tracking and operational checks

| ID | Check | Expected | Status |
|---|---|---|---|
| TC-12.1 | WSS operation tracked fields | `primarykey` = `Email`, `primaryvalue` = `email` from the request profile | **Pass** (static) |
| TC-12.2 | Kafka operation tracked fields | Same as TC-12.1 | **Pass** (static) |
| TC-12.3 | Process Reporting after TC-01 | Document shows primarykey `Email`, primaryvalue `testleadapitesting1@calor.co.uk`. This also confirms tracked-field IDs 33185/33186 are this account's | Not run |
| TC-13 | Concurrency | 5 parallel TC-01 calls all return 200 (bridge mode, simultaneous executions allowed) | Not run |
| TC-11 | Deployment | Process and API both deployed to 1-DEV; only this API uses base path `gb-cg` | **Pass** |

## Static design checks (`static_checks.py`, 24/24 passed)

TC-10.1 to TC-10.22 check the pushed components against CLAUDE.md and the design doc:
- the naming convention and agreed folder
- one Try/Catch (at most three allowed) with 3 retries
- no Notify shapes and no scripts
- bridge mode, with simultaneous executions allowed
- WSS Listen start
- Kafka PRODUCE on `[Confluent_NL-HQ_Kafka]`, topic taken from extensible `DPP_KAFKA_TOPIC`, message key = email
- `DDP_MED_NS_Msg` set to the Try/Catch message before calling the framework 4.0 CACHE Notification Facade
- catch path ends in an Exception step
- all 9 Kafka connection fields externalised with xpath bindings
- the request profile holds all 10 doc fields
- the API routes POST `/gb-cg/leads` to the process

## Notes for testers

- **TC-01 to TC-04 publish real messages to the DEV Kafka topic.** Every payload says "Testing Lead, please ignore". If a DEV instance of SUB-GB-CG-043 is running, it may create test leads in the Salesforce sandbox.
- **Check the Kafka extension works.** The connection overrides use the `GenericConnectionConfig/field[@id='…']/@value` xpath. No platform-generated Kafka example exists in the account, so run TC-08 once with an extension value changed. That proves overrides are honoured, not silently ignored.
