# Pipeline state: PUB-GB-CG-043

Written only by the `/build-interface` orchestrator.

- Step: 3/5 - round 3: reviewer and tester (re-mark and re-run TC-08, TC-09, TC-11, TC-12, TC-23) against spec revision 11 (wording only, no component change).
- Round: 3 / 3
- Spec approved: yes (revision 11, wording only; under the user's 2026-10-12 instruction "can you do this or not? Use all the boomi practoces and finish this")
- Spec approved on: 2026-10-12 (revision 11; earlier approvals superseded)
- Spec hash: 3984711dde544ab3e30a667b4e165991366697ed64cadef2f51e46c49094d113
- Kafka topics confirmed: `gb-cg.q.leads.in.insert` and `gb-cg.q.leads.in.retry` (user, 2026-10-09: "I have just created gb-cg.q.leads.in.retry and gb-cg.q.leads.in.insert in confluent")

## Components

| Name | Type | Component ID | Version |
|------|------|--------------|---------|
| [Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG] | process | 135044a4-ad21-4ba0-b4d7-5e5c21fac446 | 4 |
| PUB-GB-CG-043 Lead API | webservice | 4c878feb-2bc3-42f1-9ef5-06cea4a18529 | 2 |
| PUB-GB-CG-043 WSS Listen Lead | connector-action (wss) | 0f214069-c48d-4633-b60d-189e21dec918 | 1 |
| PUB-GB-CG-043 Lead Request JSON | profile.json | 27f55bec-bae3-4465-87cc-ad9a8944e71d | 1 |
| PUB-GB-CG-043 Lead Response JSON | profile.json | f07edecd-68d1-4aeb-acd1-e1b5fc28cb96 | 1 |
| PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.insert | connector-action (kafka) | 583b0437-f8fc-4624-bddc-efff3172e49c | 3 |
| PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.retry | connector-action (kafka) | be398af2-5ce6-48b1-b116-ba822ca179f5 | 2 |

## Status

- Open findings: 0 blocker, 0 major, 1 minor (F-2-01, spec wording; round 2). F-1R-01, F-1R-02 closed. D-1-01 closed by user decision (row 31).
- Disputed findings: none
- Last test result: round 2 (2026-10-12): 10 PASS, 4 FAIL (TC-08, TC-09, TC-11, TC-12: D-2-01 minor, spec says empty body, runtime returns default HTML error page with the error reason), 3 NOT RUN (TC-13, TC-14, TC-15), 10 PARTLY VERIFIED. No temporary Notify.

## User rulings

| Finding | Ruling (fix / accept) | Date |
|---------|-----------------------|------|

## Test decisions (user, 2026-10-08)

- TC-15 (unauthenticated call): recorded as "not run" (user: "TC-15 not run is fine").
- Kafka topic contents: no read access will be given (user: "no Kafka read access"). Message count, body, headers and key are verified on the Boomi side only (process log and Process Reporting) and reported as "partly verified (Boomi side only)".
- Technical-error and retry-send-failure paths: review only (spec revision 5, user: "C, review only for now").

## User answers to developer BLOCKED (2026-10-09, verbatim)

1. "I have just created gb-cg.q.leads.in.retry and gb-cg.q.leads.in.insert in confluent."
2. (facade inputs) "set whatever needs to be set and available to you."
3. (retries vs runtime limit) "kafka outage should give an error back."
4. (/leads/leads reaches C1) "b" (defect: designer changes the route).
Standing rules added at the user's request ("set those rules forever"): Kafka topics confirmed by the user before any build; developer runs connectivity checks first (CLAUDE.md, build-interface skill, developer role).

## User redesign instruction (2026-10-09, verbatim)

Q1 follow-up: "kafka failure is rarity."
Then: "redesign, also change in design rules: if kafka fails, try 3 times. throw exception. return exception to api consumer.  handled or unhandled."
Added to CLAUDE.md as the standing rule "Kafka send failures". Relayed to the designer for revision 7.
Further answers (2026-10-09, verbatim): "2. keep existing logic of 3 retries. 3. i don't know, find a way that my api path is /leads. if it is already taken up, make v2. 4. a" (2 = TC-T retry count, 3 = /leads/leads route, 4 = DDP_MED_NS_Level leave unset). Relayed to the designer. Questions 5 to 10 still open.
Answers to revision 7 second-pass questions (2026-10-09, verbatim): "1a 2a 3-8: a" (Q1 a: 3 attempts in total, 1 send + 2 retries, Kafka timeout 3 s; Q2 a: return the full exception text; Q3-Q8 a: leave DDP_MED_NS_Code, DPP_MED_Environment, DPP_MED_Environment_Class, DPP_MED_APIURL, DPP_MED_TrackingId, DPP_MED_TrackedFields unset). Relayed to the designer.
User decision on V7 (2026-10-09, verbatim): "if facade fails, throw an exception. unhandled." Relayed to the designer with the developer's D5 evidence (exactMatch route option) for revision 8.
Answer to revision 8 question 1 (2026-10-09, verbatim): "b" (move TC-A so it wraps only the valid-body path; facade failure on BR-F fails the execution unhandled). Relayed to the designer.
Answer to revision 10 Q1 (2026-10-12, verbatim): "email is mandatory. So, keep it on both" (option b: tracking field email on C3 and C7). Relayed to the designer.
User instruction (2026-10-12, verbatim): "can you do this or not? Use all the boomi practoces and finish this". Taken as: Q2 answered with the designer's recommended option a (no email validation; email mandatory only as the tracking field, matching the design document's scope 1.2.1), and authorisation to finalise revision 10 and run the pipeline to the end without further questions unless a blocker needs the user.
