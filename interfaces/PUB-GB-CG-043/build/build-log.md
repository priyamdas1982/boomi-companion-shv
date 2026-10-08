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
