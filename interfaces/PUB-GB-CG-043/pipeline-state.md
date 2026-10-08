# Pipeline state: PUB-GB-CG-043

Written only by the `/build-interface` orchestrator.

- Step: Design feedback loop (round 1 findings F-1-01, F-1-02, F-1-03 -> designer revision 6)
- Round: 1 / 3
- Spec approved: yes (user: "yes, I approve revision 5")
- Spec approved on: 2026-10-08 (revision 5; earlier approvals superseded)
- Spec hash: e163319eb14898d5f28a5ceedd3a3f991c5b7ba579f0af7674067352d1138899

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
