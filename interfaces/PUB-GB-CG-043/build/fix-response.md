# Fix response: PUB-GB-CG-043

## Round 1

Built against spec revision 6 (hash 9bcb1e480fb9e77fa301ce599a14df9f3cfedf46dca32e0a67fe7c5d90a4cf5a). Details and evidence: `build/build-log.md`, "Attempt 4 / Round 1 fix".

| Finding / defect | Response | Component and new version | Change or reason |
|------------------|----------|---------------------------|------------------|
| F-1-01 (blocker) | FIXED | C1 `[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]` (135044a4-ad21-4ba0-b4d7-5e5c21fac446), version 2; deployed to 1-DEV, package 7d8121d2-647f-493d-a192-8d01219cd7c7 | The 17-field `ConnectionOverride` for c85b494e (no xpath) is replaced with the block copied verbatim from 1b208fa6 (CreateLead, pulled read only): 9 fields, each with `xpath="GenericConnectionConfig/field[@id='<id>']/@value"`. Every copied field exists in C4; the only uncovered C4 field is `consumer_group` (spec row 20). The 1-DEV c85b494e extension entry has the same hash before and after the deploy. No OperationOverride for C7/C8 |
| F-1-02 (minor) | NO CHANGE | C3 0f214069 v1, C7 583b0437 v2, C8 be398af2 v2 (no tracking change) | Spec revision 6 changed only the wording. The built slots already match row 9 on all three operations: `primarykey` (33185) = static `Email`, `primaryvalue` (33186) = C5 27f55bec element 6 `email`. The C7/C8 version change comes from F-1-03, not from tracking |
| F-1-03 (minor) | FIXED | C7 `PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.insert` (583b0437-f8fc-4624-bddc-efff3172e49c) v2; C8 `PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.retry` (be398af2-5ce6-48b1-b116-ba822ca179f5) v2; bundled in C1 package 7d8121d2 | `acks` `1` -> `all` and `operation_timeout` `30000` -> `5000` on both. `client_id` `gb-cg.leads` and `compression_type` `snappy` unchanged. No other field changed. Runtime acceptance of `acks=all` is not yet confirmed (no successful produce; see the build log blocking items) |

## Round 1, revision 7

Status: BLOCKED: connectivity (D0). No revision 7 change was implemented in this run; no component was changed, pushed or deployed. See build-log.md, "Attempt 5 / revision 7". The revision 7 changes (rows 18, 21, 22, 26, 27, 28; Exception "Kafka send failed"; removal of the C8 step; S2; D5 route) are still to be made once the Boomi documentation hosts are reachable.

### Re-run (Attempt 6, 2026-10-09)

Status: BLOCKED: V7 not confirmed by Boomi documentation. D0 passed on all hosts. No component was changed, pushed or deployed, and none of the revision 7 changes is implemented yet. help.boomi.com "Process Call step" says: "Wait for the process to complete. If selected, ... If the subprocess fails, the parent process stops." No source says abort = false lets branch 2 run; see build-log.md "Attempt 6 / revision 7". D5 evidence was gathered for the next round: route attribute `exactMatch="true"` ("Match the exact endpoint"), documented and used by account API Services fd4b3297 and 57c70a99; `gb-cg-leads/v1` is used only by C2 and `gb-cg-leads/v2` is free.

## Round 1, revision 8

Built against spec revision 8 (hash 4e1f32f5e656ec7f26bdc4455947e44804dcbaf201a4b16baf2cdb38cc7dd635). Details and evidence: `build/build-log.md`, "Attempt 7 / revision 8".

Status: **BLOCKED: spec cannot be built as written (D8 happy path).** All revision 8 changes are implemented, pushed and deployed to 1-DEV. The Kafka Produce step outputs no document, so "Response 202", "Accepted" and Return Documents "Accepted" never run after a successful send; the caller gets HTTP 200 with an empty body (execution 8bee26c5). This needs a design decision.

| Finding / item | Response | Component and new version | Change or reason |
|----------------|----------|---------------------------|------------------|
| F-1-01 (blocker) | FIXED (unchanged since Round 1) | C1 135044a4 v3, package c2d1fa6b-000f-480c-b070-feb6310bb39b | 9-field c85b494e block with xpath carried over unchanged; 1-DEV extension entry hash unchanged before and after the deploy |
| F-1-02 (minor) | NO CHANGE | C3 0f214069 v1, C7 583b0437 v3 | Tracking slots `primarykey` = `Email`, `primaryvalue` = `email` unchanged |
| F-1-03 (minor) | FIXED | C7 583b0437 v3 | `operation_timeout` 5000 -> 3000 (spec rows 18, 26); `acks` `all` accepted at runtime (successful produce in 8bee26c5). C8 not changed and no longer used |
| Rev 8: TC-A on the valid-body path only | DONE | C1 v3 | Start -> S1 -> Decision outside every Try/Catch; True -> TC-A -> TC-T; False -> TC-F (runtime: no TC-A in c147f75b) |
| Rev 7/8: TC-T retry 2, Exception "Kafka send failed", no C8 step | DONE | C1 v3, C7 v3 | Retry count 2; TC-T catch path holds only the Exception step; C8 step and the parked-path steps removed; C1 has no reference to C8 |
| Rev 7: facade inputs | DONE | C1 v3 | FI-1 to FI-8 on both "Set facade inputs" steps (execution properties); FI-9 to FI-15 not set. D4 PASS (c147f75b: Document Cache Load succeeds, 400 returned) |
| Rev 7: S2 escaped 500 body | DONE | C1 v3 | "Response 500" sets `DDP_ERROR_MESSAGE`; S2 builds the body with `JsonOutput`; Message "Error" removed |
| Rev 8: facade calls wait = true, abort = true | DONE | C1 v3 | Both Process Calls; no Try/Catch around them |
| Rev 8: C2 exact route (D5) | DONE, PROVEN | C2 4c878feb v2, package 6a013563-d2e8-4ca6-a0f9-ff5b55986ce0 | `exactMatch="true"` under `gb-cg-leads/v1`: `/leads` reached C1 (8bee26c5); `/leads/leads` returned 404 with no C1 execution |
| D8 happy path | BLOCKED | C1 v3 | Produce succeeded (336 ms), then "No documents found. Skipping execution for the Response 202 step."; caller got HTTP 200 with an empty body instead of 202 `{"status":"accepted"}`. Needs the designer (spec process design step 4) |

FIXED: 2 (F-1-01, F-1-03). DISPUTED: 0.
