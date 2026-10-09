# Build log: PUB-GB-CG-043

Spec hash built from: 1f1a888b24b66d11042d647eade405fa5d8e9ca362d9fdae83450a4ae00b0396 (verified 2026-10-08, matches pipeline-state.md; spec revision 3)

Status: BLOCKED in pre-build checks (round 0). No component was created, pushed or deployed.

## Components

| Name | Type | Component ID | Version | Folder | Pulled XML |
|------|------|--------------|---------|--------|------------|

None created. Read-only pull for verification (not edited, not copied to build/components because it was not created or changed):

| Name | Type | Component ID | Version | Folder | Local copy |
|------|------|--------------|---------|--------|------------|
| [MED] (sub) CACHE Notification Facade | process | 338df4f8-af86-44f9-855c-943d8d0d478f | 1 | SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/00-SharedLibrary_v4/00-Version_4.0 (2019-12-28-baseline)/01-Facade/02-Process | active-development/process/[MED] (sub) CACHE Notification Facade.xml |

## Pre-build checks (2026-10-08)

| Check | Result | Evidence |
|-------|--------|----------|
| Spec hash | PASS | Recomputed hash equals recorded hash |
| Platform connection | PASS | Authenticated to shvenergynv-6R344K |
| Environment classification | NOT CONFIRMED | BOOMI_ENVIRONMENT_ID = 693e8bc2-46f8-4c7f-8259-8dcf6cf0f264 ("1-DEV"). `boomi-deploy.sh --list-environments` returns names and IDs only, no classification; no skill CLI tool exposes it and custom curl is not allowed. Name alone not accepted as proof. |
| Interface folder (spec row 11) | FAIL | `Calor Group Limited/02-Deployable/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead` does not exist. Account root folder is `SHV Energy N.V.`; no folder named `Calor Group Limited` exists; `SHV Energy N.V./02-Deployable` contains only `4-SystemAPI` and `Framework`. Nearest match is sandbox `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-leads` (Rjo4ODYyMjQ4), which differs in root and leaf name. |
| Connection to reuse C4 [Confluent_Kafka] | FAIL | Spec location `Calor Group Limited/00-ConnectionResources/00-Connections` does not exist. `SHV Energy N.V./00-ConnectionResources/00-Connections` holds only `[Confluent_NL-HQ_Kafka]` (c85b494e-58ab-4591-b946-76a9ec636414). `[Confluent_Kafka]` exists only as two copies in `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/France Process`: 29f19e6a-e6ed-4a7b-ac00-be5ffdc13171 and ce28029d-448f-4717-bc56-68ec76af86f5. Which one (if any) to reuse is not determinable from the spec. |
| V4 facade returns documents | FAIL | Facade 338df4f8 v1 (at the CLAUDE.md path): shape1 Start -> shape19 Process Route `[MED] Process Service` (wait=true, abort=true) -> Default -> shape20 Stop (continue=true); FlowDocuments -> shape22 Stop (continue=true). Zero `returndocuments` shapes. Steps after the Process Call (400 and 500 responses) would not run. Spec says: stop, do not redesign. |
| V1, V2, V3, V5 | NOT RUN | Each needs a deploy and test run in dev/test; blocked by the environment classification, and building is blocked by V4, folder and connection. |
| Base path `gb-cg-leads/v1` uniqueness | NOT RUN | Blocked before build. |
| Topic existence | NOT RUN | Needs a runtime test against the Kafka connection; blocked. |

## Decisions

| # | Decision | Reason |
|---|----------|--------|
| 1 | Stopped before creating any component | V4 fails (spec: stop on this); folder path and connection cannot be resolved without inventing values; environment classification cannot be confirmed |

## Deviations from spec

| # | Spec line | What was built instead | Reason |
|---|-----------|------------------------|--------|

None. Nothing built.

## Deployments

| Date | Environment | Classification | Deployment ID | Purpose |
|------|-------------|----------------|---------------|---------|

None.

## Temporary Notify shapes

| Process | Shape | Reason | Added | Removed |
|---------|-------|--------|-------|---------|

None.

---

# Attempt 2 (round 0, spec revision 4), 2026-10-08

Spec hash built from: bf649b3a2e7c43a03c1ecd033378a324636eafd42790104ee6f3db444256d17c (recomputed 2026-10-08, matches pipeline-state.md; spec revision 4)

Status: BLOCKED in pre-build checks. No component was created, pushed or deployed. No folder was created. No extension value was changed.

## Components

| Name | Type | Component ID | Version | Folder | Pulled XML |
|------|------|--------------|---------|--------|------------|

None created or changed. Read-only pulls (into active-development only, not edited, not pushed):

| Name | Type | Component ID | Version | Purpose |
|------|------|--------------|---------|---------|
| [Confluent_NL-HQ_Kafka] | connector-settings (kafka) | c85b494e-58ab-4591-b946-76a9ec636414 | 9 | D3 |
| [MED] SEND bu-short.q.domain-short.businessobject.amm.inout.verb | connector-action (kafka, PRODUCE) | 7bfb1b08-208f-4368-b360-51a3b4a138d0 | 2 | Produce operation template (V2 research) |
| 47 components referencing c85b494e | process | see active-development/inventories/kafka_refs.tsv | current | Override block and header research |
| 104 API Service components | webservice | see active-development/inventories/webservice_basepaths.tsv | current | Base path uniqueness |

## Pre-build checks (2026-10-08)

| Check | Result | Evidence |
|-------|--------|----------|
| Spec hash | PASS | Recomputed hash equals the recorded hash |
| Platform connection | PASS | Authenticated to shvenergynv-6R344K. Credentials come from the process environment (.env is empty; env-check prints no rows and exits 1 because grep finds no lines, not because of a fault) |
| D1 Environment | PASS | `--list-environments`: 1-DEV = 693e8bc2-46f8-4c7f-8259-8dcf6cf0f264; BOOMI_ENVIRONMENT_ID equals it; user-confirmed development (spec rev 4) |
| D2 Folder | PASS (not yet created) | Parent `.../Customer Portal/Publisher` exists; its only child is `PUB-GB-CG-043-leads` (Rjo4ODYyMjQ4). Leaf `PUB-GB-CG-043-Lead` not created because the build stopped first |
| D3 Reused connection | PASS | 1-DEV extensions for c85b494e: username set (useDefault=false), password encrypted value set; all other fields useDefault=true, and the component's own values for bootstrap_servers, security_protocol and sasl_mechanism are non-empty. Nothing supplied or changed |
| Runtime API tier | PASS | Atom 9beaf0cb-ca88-48e6-83a2-48cebe240f61: apiType advanced, url https://shv-energy-test.boomi.cloud |
| Base path `gb-cg-leads/v1` uniqueness | PASS | All 104 webservice components pulled; none has urlPath `gb-cg-leads/v1` (so none can be deployed with it). Only GB-CG one: `[PUB-GB-CG-043] Leads API` bd886149 v1, base `gb-cg`, in the old `-leads` folder |
| V2 Kafka header `Retry-Count` | FAIL (cannot determine mechanism) | No local skill reference for the kafka connector. Boomi docs unreachable from this environment (developer.boomi.com and help.boomi.com: getaddrinfo ENOTFOUND). Across all 47 components that reference c85b494e, the only Kafka document properties used are connector.kafka.message_key, topic_name, topic_partition, message_offset; no header property and no operation header field. The PRODUCE operation config (7bfb1b08) has fields client_id, acks, compression_type, operation_timeout only. Inventing a property ID would be guessing. |
| C7/C8 operation extensions (topic) | FAIL (not supported as documented) | Skill `process_extensions.md`: "Only operations with actionType=LISTEN support extension overrides. Other actionTypes ... are rejected at write time." C7/C8 are PRODUCE operations; the topic is the operation's objectTypeId, not an operation field. No process among the 47 declares any OperationOverride (all `<Operations/>` empty). The spec (Connectors table, Test notes "Technical error" and "Retry-send failure", "Extensions") depends on a C7/C8 topic extension |
| D4, V1, V3, V5, V6, Topic existence | NOT RUN | Need a deployed build; stopped before building |

## Decisions

| # | Decision | Reason |
|---|----------|--------|
| 1 | Stopped before creating the folder or any component | V2 and the operation-extension requirement cannot be built as written from available sources; developer must not redesign |
| 2 | (For the next attempt) API route: overrides objectName="leads", urlPath="", httpMethod="POST" | Effective path is /<base>/<objectName>/<urlPath>; urlPath="leads" with WSS objectName "leads" would give /gb-cg-leads/v1/leads/leads, not the spec's /ws/rest/gb-cg-leads/v1/leads. To verify at test time |
| 3 | (For the next attempt) Kafka connection extensions: reuse the platform-generated ConnectionOverride block for c85b494e as found in 45 of 46 account processes (17 fields, no xpath attributes) | process_extensions.md: emit the platform-generated block, do not hand-author |

