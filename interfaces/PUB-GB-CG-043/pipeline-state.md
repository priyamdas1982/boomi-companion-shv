# Pipeline state: PUB-GB-CG-043

Written only by the `/build-interface` orchestrator.

- Step: PAUSED by user (2026-10-08). Next: step 4 - developer fix mode for round 1 findings F-1-01, F-1-02, F-1-03 against approved revision 6. Fix run was stopped before any push (C1, C7, C8 still version 1). Then round 1 re-review and test execution; tests need SERVER_USERNAME and SERVER_TOKEN set in the environment.
- Round: 1 / 3
- Spec approved: yes (user: "yes, I approve revision 6")
- Spec approved on: 2026-10-08 (revision 6; earlier approvals superseded)
- Spec hash: 9bcb1e480fb9e77fa301ce599a14df9f3cfedf46dca32e0a67fe7c5d90a4cf5a

## Components

| Name | Type | Component ID | Version |
|------|------|--------------|---------|
| [Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG] | process | 135044a4-ad21-4ba0-b4d7-5e5c21fac446 | 1 |
| PUB-GB-CG-043 Lead API | webservice | 4c878feb-2bc3-42f1-9ef5-06cea4a18529 | 1 |
| PUB-GB-CG-043 WSS Listen Lead | connector-action (wss) | 0f214069-c48d-4633-b60d-189e21dec918 | 1 |
| PUB-GB-CG-043 Lead Request JSON | profile.json | 27f55bec-bae3-4465-87cc-ad9a8944e71d | 1 |
| PUB-GB-CG-043 Lead Response JSON | profile.json | f07edecd-68d1-4aeb-acd1-e1b5fc28cb96 | 1 |
| PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.insert | connector-action (kafka) | 583b0437-f8fc-4624-bddc-efff3172e49c | 1 |
| PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.retry | connector-action (kafka) | be398af2-5ce6-48b1-b116-ba822ca179f5 | 1 |

## Status

- Open findings: 1 blocker, 0 major, 2 minor (round 1)
- Disputed findings:
- Last test result:

## User rulings

| Finding | Ruling (fix / accept) | Date |
|---------|-----------------------|------|

## Test decisions (user, 2026-10-08)

- TC-15 (unauthenticated call): recorded as "not run" (user: "TC-15 not run is fine").
- Kafka topic contents: no read access will be given (user: "no Kafka read access"). Message count, body, headers and key are verified on the Boomi side only (process log and Process Reporting) and reported as "partly verified (Boomi side only)".
- Technical-error and retry-send-failure paths: review only (spec revision 5, user: "C, review only for now").
