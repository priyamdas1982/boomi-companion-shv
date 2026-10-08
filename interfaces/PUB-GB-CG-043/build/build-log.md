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