## Deviations from spec

None. Nothing built.

## Deployments

None.

## Temporary Notify shapes

None.

---

# Attempt 3 (round 0, spec revision 5), 2026-10-08

Spec hash built from: e163319eb14898d5f28a5ceedd3a3f991c5b7ba579f0af7674067352d1138899 (recomputed 2026-10-08, matches pipeline-state.md; spec revision 5)

Status: BLOCKED (missing value: endpoint credentials). Everything in the spec is built, pushed and deployed to 1-DEV. The runtime checks that need an HTTP call to the endpoint could not run (see "Developer checks").

## Components

All of them are in `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead` (folder ID Rjo4ODkxNDA5, created in this attempt).

| # | Name | Type | Component ID | Version | Pulled XML |
|---|------|------|--------------|---------|------------|
| C1 | [Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG] | process | 135044a4-ad21-4ba0-b4d7-5e5c21fac446 | 1 | build/components/process/ |
| C2 | PUB-GB-CG-043 Lead API | webservice | 4c878feb-2bc3-42f1-9ef5-06cea4a18529 | 1 | build/components/webservice/ |
| C3 | PUB-GB-CG-043 WSS Listen Lead | connector-action (wss) | 0f214069-c48d-4633-b60d-189e21dec918 | 1 | build/components/connector-action/ |
| C5 | PUB-GB-CG-043 Lead Request JSON | profile.json | 27f55bec-bae3-4465-87cc-ad9a8944e71d | 1 | build/components/profile.json/ |
| C6 | PUB-GB-CG-043 Lead Response JSON | profile.json | f07edecd-68d1-4aeb-acd1-e1b5fc28cb96 | 1 | build/components/profile.json/ |
| C7 | PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.insert | connector-action (kafka PRODUCE) | 583b0437-f8fc-4624-bddc-efff3172e49c | 1 | build/components/connector-action/ |
| C8 | PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.retry | connector-action (kafka PRODUCE) | be398af2-5ce6-48b1-b116-ba822ca179f5 | 1 | build/components/connector-action/ |

Reused, not edited and not pushed: C4 [Confluent_NL-HQ_Kafka] c85b494e (still version 9, current), C9 [MED] (sub) CACHE Notification Facade 338df4f8 (version 1).

Read-only pulls made for reference only (into active-development, not edited or pushed): c54a0d5e, 0dea7d10, 3c0e1d39 (old `-leads` interface components), d27a7bda and 36312dbe (EMAIL_API operations).

C1 structure (pulled XML): Start (WSS Listen, C3) -> TC-A shape2 (retry 0, catch all) -> shape3 Data Process "Check JSON body" (S1, groovy2) -> shape4 Decision "Body is valid JSON?" (DDP_VALIDATION_ERROR equals empty).
True: TC-T shape5 (retry 3). Try: C7 produce -> Response 202 -> Message Accepted -> Return "Accepted". Catch: C8 produce -> Response 202 (parked) -> Message Accepted (parked) -> Return "Accepted - parked on retry topic".
False: TC-F shape14 (retry 0). Try: Exception "Functional error" (stopsingledoc=true, message = DDP_VALIDATION_ERROR). Catch: BR-F shape16 (numBranches=2). Branch 1: Set DDP_MED_NS_Msg = Base - Try/Catch Message -> Process Call facade (wait, abort, no return paths). Branch 2: Response 400 -> Message Rejected (message = Base - Try/Catch Message) -> Return "Rejected - functional error".
TC-A catch: BR-A shape22 (numBranches=2). Branch 1: Set DDP_MED_NS_Msg -> facade. Branch 2: Response 500 -> Message Error (fixed text) -> Return "Error".
Shape counts: Try/Catch 3, Branch 2, Process Call 2, Return Documents 4, Exception 1, Decision 1, Data Process 1, Kafka connector steps 2, Notify 0. workload="bridge", allowSimultaneous="true". processOverrides: connection c85b494e only (17 fields, no xpath). No OperationOverride.

## Developer checks (2026-10-08)

| Check | Result | Evidence |
|-------|--------|----------|
| Spec hash | PASS | Recomputed hash equals the recorded hash |
| Platform connection | PASS | `--test-connection`: authenticated to shvenergynv-6R344K |
| D1 Environment | PASS | `--list-environments`: 1-DEV = 693e8bc2-46f8-4c7f-8259-8dcf6cf0f264 = BOOMI_ENVIRONMENT_ID; user-confirmed development. No other environment touched |
| Runtime API tier | PASS | Atom 9beaf0cb: apiType advanced, url https://shv-energy-test.boomi.cloud, minAuth none |
| D2 Folder | PASS | Parent `.../Customer Portal/Publisher` (Rjo4ODYyMjQ3) existed. Created leaf `PUB-GB-CG-043-Lead` (Rjo4ODkxNDA5). Folder search: 7 new components there. Old `PUB-GB-CG-043-leads` (Rjo4ODYyMjQ4) still holds the same 5 components, all version 1, last modified 2026-09-25 |
| D3 Reused connection | PASS (unchanged) | c85b494e still version 9 (current). Not edited or pushed |
| D6 Connection override block | PASS (declaration); runtime binding not testable | C1 declares the 17-field platform-generated block for c85b494e, copied verbatim from `[MED]-[Tracking]-[Boomi]-[NL-HM]-[CreateEmailNotification] USER (main) V1` (no xpath). No OperationOverride for C3, C7 or C8. `boomi-extensions.sh get` after deploy: the 1-DEV connection entry for c85b494e lists all 17 fields. Note: the extensions API is per environment, so it cannot show the fields as belonging to C1 alone, and the 17 fields were already listed before the deploy because other processes declare them. `set` not run. See the D6 premise note under Decisions |
| Extension values unchanged | PASS | sha256 of the c85b494e connection entry in `extensions get`, before and after the deploy: 36df9143...5ac6 both times |
| Base path `gb-cg-leads/v1` uniqueness (recheck before deploy) | PASS | `component-search --type webservice`: 104 components, the same count as Attempt 2; the latest modifiedDate is 2026-09-28, before Attempt 2, so the Attempt 2 base path inventory still holds. The only one using it is the new C2 |
| D5 API route | NOT RUN (blocked) | C2 is configured with POST, objectName `leads`, urlPath "", base `gb-cg-leads/v1`. A single test POST to /ws/rest/gb-cg-leads/v1/leads with no auth returned HTTP 401 UNAUTHORIZED (runtime perimeter). SERVER_USERNAME and SERVER_TOKEN are defined but empty in this session, so `boomi-wss-test.sh` with SERVER_AUTH_TYPE=basic refuses to run. No execution record was created |
| D4 Facade runtime | NOT RUN (blocked) | Needs the functional-error HTTP test; see D5 |
| V1 | Review only (spec) | TC-T and its catch path sit on TC-A's try path (shape2 Try -> shape3 -> shape4 -> shape5) |
| V3 HTTP status property | PARTIAL: mechanism from an account process; runtime NOT RUN | Boomi docs unreachable (help.boomi.com and developer.boomi.com: getaddrinfo ENOTFOUND). Account process `[MED] - CREATE EmailAPI` (c0b3d5ec v13, a WSS listener) sets the response status with DDP `outstatuscode` (= 202) and DDP `outheader_Content-Type`. No pulled process uses a Web Services Server connector property for status. C1 uses DDP `outstatuscode` (202/202/400/500). Runtime confirmation is blocked (see D5) |
| V5 | NOT RUN (blocked) | Needs the functional-error HTTP test |
| V6 BR-F | NOT RUN (blocked) | Needs the functional-error HTTP test. V6 for BR-A is review only (spec, F3) |
| Topic existence | NOT RUN (blocked) | `gb-cg.q.leads.in.insert` is proven only by a successful happy-path produce, which needs the endpoint. `gb-cg.q.leads.in.retry` cannot be checked with the skill CLI tools without producing a message to it, which the spec does not allow in this build (review only, "nothing on the retry topic") |

Executions: none. The single 401 request did not reach the runtime process, so it has no execution ID.

## Decisions

