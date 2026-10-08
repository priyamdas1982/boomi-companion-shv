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
