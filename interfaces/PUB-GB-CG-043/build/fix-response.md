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