| # | Decision | Reason |
|---|----------|--------|
| 1 | HTTP status set with DDP `outstatuscode` in a Set Properties step (static 202/400/500) | V3 lets the developer confirm the property against Boomi docs or an existing account process. The docs are unreachable; the only account precedent is `[MED] - CREATE EmailAPI`. Unconfirmed at runtime until the endpoint can be called |
| 2 | Tracking field `email`: account tracked fields `primarykey` (33185) = static "Email" and `primaryvalue` (33186) = C5 element `email` (key 6), on C3, C7 and C8 | These are the only tracked-field slots in evidence in the account, used by this interface's earlier operations (c54a0d5e, 0dea7d10). No account tracked field named "email" was found, and the skill has no CLI tool to list CustomTrackedField |
| 3 | C3 operationType CREATE, inputType/outputType singlejson, responseContentType application/json | operationType must be one of the platform keywords; route method POST comes from C2 (D5) |
| 4 | C7/C8 fixed fields: client_id `gb-cg.leads`, acks 1, compression snappy, operation_timeout 30000 | Not in the spec. Values follow the framework Produce template 7bfb1b08 and this interface's earlier operation 0dea7d10. No header_properties, no partition, no key |
| 5 | No OperationOverride for the WSS Listen operation C3 | The spec asks to extend "every operation field the platform allows". No platform-generated WSS OperationOverride exists in any pulled account process (0 of 47), the skill documents none, and docs are unreachable. process_extensions.md forbids hand-authoring override blocks. Flagged for the reviewer: if the platform does allow WSS operation extensions, the field list must come from a GUI-generated block |
| 6 | D6 premise discrepancy (recorded, no change to the build) | The spec says the 17-field no-xpath block appears in "45 of the 46 account processes". The pulled data (active-development/inventories/kafka_refs.tsv, 47 processes) shows 22 processes with a 9-field block (no xpath), 4 with the 17-field block (no xpath), 1 with 10 fields, 1 with 9 fields plus xpath (old CreateLead), and 19 with none. The spec's concrete instruction (17 fields, no xpath) matches a real platform-generated block that lists every field of the connector, so it was built as written. The skill (process_extensions.md, Issue #31) warns that fields without xpath may be inert at runtime. This cannot be tested without changing the shared extension values, which is forbidden |
| 7 | S1 reads the body bytes once and re-stores the same bytes | The document passes through unchanged (mapping.md: pass-through) |
| 8 | Deployments left in place in 1-DEV | They are needed for the endpoint tests once credentials are available |

## Deviations from spec

None.

## Deployments

| Date | Environment | Classification | Component | Package ID | Notes |
|------|-------------|----------------|-----------|------------|-------|
| 2026-10-08 | 1-DEV (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264) | development (user-confirmed) | C1 135044a4 v1 | 2cb065e7-6cb9-4e7c-8852-93ea49a6016f | Bridge mode (workload=bridge in the packaged process). The tool reports the package ID; it does not return a deployment ID |
| 2026-10-08 | 1-DEV (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264) | development (user-confirmed) | C2 4c878feb v1 | d2229e66-4e42-499f-b9b9-31f060725ff7 | |

## Temporary Notify shapes

None added. The final C1 has 0 Notify shapes.

## Blocking item

- SERVER_USERNAME and SERVER_TOKEN (Basic credentials for the 1-DEV runtime shared web server / Atom Cloud perimeter at https://shv-energy-test.boomi.cloud): needed to call `/ws/rest/gb-cg-leads/v1/leads` for D4, D5, V3, V5, V6 (BR-F), topic existence (main topic) and the happy-path check (CLAUDE.md section: Credentials & .env files; spec "Developer checks, run first"). The variables are defined but empty in this session, and the endpoint returns 401 without auth.

---

# Attempt 4 / Round 1 fix (spec revision 6), 2026-10-09

Spec hash built from: 9bcb1e480fb9e77fa301ce599a14df9f3cfedf46dca32e0a67fe7c5d90a4cf5a (recomputed 2026-10-09, matches pipeline-state.md; spec revision 6). Required values: none OPEN.

Status: findings F-1-01 and F-1-03 fixed, pushed and deployed to 1-DEV; F-1-02 needs no build change. **BLOCKED** on three runtime developer checks run for the first time with endpoint credentials: D4 (facade fails), D5 (wrong path also reaches C1) and the happy path / main-topic existence (execution time limit exceeded). See "Blocking items".

## Components (changed in this attempt)

Folder: `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead` (Rjo4ODkxNDA5).

| # | Name | Type | Component ID | Version before -> after | Pulled XML |
|---|------|------|--------------|-------------------------|------------|
| C1 | [Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG] | process | 135044a4-ad21-4ba0-b4d7-5e5c21fac446 | 1 -> 2 | build/components/process/ (byte-identical to the platform v2 pull) |
| C7 | PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.insert | connector-action (kafka PRODUCE) | 583b0437-f8fc-4624-bddc-efff3172e49c | 1 -> 2 | build/components/connector-action/ |
| C8 | PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.retry | connector-action (kafka PRODUCE) | be398af2-5ce6-48b1-b116-ba822ca179f5 | 1 -> 2 | build/components/connector-action/ |

Unchanged: C2 4c878feb v1, C3 0f214069 v1, C5 27f55bec v1, C6 f07edecd v1. Reused, not edited or pushed: C4 c85b494e (still v9, current), C9 338df4f8 (still v1, current).

Versions before editing (verified with `boomi-version-history.sh`, 2026-10-09): C1 v1, C7 v1, C8 v1 (all current, main), so the earlier stopped fix run had pushed nothing.

Read-only pulls (into active-development only, not edited or pushed): 1b208fa6-9aa8-4014-b77d-51be59717e91 `[Publisher]-[PUB-GB-CG-043]-[CreateLead]-[Customer Portal]-[GB-CG]` v1 (folder PUB-GB-CG-043-leads), C4 c85b494e v9, C9 338df4f8 v1, and 9 account Kafka PRODUCE operations (a1970311, 2806373d, d2dc4e94, 2cd81cdd, 9048f954, 01367749, d27a7bda, ee30a67e, 8435e3e3) for the D7 precedent check.

Changes:

- C1: the `ConnectionOverride` for c85b494e was replaced with the block from 1b208fa6, copied verbatim (9 fields, same `label`, `overrideable="true"` and `xpath="GenericConnectionConfig/field[@id='<id>']/@value"` on each). Nothing else in `processOverrides` was copied (1b208fa6 also has `<Properties><PropertyOverride name="DPP_KAFKA_TOPIC"/>`, which is outside the ConnectionOverride block and is not used by C1). Description text "spec rev 5" -> "spec rev 6". No shape changed.
- C7, C8: `acks` `1` -> `all`, `operation_timeout` `30000` -> `5000`. `client_id` `gb-cg.leads` and `compression_type` `snappy` unchanged. Nothing else changed (no header, key or partition).

Final C1 v2 shape counts (pulled XML): catcherrors 3, branch 2, processcall 2, returndocuments 4, exception 1, decision 1, dataprocess 1, connectoraction 2, documentproperties 6, message 4, start 1, **notify 0**. `workload="bridge"`, `allowSimultaneous="true"`. 9 `xpath` attributes in `processOverrides`. No OperationOverride.

## Developer checks (2026-10-09)

| Check | Result | Evidence |
|-------|--------|----------|
| Spec hash | PASS | Recomputed hash equals the recorded hash |
| Platform connection | PASS | `--test-connection`: authenticated to shvenergynv-6R344K. Credentials come from the process environment (.env is empty) |
| D1 Environment | PASS | `--list-environments`: 1-DEV = 693e8bc2-46f8-4c7f-8259-8dcf6cf0f264; BOOMI_ENVIRONMENT_ID equals it; user-confirmed development. No other environment touched |
| D3 Reused connection | PASS (unchanged) | c85b494e still v9, current. Not edited or pushed |
| D6.1 Pull 1b208fa6 read only | PASS | Pulled v1; not edited, pushed or deployed. It has no execution records (`boomi-execution-query.sh --process-id 1b208fa6...`: 0) |
| D6.2 Copy block verbatim | PASS | C1 v2 block = 1b208fa6 block for c85b494e, field for field (9 fields with xpath) |
| D6.3 Every copied field exists in C4 | PASS | C4 `GenericConnectionConfig` fields: username, password, bootstrap_servers, service_principal, security_protocol, sasl_mechanism, private_certificate, polling_interval, polling_delay, consumer_group. All 9 copied ids are present |
| D6.4 C4 fields not covered | PASS (accepted exception) | Only `consumer_group` (spec row 20, user "2. a"). No other uncovered field |
| D6.5 No C7/C8 operation overrides | PASS | `<Operations>` absent from C1 processOverrides |
| D6.6 Extensions after redeploy | PASS | `boomi-extensions.sh get` before the push and after the deploy: the 1-DEV c85b494e entry is present with the same field list (17 field ids, because other deployed processes still declare the 17-field block), and the sha256 of the c85b494e entry is identical before and after (79ae05c8...0d95). `set` not run. With the xpath binding, the 1-DEV values now apply to C1: username (useDefault=false, the value equals the C4 component value by hash comparison, value not recorded), password (encrypted value set; cannot be compared), all other fields useDefault=true (component defaults) |
| D7 Producer settings | PASS (component); runtime see below | C7 v2 and C8 v2: acks `all`, operation_timeout `5000`, client_id `gb-cg.leads`, compression_type `snappy`. The push accepted `all`. No account precedent for `all` exists (the 9 sampled Kafka PRODUCE operations use `acks` `0` or `1`, all with operation_timeout 30000). Whether `operation_timeout` bounds the whole send including the wait for broker metadata: **not determined**. Boomi docs are unreachable (help.boomi.com and developer.boomi.com: getaddrinfo ENOTFOUND), no account precedent shows it, and the happy-path log could not be downloaded (see below). Runtime acceptance of `acks=all` is also not confirmed, because no produce has succeeded yet |
| Base path `gb-cg-leads/v1` uniqueness (recheck before deploy) | PASS | `component-search --type webservice`: 105 components = the 104 from Attempt 2 plus C2. The only component modified since 2026-10-08 is C2 |
| Bridge mode | PASS | C1 v2 packaged with `workload="bridge"`; executions report `type=exec_listener_bridge` |
| D5 API route, correct path | PASS | POST `/ws/rest/gb-cg-leads/v1/leads` (basic auth from the environment) started C1 execution 93e06b38 (launcherID = C2 4c878feb) |
| D5 API route, wrong path | **FAIL** | POST `/ws/rest/gb-cg-leads/v1/leads/leads` (payload TC-03) **also** started C1: execution bcec584b. The spec says this path must not reach C1. Stopped as D5 instructs |
| Happy path, main topic existence, V3 (202) | **FAIL / NOT CONFIRMED** | TC-01 sample lead, execution 93e06b38: HTTP client got no response within 30 s (HTTP 000); execution status ERROR, "Process exceeded maximum execution time limit", duration 33 385 ms, inbound 1, inbound error 1, outbound 0. The main-topic produce did not complete successfully within the runtime's limit. Cause not determined: the process log download fails (`boomi-execution-query.sh --logs` exits with curl code 56, three tries), so the C7 error text is not visible. Candidates: topic `gb-cg.q.leads.in.insert` missing in the 1-DEV cluster; Kafka connection or authentication with the now-bound 1-DEV extension values; `acks=all` rejected or not satisfiable; the producer metadata wait not being bounded by `operation_timeout`. The wrong-path run bcec584b (same valid lead body) ended the same way (ERROR, same message, 30 082 ms). It is not known whether the TC-T catch path ran C8 during these two runs, so a message on `gb-cg.q.leads.in.retry` cannot be ruled out; nothing was sent to it deliberately |
| D4 Facade runtime | **FAIL** | TC-10 malformed JSON, execution 22c61363: HTTP 500 with the runtime's default HTML error page, body "Error indexing document. Could not determine value for Index key: DDP_MED_ProcessId"; status ERROR, 928 ms, outbound 0. The facade 338df4f8 only reads DDP_MED_NS_Code, DDP_MED_NS_Level and DDP_MED_NS_Msg and then calls Process Route `resource::rout:76eb8a3a-3b83-4ecc-80db-6b01446a65b2` (`[MED] Process Service`); the failing cache index key `DDP_MED_ProcessId` is not set anywhere in C1 or in the facade. The error escaped BR-F branch 1, then TC-A, then BR-A branch 1 (second facade call), matching the spec row "facade call on BR-A branch 1 also fails -> runtime default". Shared framework components not changed or deployed |
| V3 (400) | NOT CONFIRMED | Blocked by D4: BR-F branch 2 never ran |
| V5, V6 (BR-F) | NOT CONFIRMED | Blocked by D4 |
| V1 TC-T, V6 BR-A, technical-error and retry-send-failure tests | Review only | User test decision (spec row 16). Not forced |
| Topic `gb-cg.q.leads.in.retry` existence | NOT RUN | Spec: no deliberate produce to the retry topic |
| TC-15 | NOT RUN | User test decision |

Executions (all in 1-DEV, atom 9beaf0cb MCS_NL-HM_DEV_1):

| Execution ID | Request | Result |
|--------------|---------|--------|
| execution-93e06b38-ff26-465e-8d04-4bd5a37fbede-2026.10.09 | POST /ws/rest/gb-cg-leads/v1/leads, TC-01 happy-path lead | ERROR, "Process exceeded maximum execution time limit", 33.4 s, client HTTP 000 after 30 s |
| execution-22c61363-80dd-4f5e-aaa5-5fb369afbd7d-2026.10.09 | POST /ws/rest/gb-cg-leads/v1/leads, TC-10 malformed JSON | ERROR, "Error indexing document. Could not determine value for Index key: DDP_MED_ProcessId", 0.9 s, client HTTP 500 (runtime default page) |
| execution-bcec584b-4848-4856-b7ac-d4ea1b89c0d7-2026.10.09 | POST /ws/rest/gb-cg-leads/v1/leads/leads, TC-03 (wrong path) | Reached C1 (D5 fail). ERROR, "Process exceeded maximum execution time limit", 30.1 s, client HTTP 000 |

## Log analysis (2026-10-09, coordinator follow-up)

The process logs for the three executions were downloaded read only with `boomi-execution-query.sh --execution-id <ID> --logs` once platform.boomi.com was allowed. No new execution was run. Nothing was edited, pushed or deployed, and no extension value was changed. No credential value appears in the extracts below. Raw logs (local only, not part of the build): `active-development/feedback/execution-results/logs_20261009_1319*_<execution-id>.json`. Read-only reference pulls made for this analysis: Process Route `[MED] Process Service` 76eb8a3a-3b83-4ecc-80db-6b01446a65b2, route target `[MED] (sub) CACHE Notification` 47e2da88-c030-4cfe-b3b4-8c8e89ed7841 (v2), map `[MED] CREATE Notification` 911b9276-126e-4e80-9b44-306b9dae1a97.

### execution-93e06b38 (happy path, TC-01) and execution-bcec584b (wrong path, TC-03)

The two logs show the same sequence. Times are for 93e06b38, with bcec584b in brackets.

| Time | Shape | Result |
|------|-------|--------|
| 13:07:22 (13:09:21) | Start (C3) -> TC-A -> Check JSON body -> Body is valid JSON? (True) -> TC-T | OK |
| 13:07:22 -> 13:07:27 | Produce gb-cg.q.leads.in.insert (C7), first attempt | "Shape executed with errors in 5165 ms" (5060 ms); "No documents found. Skipping execution for the Response 202 step." |
| 13:07:27 -> 13:07:32 | TC-T retry 1: C7 | errors in 5052 ms (5048 ms) |
| 13:07:43 -> 13:07:48 | TC-T retry 2 (started 11 s after retry 1 ended; 13 s in bcec584b): C7 | errors in 5051 ms (5042 ms) |
| 13:07:55 (13:09:51) | TC-T retry 3 starts (7 s after retry 2; 1 s in bcec584b) | SEVERE "Unexpected error executing process: java.util.concurrent.CancellationException: Process exceeded maximum execution time limit" before any shape ran |
| 13:07:55 (13:09:51) | TC-A | "Try/Catch Shape sending 1 document(s) down error path", then the same CancellationException. No BR-A shape, Set Properties or facade line follows |

- **C7 error text:** the process log does not contain it. Every C7 attempt is logged only as "Shape executed with errors in ~5050 ms", with no exception message or stack trace for the connector. The only exception in either log is the runtime's CancellationException. The document-level error text is not exposed by the CLI tools.
- **C8 (retry topic):** **did not run** in either execution. There is no log line for "Produce gb-cg.q.leads.in.retry", "Response 202 (parked)" or the TC-T catch path, because the runtime cancelled the execution at the start of retry 3, before TC-T reached its catch path. **No message can have been sent to `gb-cg.q.leads.in.retry`** by these runs. The facade did not run either.
- **TC-T retry timing (new evidence):** retries are **not immediate** on this runtime. The gaps between attempts were 0 s, 11 s and 7 s (93e06b38) and 0 s, 13 s and 1 s (bcec584b). The spec's assumption ("Retries in TC-T run immediately, with no back-off", Error handling and "Kafka producer settings") does not hold here. The cause of the gaps is not shown in the log.
- **Runtime execution limit (new evidence):** the listener execution was cancelled at 30-33 s. With 4 attempts of about 5 s plus the observed retry gaps, TC-T never reaches its catch path within that limit. So on this runtime the designed technical-error path (C8 park, 202) and the retry-send-failure path (BR-A, 500) cannot complete when the main topic is failing. This is relevant to spec rows 16 and 19 and follow-ups F2 and F3, and is for the designer.

**Cause of the C7 failure (evidence-based conclusion):**

- Proven by the log: each C7 attempt failed after 5042-5165 ms, which is `operation_timeout` (5000 ms) plus a small overhead. So the send is bounded by `operation_timeout` and ends as a timeout-length failure, not a fast rejection. This partly answers D7: at least in this failure mode, the whole attempt (whatever the producer was waiting for) stopped at about 5 s.
- Not proven (unconfirmed): what the producer was waiting for. A fast authentication rejection or an invalid-configuration error (for example the connector refusing `acks=all`) would usually fail in well under 5 s, so these are less likely, but the log does not exclude them. The pattern fits a wait that never completes: the topic `gb-cg.q.leads.in.insert` missing (with auto-creation off), the broker or cluster not reachable from the 1-DEV runtime with the bound connection values, or `acks=all` waiting for in-sync replicas that are not available. None of these is confirmed. Topic existence is still unconfirmed.
- Suggested next evidence (for the orchestrator, not done): the Kafka error text from Process Reporting (document detail of the C7 step) in the Boomi GUI; or the Confluent administrator confirming that the topic exists and the 1-DEV principal can write to it; or a run with `acks` `1` to isolate `acks=all` (needs a spec change).

### execution-22c61363 (malformed JSON, TC-10)

Shapes in order (all at 13:09:09-13:09:10):

1. C1: Start -> TC-A -> Check JSON body -> Body is valid JSON? (False) -> TC-F -> Exception "Functional error" ("Shape executed with errors in 25 ms") -> TC-F "sending 1 document(s) down error path" -> BR-F -> branch 1: Set DDP_MED_NS_Msg -> Process Call `[MED] (sub) CACHE Notification Facade`.
2. Facade 338df4f8 -> Process Route "Executing process '[MED] (sub) CACHE Notification' with 1 document(s) for route key 'CACHE_NOTIFICATION'".
3. Route target 47e2da88: Start (Passthrough) -> Document not in Notification Cache? -> Branch -> Empty Document -> Get DPP_MED_ProcessCallStack (logs "DPP_MED_ProcessCallStack: [Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG] (Continuation f_0)") -> Stop (continue) -> Remove additional whitespace & hash document - DDP_MED_NS_MSG_HASH -> remove XML tags from DDP_MED_NS_Msg -> encryp for NL-HMt (PGP Encrypt) -> Set Properties "DDP_MED_NS_DOC, DDP_ALL, DDP_MED_ProcessId" -> Map `[MED] CREATE Notification` -> Branch -> DDP_MED_NS_MSG_HASH not in cache? -> **Document Cache Load: "Shape executed with errors in 36 ms"**.
4. Back in C1: "BR-F Notify then reject: No documents found. Skipping execution for the Response 400 step." -> TC-A "sending 1 document(s) down error path" -> BR-A -> branch 1: Set DDP_MED_NS_Msg -> facade -> same route target path -> Document Cache Load fails again -> "BR-A Notify then error: No documents found. Skipping execution for the Response 500 step."
5. Final: SEVERE "First document failure: Error indexing document.  Could not determine value for Index key: DDP_MED_ProcessId". The HTTP 500 is the runtime default, not C1's BR-A response.

- **Exact error:** `Error indexing document.  Could not determine value for Index key: DDP_MED_ProcessId` (Document Cache Load in route target 47e2da88, document cache 5561b6a6-8ba0-4bb5-a30f-3239c1c39f60).
- **Root cause (proven from the XML and log):** the route target's Set Properties step "DDP_MED_NS_DOC, DDP_ALL, DDP_MED_ProcessId" sets `DDP_MED_ProcessId` from the process property **`DPP_MED_ProcessId`** (`processpropertydefaultvalue=""`). C1 never sets `DPP_MED_ProcessId`, so the DDP is empty and the document cache cannot index it. The Process Route target is deployed and runs in 1-DEV (the D4 route-target concern does not apply). The failure is a missing caller input.
- **Kafka:** no Kafka shape ran (correct for the functional path). C8 did not run.
- **V5 partial evidence:** the Exception step ran and TC-F caught it. The 400 body was never built, so V5 and V6 stay unconfirmed.

Inputs the facade / route path reads that C1 does not set (facade 338df4f8 description "Input:" list, the route target 47e2da88 XML and map 911b9276 PropertyGet functions):

| Property | Kind | Read by | Effect when empty |
|----------|------|---------|-------------------|
| `DPP_MED_ProcessId` | DPP | Route target Set Properties -> `DDP_MED_ProcessId` (document cache index key); map PropertyGet | **Fatal**: Document Cache Load fails (this error) |
| `DDP_MED_NS_Level` | DDP | Facade input list; map 911b9276 | Not fatal in this run (the error came later); notification field empty |
| `DDP_MED_NS_Code` | DDP | Facade input list; map 911b9276 | Not fatal in this run; notification field empty |
| `DPP_MED_AccountId` | DPP | Facade input list; map PropertyGet | Not fatal in this run; empty or map default |
| `DPP_MED_APIURL` | DPP | Facade input list; map PropertyGet | as above |
| `DPP_MED_AtomId` | DPP | Facade input list; map PropertyGet | as above |
| `DPP_MED_AtomName` | DPP | Map PropertyGet (not in the facade input list) | as above |
| `DPP_MED_ContainerId` | DPP | Facade input list; map PropertyGet | as above |
| `DPP_MED_Environment` | DPP | Facade input list; map PropertyGet | as above |
| `DPP_MED_Environment_Class` | DPP | Facade input list; map PropertyGet | as above |
| `DPP_MED_ExecutionId` | DPP | Facade input list; map PropertyGet (map default "unknownExecu...") | as above |
| `DPP_MED_ProcessName` | DPP | Facade input list; map PropertyGet | as above |
| `DPP_MED_TrackingId` | DPP | Facade input list; map PropertyGet | as above |
| `DPP_MED_TrackedFields` | DPP | Facade input list; map PropertyGet | as above |

C1 sets only `DDP_MED_NS_Msg` (as the spec requires). `DDP_MED_NS_DOC`, `DDP_ALL`, `DDP_MED_ProcessId`, `DDP_MED_NS_MSG_HASH` and `DPP_MED_ProcessCallStack` / `DPP_ProcessCallStack` are set inside the route target itself. Which values C1 should supply for the 13 missing inputs, and how other SHV framework processes normally set them, is a design question; no value has been invented.

## Decisions

| # | Decision | Reason |
|---|----------|--------|
| 1 | `acks` written as the literal string `all` | Spec row 18 and D7 say `all`. No account precedent or reachable documentation gives another stored form (for example `-1`); substituting one would be inventing a value. The platform accepted the push |
| 2 | Only the `ConnectionOverride` element was copied from 1b208fa6, not its `DPP_KAFKA_TOPIC` property override | D6.2 names the ConnectionOverride block only; C1 has no DPP_KAFKA_TOPIC (topics are fixed in C7/C8, spec row 14) |
| 3 | Stopped testing after one run per failing check | D4 and D5 tell the developer to stop and return. A second functional-error run would only call the failing shared facade again, and more happy-path runs would add more produce attempts while the cause is unknown |
| 4 | Deployments left in place in 1-DEV | Needed for the re-test after the design answers |
| 5 | Local extension dumps deleted from active-development after the hash comparison | They contained a connection username value. Nothing about credential values is recorded here |

## Deviations from spec

None.

## Deployments

| Date | Environment | Classification | Component | Package ID | Notes |
|------|-------------|----------------|-----------|------------|-------|
| 2026-10-09 | 1-DEV (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264) | development (user-confirmed) | C1 135044a4 v2 | 7d8121d2-647f-493d-a192-8d01219cd7c7 | Bridge mode. Replaces package 2cb065e7 (C1 v1). Bundles C7 v2, C8 v2 and C9 v1. The tool returns the package ID, not a deployment ID |

C2 package d2229e66 (v1, unchanged) is still deployed and was not redeployed.

## Temporary Notify shapes

None added. Final C1 v2 has 0 Notify shapes.

## Blocking items

1. **D4 facade fails in 1-DEV** (spec D4: "If it fails ... stop and return to the orchestrator. Do not deploy or edit shared framework components"). The facade's Process Route target fails on the cache index key `DDP_MED_ProcessId`, which the spec does not tell C1 to set. The designer needs to decide which DDPs (for example `DDP_MED_ProcessId`, and possibly `DDP_MED_NS_Code` / `DDP_MED_NS_Level`, which the facade reads) C1 must set before the facade call, and their values, or whether the 1-DEV framework deployment is at fault. Evidence: execution 22c61363. **Updated by the log analysis:** the route target is deployed and runs; the fatal missing input is the process property `DPP_MED_ProcessId`, and 12 further facade inputs are unset (see "Log analysis").
2. **D5 wrong path reaches C1** (spec D5: "If the effective path differs, stop and return to the orchestrator"). `/ws/rest/gb-cg-leads/v1/leads/leads` started C1 (execution bcec584b), so the API Service route also matches a trailing extra segment.
3. **Happy path does not complete and main-topic existence is unconfirmed** (spec "Topic existence": "If not, stop and return to the orchestrator"). Execution 93e06b38 exceeded the runtime's maximum execution time (about 30 s) with no response. The C7 error is not visible because the log download fails (curl exit 56). **Updated by the log analysis:** logs now downloaded. C7 failed 4 times at about 5 s each (operation_timeout) with no error text in the process log; TC-T retries had 7-13 s gaps; the runtime cancelled at the start of retry 3, so C8 and the facade never ran and nothing reached the retry topic. Cause unconfirmed (see "Log analysis"). Also relevant to spec row 19: the runtime ended a listener execution at about 30-33 s, so the accepted worst case of "about 25 s plus the facade" is close to this runtime limit.

---

# Attempt 5 / revision 7 (round 1 fix, 2026-10-09)

Status: **BLOCKED: connectivity** at D0. Nothing was created, changed, pushed or deployed in this attempt. C1 135044a4 v2 (package 7d8121d2), C2 4c878feb v1, C3 0f214069 v1, C7 583b0437 v2 and C8 be398af2 v2 are unchanged.

## D0 connectivity checks

| Check | Result |
|-------|--------|
| `boomi-env-check.sh` | Exit 1, no variable list. The project `.env` is empty (0 bytes); the script reads variable names from `.env`, so it lists nothing. The credentials come from the process environment instead (checked by name only, below) |
| `boomi-folder-create.sh --test-connection` | Passed (connected to account shvenergynv-6R344K) |
| Platform variables | BOOMI_API_URL, BOOMI_USERNAME, BOOMI_API_TOKEN, BOOMI_ACCOUNT_ID, BOOMI_ENVIRONMENT_ID, BOOMI_TEST_ATOM_ID, BOOMI_VERIFY_SSL, BOOMI_TARGET_FOLDER: SET (process environment) |
| Runtime endpoint credentials | SERVER_USERNAME: SET. SERVER_TOKEN: SET. SERVER_BEARER_TOKEN: EMPTY. SERVER_AUTH_TYPE: SET. SERVER_BASE_URL: SET |
| `platform.boomi.com` (log downloads) | Reachable (HTTP 200) |
| `api.boomi.com` | Reachable (HTTP 200) |
| `shv-energy-test.boomi.cloud` (1-DEV runtime) | Reachable (HTTP 404 at `/`, so the server answered) |
| `help.boomi.com` | **Not reachable**: proxy CONNECT 403 (curl exit 56); WebFetch: DNS lookup failed (ENOTFOUND) |
| `developer.boomi.com` | **Not reachable**: proxy CONNECT 403 (curl exit 56); WebFetch: DNS lookup failed (ENOTFOUND) |

Spec hash recomputed: 8a32401414260fab4c811eeb3093d9cb5789aa2948caa93135861a919a8f0d49 (matches pipeline-state.md). Kafka topic gate: `gb-cg.q.leads.in.insert` is recorded under "Kafka topics confirmed" (passed).

## Blocking item

The run needs the Boomi documentation hosts: the orchestrator requires V7 (Process Call abort = false lets branch 2 run after a facade failure) to be verified against Boomi documentation before relying on it, and D5 step 1 requires a documentation search for an exact API Service route. Both `help.boomi.com` and `developer.boomi.com` are unreachable from this session, so D0 fails and, per CLAUDE.md "Connectivity checks first", nothing was changed. Remedy: allow `help.boomi.com` and `developer.boomi.com` through the session's network policy, or have the user paste the relevant Boomi documentation (Process Call shape "Abort if process fails"; API Service REST route / URL path matching), then re-run the developer.

---

# Attempt 6 / revision 7 (round 1 fix, re-run, 2026-10-09)

Status: **BLOCKED: V7 not confirmed by Boomi documentation** (spec V7: "Before building, confirm the abort = false behaviour from Boomi documentation ... If the documentation says abort = false does not let branch 2 run, stop and return to the orchestrator; do not add a Try/Catch"). Nothing was created, changed, pushed or deployed. C1 135044a4 v2 (package 7d8121d2-647f-493d-a192-8d01219cd7c7), C2 4c878feb v1 (package d2229e66), C3 0f214069 v1, C7 583b0437 v2 and C8 be398af2 v2 are unchanged. `build/components/` was not refreshed, because no component changed.

## D0 connectivity checks (all passed)

| Check | Result |
|-------|--------|
| `boomi-env-check.sh` | Not usable here: the project `.env` is empty and the variables come from the process environment. As agreed by the orchestrator, the by-name check below is the env check result |
| Platform variables (by name) | BOOMI_API_URL, BOOMI_USERNAME, BOOMI_API_TOKEN, BOOMI_ACCOUNT_ID, BOOMI_ENVIRONMENT_ID, BOOMI_TEST_ATOM_ID, BOOMI_VERIFY_SSL, BOOMI_TARGET_FOLDER: SET |
| `boomi-folder-create.sh --test-connection` | Passed (account shvenergynv-6R344K) |
| Runtime endpoint credentials | SERVER_USERNAME SET, SERVER_TOKEN SET, SERVER_BEARER_TOKEN EMPTY, SERVER_AUTH_TYPE SET (SERVER_BASE_URL SET) |
| `platform.boomi.com` | HTTP 200 |
| `api.boomi.com` | HTTP 200 |
| `shv-energy-test.boomi.cloud` (1-DEV runtime) | Reachable (HTTP 404 at `/`) |
| `help.boomi.com` | HTTP 200 (curl through the proxy; WebFetch still cannot resolve the host, so curl was used) |
| `developer.boomi.com` | HTTP 200 (`/llms.txt`) |

Spec hash recomputed twice: 8a32401414260fab4c811eeb3093d9cb5789aa2948caa93135861a919a8f0d49 (matches). Kafka topic gate: `gb-cg.q.leads.in.insert` is recorded in pipeline-state.md "Kafka topics confirmed" (passed).

## V7 documentation check (failed: not confirmed)

Sources read (2026-10-09):

1. help.boomi.com, "Process Call step" (updated 21 April 2026): https://help.boomi.com/docs/Atomsphere/Integration/Process%20building/r-atm-Process_Call_shape_cc0f1835-4d30-499f-8fd2-95d3c0997c85
   - "Wait for the process to complete. If selected, the parent process waits for the subprocess to complete before continuing to its next step. **If the subprocess fails, the parent process stops.** If cleared, and if Abort if process fails is selected, the parent process reports the subprocess' error after all subprocesses have executed."
   - "Abort if subprocess fails. If selected, the parent process stops and is marked as failed if the subprocess fails."
2. help.boomi.com, "Process Route step": https://help.boomi.com/docs/Atomsphere/Integration/Process%20building/r-atm-Process_Route_shape_5ee00436-fb63-43c1-8fcb-48f8c8829115. It has the same wording for "Wait" ("If the subprocess fails, the parent process stops") and "Abort".
3. help.boomi.com, "Branch step": https://help.boomi.com/docs/Atomsphere/Integration/Process%20building/r-atm-Branch_shape_83d94692-c1c3-4ad6-a6e6-50ee0e48c495. It says only that "A branch's path is executed to completion before executing the next branch" and says nothing about a failed branch.
4. Skill `process_call_step.md`: `abort` = "Whether parent process aborts if subprocess fails" (no behaviour for false).

Finding: the spec uses wait = true. For that setting the documentation says "If the subprocess fails, the parent process stops." The sentence does not depend on the Abort option. No source says that clearing Abort lets the parent continue: the document going on to BR-F or BR-A branch 2 after a facade failure. The documentation therefore does not confirm V7, and on its plain reading it says the opposite (with wait = true the parent stops). Clearing Abort is documented only as not marking the parent as failed. The spec forbids forcing a facade failure to test it (V7, F3) and forbids adding a Try/Catch. So rows 23, 27 and 28 and the "Facade fails" row of the error table cannot be shown to work as designed. Stopped before building, per V7.

Options for the designer and user (not decided by the developer): keep abort = false and accept V7 as unconfirmed (runtime confirmation later under F3); keep abort = false and approve a controlled facade-failure test in 1-DEV; or change the design so the error response does not depend on the facade outcome.

## D5 evidence gathered (read only; nothing changed or deployed)

- Documentation: help.boomi.com, "Adding a REST endpoint to an API service component" (updated 22 July 2026): https://help.boomi.com/docs/Atomsphere/API%20Management/Topics/t-atm-Adding_a_REST_endpoint_to_an_API_component_ab757f9c-ebf1-4ee2-97d4-8016460378bb. "The Match the exact endpoint checkbox controls how the system routes incoming API requests. The endpoint responds only to precisely defined requests ... the system requires static path components to match exactly ... The system honors exact match configurations only if you deploy the corresponding process ... When you uncheck the checkbox, the system applies the Best Match principle, finding the most specific or closest matching pattern among deployed endpoints." Full URL form: `http://Host:port/REST_url_path/Object/Path_Parameters`.
- Account precedent (pulled read only, 105 API Service components): the route `overrides` element takes the attribute `exactMatch`. It is `exactMatch="true"` in `[CustomerPortals]-[NL-HQ] BUSINESS v1 (QA)` (fd4b3297, v1) and `(stage)` (57c70a99, v1), and `exactMatch="false"` in `(PROD)` (2cdd7641). C2 has no `exactMatch` attribute, so best match applies today, which explains why `/leads/leads` reaches C1 (bcec584b).
- Candidate for D5 (not verified at runtime, because the run stopped at V7): C2 route `overrides` with `objectName="leads"`, `urlPath=""`, `httpMethod="POST"` and **`exactMatch="true"`**, under base path `gb-cg-leads/v1`. It must still pass D5 step 2 in 1-DEV.
- Base-path uniqueness (rechecked over all 105 API Services): `gb-cg-leads/v1` is used only by C2 (4c878feb); `gb-cg-leads/v2` is used by none; `[PUB-GB-CG-043] Leads API` (bd886149) uses `gb-cg`.

## Developer checks (Attempt 6)

| Check | Result |
|-------|--------|
| D0 | Passed |
| D1 | Passed (unchanged; 1-DEV only, no deployment made) |
| D2 to D4, D6 to D8 | Not run (stopped at V7, before building) |
| D5 | Evidence gathered only (above); not verified at runtime |
| V1, V3, V5, V6, V8 | Not run |
| V7 | **Failed: not confirmed by documentation** (above) |

## Deployments

None in this attempt.

## Temporary Notify shapes

None added. C1 v2 is unchanged and has 0 Notify shapes.

---

# Attempt 7 / revision 8 (round 1 fix, 2026-10-09)

Spec: revision 8 (second pass), approved by the user 2026-10-09 ("yes, I approve revision 8"). Hash recomputed from the repo root: 4e1f32f5e656ec7f26bdc4455947e44804dcbaf201a4b16baf2cdb38cc7dd635 (matches pipeline-state.md). Required values: none OPEN. Kafka topic gate: `gb-cg.q.leads.in.insert` is recorded under "Kafka topics confirmed" (passed).

Status: **BLOCKED: spec cannot be built as written (D8 happy path).** Every revision 8 change is implemented, pushed and deployed to 1-DEV. D4, D5, V3 (400), V5, V6 (BR-F) and the TC-A placement pass at runtime. The first successful Kafka produce shows that the Kafka Produce step outputs **no document**, so the designed valid path (C7 -> "Response 202" -> "Accepted" -> Return Documents "Accepted") never runs after a successful send, and the caller gets HTTP 200 with an empty body instead of 202 `{"status":"accepted"}`. See "Blocking item".

## D0 connectivity checks (all passed)

| Check | Result |
|-------|--------|
| `boomi-env-check.sh` | Ran; lists no variables because the project `.env` is empty. The by-name check below is the env check result (accepted by the user, spec D0) |
| Platform variables (by name) | BOOMI_API_URL, BOOMI_USERNAME, BOOMI_API_TOKEN, BOOMI_ACCOUNT_ID, BOOMI_ENVIRONMENT_ID, BOOMI_TEST_ATOM_ID, BOOMI_VERIFY_SSL, BOOMI_TARGET_FOLDER: SET |
| `boomi-folder-create.sh --test-connection` | Passed (account shvenergynv-6R344K). No auth error |
| Runtime endpoint credentials | SERVER_AUTH_TYPE SET, SERVER_USERNAME SET, SERVER_TOKEN SET, SERVER_BEARER_TOKEN EMPTY (SERVER_BASE_URL SET) |
| `platform.boomi.com` | HTTP 200 |
| `api.boomi.com` | HTTP 200 |
| `shv-energy-test.boomi.cloud` (1-DEV runtime) | Reachable (HTTP 404 at `/`, so the server answered) |
| `help.boomi.com` | HTTP 200 |
| `developer.boomi.com` | HTTP 200 (`/llms.txt`) |

## Components (changed in this attempt)

Folder: `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead` (Rjo4ODkxNDA5). Versions before editing were checked with `boomi-version-history.sh`: C1 v2, C2 v1, C7 v2 (all current, main).

| # | Name | Type | Component ID | Version before -> after | Pulled XML |
|---|------|------|--------------|-------------------------|------------|
| C1 | [Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG] | process | 135044a4-ad21-4ba0-b4d7-5e5c21fac446 | 2 -> 3 | build/components/process/ |
| C2 | PUB-GB-CG-043 Lead API | webservice | 4c878feb-2bc3-42f1-9ef5-06cea4a18529 | 1 -> 2 | build/components/webservice/ |
| C7 | PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.insert | connector-action (kafka PRODUCE) | 583b0437-f8fc-4624-bddc-efff3172e49c | 2 -> 3 | build/components/connector-action/ |

Unchanged: C3 0f214069 v1, C5 27f55bec v1, C6 f07edecd v1, C8 be398af2 v2 (left in the folder, unreferenced, F4). Reused, not edited, pushed or deployed: C4 c85b494e, C9 338df4f8 and its route targets.

Changes:

- **C7 v3:** `operation_timeout` 5000 -> 3000. Nothing else changed (`acks` `all`, `client_id` `gb-cg.leads`, `compression_type` `snappy`, tracking slots, no header, key or partition). C8 not changed.
- **C2 v2:** the single REST route `overrides` now has `exactMatch="true"` (attribute form copied from fd4b3297 / 57c70a99, placed after `contentType`). `objectName="leads"`, `urlPath=""`, `httpMethod="POST"` and base path `gb-cg-leads/v1` unchanged. Description updated. C3 not changed.
- **C1 v3** (revision 8 structure, process design steps 1 to 6):
  - Start -> S1 "Check JSON body" -> Decision "Body is valid JSON?", outside every Try/Catch. S1 script unchanged.
  - True -> TC-A "TC-A Technical error" (retry 0, catch all) -> try: TC-T "TC-T Kafka send" (**retry 2**, catch all) -> try: C7 produce -> "Response 202" -> Message "Accepted" -> Return Documents "Accepted". TC-T catch -> new **Exception "Kafka send failed"** (stopsingledoc true, message `Kafka send to gb-cg.q.leads.in.insert failed after 3 attempts: {1}`, {1} = Meta "Base - Try/Catch Message").
  - TC-A catch -> BR-A (2 branches). Branch 1: "Set facade inputs" -> Process Call C9 (wait true, abort true, no return paths). Branch 2: "Response 500" (`outstatuscode` 500 and `DDP_ERROR_MESSAGE` = Meta "Base - Try/Catch Message") -> new Data Process **S2 "Build error response"** (Groovy 2.4, `groovy.json.JsonOutput.toJson([status: "error", message: <DDP_ERROR_MESSAGE or "">])`, document properties kept) -> Return Documents "Error".
  - False -> TC-F "TC-F Functional" (retry 0) -> try: Exception "Functional error" (unchanged). TC-F catch -> BR-F (2 branches). Branch 1: "Set facade inputs" -> Process Call C9 (wait true, abort true). Branch 2: "Response 400" -> Message "Rejected" -> Return Documents "Rejected - functional error" (unchanged).
  - Both "Set facade inputs" steps (renamed from "Set DDP_MED_NS_Msg"), in table order: FI-1 `DDP_MED_NS_Msg` = Meta "Base - Try/Catch Message"; FI-2 to FI-8 DPPs `DPP_MED_ProcessId` = Execution property `Process Id`, `DPP_MED_ProcessName` = `Process Name`, `DPP_MED_ExecutionId` = `Execution Id`, `DPP_MED_AccountId` = `Account Id`, `DPP_MED_AtomId` = `Atom Id`, `DPP_MED_AtomName` = `Atom Name`, `DPP_MED_ContainerId` = `Atom Id` (`valueType="execution"`). FI-9 to FI-15 are not set.
  - Removed: the C8 connector step, "Response 202 (parked)", "Accepted (parked)", Return Documents "Accepted - parked on retry topic", and Message "Error". C1 no longer references C8 (be398af2).
  - `processOverrides` unchanged (9-field c85b494e block with xpath, copied from 1b208fa6 in Attempt 4). No OperationOverride. Description "spec rev 6" -> "spec rev 8".
- Final C1 v3 shape counts (pulled XML): catcherrors 3 (retry 0 / 2 / 0), branch 2, processcall 2 (both `wait="true" abort="true"`), returndocuments 3, exception 2, decision 1, dataprocess 2, connectoraction 1 (C7), message 2, documentproperties 5, start 1, **notify 0**. `workload="bridge"`, `allowSimultaneous="true"`. Every shape except Start has an inbound connection; no dangling or unset dragpoint; no step has two inbound outcomes from one shape. These match the spec's shape count summary.

## Decisions

| # | Decision | Reason |
|---|----------|--------|
| 1 | New shape names `shape28` (Exception "Kafka send failed") and `shape29` (S2) instead of reusing the removed shapes' names | Avoids an existing shape name changing type; shape names are identifiers only |
| 2 | The D5 positive call (sample lead to `/leads`) was also the single D8 happy-path re-run | D8 allows one re-run and D5 needs the same request; a second call would only add another produce |
| 3 | Base-path recheck covered all 105 API Service components, including the 34 that share a name with another component (pulled one by one into `active-development/webservice-dupcheck/`) | The name-keyed local folder holds only 87 unique names. Only C2 uses `gb-cg-leads/v1`; `gb-cg-leads/v2` is unused |
| 4 | Stopped after one happy-path run, one negative route run and one functional-error run; no volume, tracking or other tests run | D8: "Do not run the happy path again". The happy-path defect blocks the rest |
| 5 | Deployments left in place in 1-DEV (C1 v3, C2 v2) | Needed for the re-test after the design answer. Effect in the meantime: a valid lead is published and the caller gets HTTP 200 with an empty body |

## Deviations from spec

None. The blocking item below is a spec defect, not a build deviation; nothing was redesigned.

## Deployments

| Date | Environment | Classification | Component | Package ID | Notes |
|------|-------------|----------------|-----------|------------|-------|
| 2026-10-09 | 1-DEV (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264) | development (user-confirmed; `--list-environments` lists it, BOOMI_ENVIRONMENT_ID equals it) | C1 135044a4 v3 | c2d1fa6b-000f-480c-b070-feb6310bb39b | Bridge mode. Replaces 7d8121d2 (C1 v2). Bundles C7 v3 and C9 v1; C8 no longer bundled |
| 2026-10-09 | 1-DEV | development | C2 4c878feb v2 | 6a013563-d2e8-4ca6-a0f9-ff5b55986ce0 | Deployed after C1. Replaces d2229e66 (C2 v1) |

The tool returns package IDs, not deployment IDs. No production environment was touched. No extension value was set.

## Developer checks (Attempt 7)

| Check | Result | Evidence |
|-------|--------|----------|
| D0 | PASS | Above |
| D1 Environment | PASS | 1-DEV only |
| D3 Reused connection | PASS | C4 not edited or pushed |
| D4 Facade runtime | **PASS** | TC-10 malformed JSON, execution-c147f75b-6ae1-4b5a-92ac-eaa056290361-2026.10.09 (COMPLETE). Log: TC-F -> Exception "Functional error" -> TC-F error path -> BR-F -> "Set facade inputs" -> facade -> Process Route "CACHE_NOTIFICATION" -> route target `[MED] (sub) CACHE Notification` ... **"Document Cache Load: Shape executed successfully in 33 ms"** -> route target "completed normally" -> "Response 400" -> "Rejected" -> Return Documents "Rejected - functional error". Caller: HTTP 400 `{"status":"rejected","message":"Functional error: request body is not valid JSON"}` in 0.95 s. The `DPP_MED_ProcessId` error from 22c61363 is gone |
| D5 API route, exact `/leads` | **PASS (v1)** | `exactMatch="true"` under `gb-cg-leads/v1`. POST `/ws/rest/gb-cg-leads/v1/leads` (15:47:35Z) started C1: execution-8bee26c5-6b6c-46de-9108-223d0e90e172-2026.10.09. POST `/ws/rest/gb-cg-leads/v1/leads/leads` (15:48:31Z, TC-03 payload) returned **HTTP 404** "Unknown operation for the given URL path." and created **no C1 execution** (the only C1 executions since the deploy are 8bee26c5 at 15:47:36Z and c147f75b at 15:48:35Z). Final endpoint: `https://shv-energy-test.boomi.cloud/ws/rest/gb-cg-leads/v1/leads`. Evidence for the setting: help.boomi.com "Adding a REST endpoint to an API service component" ("Match the exact endpoint"); account API Services fd4b3297 and 57c70a99 |
| Base path uniqueness | PASS | Rechecked over all 105 API Service components just before deploying: only C2 uses `gb-cg-leads/v1` |
| D6.6 Extensions | PASS | sha256 of the 1-DEV c85b494e extension entry (jq-extracted, values not displayed) 89488fd6...ef33 before the C1 push/deploy and after; unchanged. Field ids present: the 9 declared fields plus the 8 that other deployed processes declare. `set` not run |
| D7 Producer settings | PASS | C7 v3: `acks` `all`, `operation_timeout` `3000`, `client_id` `gb-cg.leads`, `compression_type` `snappy`. Runtime: the first produce with `acks=all` **succeeded** (336 ms, 8bee26c5) |
| D8 Happy path | **FAIL (spec defect)** | execution-8bee26c5 (COMPLETE, about 0.3 s in C1; client 1.28 s). Log: Start -> Check JSON body -> Decision True -> TC-A -> TC-T -> "Produce gb-cg.q.leads.in.insert: Shape executed successfully in 336 ms." then **"No documents found. Skipping execution for the Response 202 step."** Neither "Accepted" nor Return Documents "Accepted" ran. Caller received **HTTP 200 with an empty body**, not 202 `{"status":"accepted"}`. The produce succeeded, so the lead is expected on `gb-cg.q.leads.in.insert` (Boomi side only; no Kafka read access). One C7 attempt, no retry, no exception, no facade, no C8 |
| V1 (TC-T) | Review only | User test decision (row 16). Structure: the TC-T catch path (Exception "Kafka send failed") sits inside the TC-A try path |
| V3 HTTP status (`outstatuscode`) | PARTIAL | 400 confirmed at runtime (c147f75b). 202 not confirmed (D8 defect). 500 review only |
| V5 | PASS (BR-F) | The 400 body holds the exception text "Functional error: request body is not valid JSON" read from the Try/Catch message on BR-F branch 2 |
| V6 (BR-F) | PASS | Log order in c147f75b: facade (branch 1) completes, then branch 2 "Response 400" -> "Rejected" -> Return Documents; the HTTP body is only the branch 2 document. BR-A review only (F3) |
| V7 | PASS (setting) | Both Process Calls `wait="true" abort="true"`, no Try/Catch around them. Facade failure not forced |
| V8 | PASS (review) | S2 uses `groovy.json.JsonOutput.toJson`; no string concatenation. No natural 500 occurred |
| TC-A placement (R8) | PASS | XML: Start -> S1 -> Decision; True -> TC-A; False -> TC-F. Runtime: c147f75b has no TC-A or BR-A line |
| 0 Notify shapes | PASS | Pulled C1 v3: 0 `shapetype="notify"` |
| Kafka failure path, TC-15, facade failure | Not run | User test decisions |

## Blocking item

**The Kafka Produce step emits no output document, so the valid-body path cannot return 202 as the spec designs it.** Spec process design step 4.2 to 4.5 places "Response 202" -> Message "Accepted" -> Return Documents "Accepted" after the C7 produce on the TC-T try path. In execution 8bee26c5 the produce succeeded (336 ms) and the runtime logged "No documents found. Skipping execution for the Response 202 step." The process then completed normally, and the API consumer received HTTP 200 with an empty body (the runtime default for a listener with no returned document), not 202 `{"status":"accepted"}`. C7 has `responseProfileType="none"`; spec D7 forbids any other C7 change, and no source tells the developer which setting (if any) makes a Kafka Produce pass its input document on. The developer did not redesign the path. The designer needs to decide how the 202 response is produced after a successful send (for example a step layout that does not depend on C7 output, or a C7 setting proven by documentation or an account precedent), then the user re-approves. Until then the deployed C1 v3 publishes a valid lead and answers 200 with no body.

## Temporary Notify shapes

None added. C1 v3 has 0 Notify shapes.
