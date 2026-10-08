# Design spec: PUB-GB-CG-043

Status: DRAFT - OPEN QUESTIONS

Revision 2. This revision includes the user's answers to the 19 questions in revision 1 and to follow-up questions A to D (relayed by the orchestrator).

## Requirements

Source: the user-supplied interface design document "PUB-GB-CG-043-Web_To_Lead_Publisher_V0.1.docx"
(author A. Koyyada, version 1, 21/09/2026), converted text at
`interfaces/PUB-GB-CG-043/design/source/requirements.md`, plus the user's answers quoted below.

Scope of this spec: **the Publisher only (PUB-GB-CG-043).**

- Sitecore submits selected web forms (web-to-lead) as a JSON request through Azure APIM, in real time
  and event driven. APIM calls the Boomi REST endpoint, which is published by a Boomi API Service component (user, follow-up D: "Boomi API Service component").
- Boomi publishes the request body **unchanged** to the Kafka topic `gb-cg.q.leads.in.insert` (document section 1.3.2; user Q12: "unchanged").
- Every published Kafka message carries the header `Retry-Count` with value `0` (user Q13: "header as 'Retry-COunt': 0 (we will use it later in retry mechanism, not for now)"). There is no message key: the user asked for the header only.
- Errors (user Q8: "3 retry on all technical errors. No retry on functional error. Must be send to a retry kakfa topic. If tech retries expire after 3 times, also send to retry topic."):
  - Functional error: no retry. Send to the retry topic `gb-cg.q.leads.in.retry` (user, follow-up B: "Nice name.").
  - Technical error: 3 retries, then send to the retry topic.
- The facade `[MED] (sub) CACHE Notification Facade` is called, with `DDP_MED_NS_Msg` set to the Try/Catch message, for functional errors and when the retry-topic send fails. It is not called on success, and not for a technical error that was parked on the retry topic (user, follow-up C: "the Try/Catch message in DDP_MED_NS_Msg should contain the functional error and if (very rarely) send to retry topic also fail. Sitecore should get 202").
- Downstream consumer (out of scope, separate interface): SUB-GB-CG-043 reads `gb-cg.q.leads.in.insert` and creates the Lead in Salesforce. `[SF_Connector]` belongs to that interface.
- Business criticality: Medium. The data has customer fields and is sensitive.
- NFRs: API response time 5 s (max 5 s); about 60 calls per day, peak 75 per day, average 525 per week.
- Data validation is outside integration scope (document section 1.2.1). The only "functional" check is that the body is present and is a JSON object (see Error handling).
- Build account: `shvenergynv-6R344K` (user Q6). Build, deploy and test in a development or test environment only, never production (CLAUDE.md). The orchestrator reports that the test runtime (`shv-energy-test.boomi.cloud`) has apiType `advanced`. That is why the endpoint is an API Service component and not a bare WSS listener.

## Required values

| # | Value | Answer | Source |
|---|-------|--------|--------|
| 1 | Interface type | Publisher (Web Services Server start, published by an API Service component, publishes to a Kafka topic) | user: design document "Interface Design and Specification (Publisher)" and process name "[Publisher]-[PUB-GB-CG-043]-..."; user Q5: "you have correctly suggested"; CLAUDE.md: Interface type (Publisher) |
| 2 | Integration ID sequence number (YYY) | 043 | user: design document interface ID "PUB-GB-CG-043" |
| 3 | Integration ID | PUB-GB-CG-043 (`PUB` = Publisher, `GB-CG` = Calor Group Limited, `043`). Equals the orchestrator folder ID. | CLAUDE.md: Integration ID, BU-SHORT codes; user: design document |
| 4 | Main atomic object | Lead | user Q1: "Lead" |
| 5a | Source application | Customer Portal | user Q2: "Customer Portal" |
| 5b | Source BU | GB-CG | user: design document "Business Units and Applications" table (Calor GB, GB-CG) and process names in section 1.3.2 |
| 6a | Target application | Not required for this interface type (Publisher) and not used | CLAUDE.md: Interface type (Publisher: Source application and Source BU mandatory) |
| 6b | Target BU | Not required for this interface type (Publisher) and not used | CLAUDE.md: Interface type (Publisher) |
| 7 | Project type | Enterprise Projects | user Q3: "Enterprise Projects" |
| 8 | Application name | Customer Portal (see deviation note below) | user, follow-up A: "Customer Portal" |
| 9 | Tracking field(s) | `email` (request profile element `email`). Used on the WSS listen operation and on both Kafka produce operations (main topic and retry topic). | user Q7: "email" |
| 10 | Full process name | `[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]` | CLAUDE.md: Process naming convention (Publisher segments); values from rows 1, 3, 4, 5a, 5b |
| 11 | Full folder path | `Calor Group Limited/02-Deployable/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead` | CLAUDE.md: Folder path convention (from `GB-CG` down); user Q5: "you have correctly suggested" (root "Calor Group Limited/02-Deployable/", leaf "PUB-GB-CG-043-Lead") |

Source is one of: `user: "<answer>"`, `CLAUDE.md: <section>`, or `OPEN`.

Notes:

- The Publisher pattern has exactly five segments: interface type, integration ID, main atomic object, source application, source BU. No target segments are added.
- **Deviation from the CLAUDE.md hint (user's explicit choice).** CLAUDE.md says that for Enterprise Projects the APPLICATION-NAME level is the target application (for example PDI, RNA, Paragon, OBTC). For this interface the user explicitly chose "Customer Portal" (follow-up A), which is the source application. This is recorded as the user's decision, not a derived value.
- Folder tree, as it appears in the account `shvenergynv-6R344K`:

      Calor Group Limited
        02-Deployable
          GB-CG
            Enterprise Projects
              Customer Portal
                Publisher
                  PUB-GB-CG-043-Lead

## Components

All new components go into the interface folder (row 11) unless stated otherwise. The names below are proposals and are confirmed when the spec is approved. Only the process name is governed by the CLAUDE.md naming convention.

| # | Component | Type | New / reuse | Location | Notes |
|---|-----------|------|-------------|----------|-------|
| C1 | `[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]` | Process | New | Interface folder | Listen process. Process Mode `bridge`, allow simultaneous executions |
| C2 | `PUB-GB-CG-043 Lead API` | API Service component (`webservice`), REST | New | Interface folder | One REST route, POST, resource path `leads`, linked to C1. Base API path: OPEN (question 1) |
| C3 | `PUB-GB-CG-043 WSS Listen Lead` | Web Services Server operation (`wss`), Listen | New | Interface folder | Object/operation name `leads`. Input: single JSON document (C5). Output: single JSON document (C6). Tracked field `email` |
| C4 | `[Confluent_Kafka]` | Kafka connection | Reuse unchanged (user Q14: "yes always reuse") | `Calor Group Limited/00-ConnectionResources/00-Connections` | Not edited. All its settings are declared extensible on process C1 (see Connectors) |
| C5 | `PUB-GB-CG-043 Lead Request JSON` | JSON profile | New | Interface folder | Built from the corrected sample (see `mapping.md`). Field `additional-comments` (user Q11) |
| C6 | `PUB-GB-CG-043 Lead Response JSON` | JSON profile | New | Interface folder | `{"status": "...", "message": "..."}` (see `mapping.md`) |
| C7 | `PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.insert` | Kafka operation, Produce | New (user Q15: "new opretaion. always") | Interface folder | Topic `gb-cg.q.leads.in.insert`. Tracked field `email` |
| C8 | `PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.retry` | Kafka operation, Produce | New (user Q15; follow-up B) | Interface folder | Topic `gb-cg.q.leads.in.retry`. Tracked field `email` |
| C9 | `[MED] (sub) CACHE Notification Facade` | Process (subprocess) | Reuse (user Q16: "reuse, always") | `SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/00-SharedLibrary_v4/00-Version_4.0 (2019-12-28-baseline)/01-Facade/02-Process` | Called by Process Call, Wait for process to complete = true |

Topics:

| Topic | Use | Source |
|-------|-----|--------|
| `gb-cg.q.leads.in.insert` | Main topic; every accepted lead | user: design document section 1.3.2 |
| `gb-cg.q.leads.in.retry` | Parking topic for functional errors and for technical errors after 3 retries | user, follow-up B: "Nice name." |

Prerequisite (not a design decision): both topics must exist in the development/test Confluent cluster that `[Confluent_Kafka]` points to in the target environment. Boomi cannot create Confluent topics. If a topic is missing, the developer or tester stops and reports it to the orchestrator.

## Process design

Start shape: Web Services Server listen, using operation C3, exposed through API Service component C2.

Main path (labels TC-A, TC-T and TC-F are the three Try/Catch shapes):

1. **Start** (WSS listen, C3).
2. **TC-A** Try/Catch "Retry-topic send failure", retry count 0, catch All errors. Try path continues with step 3.
3. **Set Properties "Set Kafka header"**: sets the Kafka message header `Retry-Count` = `0` (static) as a document property that the Kafka connector writes as a message header. It is set here, before TC-T and TC-F, so the property travels on the document into both catch paths.
4. **Data Process, Custom Scripting "Check JSON body"** (script S1): sets `DDP_VALIDATION_ERROR`. The document is passed through unchanged.
5. **Decision "Body is valid JSON?"**: `DDP_VALIDATION_ERROR` equals empty.
   - **True (valid)**: go to 6.
   - **False (functional error)**: go to 7.
6. Valid path:
   1. **TC-T** Try/Catch "Technical", **retry count 3**, catch All errors.
   2. Try: **Kafka Produce** (C4 + C7, topic `gb-cg.q.leads.in.insert`), body unchanged, header `Retry-Count: 0`.
   3. **Set Properties "Response 202"**: HTTP response status code 202.
   4. **Message "Accepted"**: `{"status":"accepted"}`.
   5. **Return Documents "Accepted"**.
   6. TC-T Catch (all 3 retries failed): **Kafka Produce** (C4 + C8, topic `gb-cg.q.leads.in.retry`), original body unchanged, header `Retry-Count: 0`.
   7. **Set Properties "Response 202 (parked)"**: HTTP status 202.
   8. **Message "Accepted (parked)"**: `{"status":"accepted"}`.
   9. **Return Documents "Accepted - parked on retry topic"**.
7. Functional-error path:
   1. **TC-F** Try/Catch "Functional", retry count 0, catch All errors.
   2. Try: **Exception step "Functional error"** (stop single document = true), message = `DDP_VALIDATION_ERROR`. TC-F catches it, so the Try/Catch message holds the functional error.
   3. TC-F Catch: **Set Properties "Set DDP_MED_NS_Msg"**: `DDP_MED_NS_Msg` = Try/Catch message (Meta information > Base > Try/Catch Message).
   4. **Process Call** `[MED] (sub) CACHE Notification Facade` (C9), wait = true.
   5. **Kafka Produce** (C4 + C8, topic `gb-cg.q.leads.in.retry`), original body unchanged, header `Retry-Count: 0`.
   6. **Set Properties "Response 400"**: HTTP status 400.
   7. **Message "Rejected"**: `{"status":"rejected","message":"<DDP_MED_NS_Msg>"}`.
   8. **Return Documents "Rejected - functional error"**.
8. TC-A Catch (an error in the TC-T or TC-F catch path, in practice a failed send to the retry topic):
   1. **Set Properties "Set DDP_MED_NS_Msg"**: `DDP_MED_NS_Msg` = Try/Catch message.
   2. **Process Call** `[MED] (sub) CACHE Notification Facade` (C9), wait = true.
   3. **Set Properties "Response 500"**: HTTP status 500.
   4. **Message "Error"**: `{"status":"error","message":"Technical error. The lead was not accepted."}` (a fixed text, so that no sensitive data or connection detail is returned).
   5. **Return Documents "Error"**.

Each outcome ends in its own Return Documents shape. No two outcomes converge on one step, and there are no Notify shapes.

Developer verification items (behaviour that is not documented in the local skill references):

- **V1.** An error raised on the Catch path of an inner Try/Catch (TC-T or TC-F) must be caught by the enclosing TC-A. Verify this in development/test. If the platform does not behave this way, the design would need a fourth Try/Catch. Do not add one; stop and return to the orchestrator (CLAUDE.md: Error handling).
- **V2.** Kafka message header: the local skill has no Kafka connector reference. Use the Kafka connector's own mechanism for custom message headers (a document property or an operation header setting), following `references/guides/problem_solving_guide.md`. The header name must be exactly `Retry-Count` and the value `0`.
- **V3.** HTTP response status: set it with the Web Services Server response status-code document property (Set Properties, Connector properties, Web Services Server). This is not documented locally; confirm the exact property against Boomi documentation.

### HTTP response per outcome

| Outcome | Kafka result | Facade called | HTTP status | Response body |
|---------|--------------|---------------|-------------|---------------|
| Valid body, main topic send succeeds (first try or within 3 retries) | Message on `gb-cg.q.leads.in.insert` | No | 202 | `{"status":"accepted"}` |
| Valid body, main topic fails 1 + 3 times, retry topic send succeeds | Message on `gb-cg.q.leads.in.retry` | No | 202 | `{"status":"accepted"}` |
| Functional error (body missing, empty, not valid JSON, or not a JSON object), retry topic send succeeds | Message on `gb-cg.q.leads.in.retry` | Yes, `DDP_MED_NS_Msg` = functional error | 400 | `{"status":"rejected","message":"<functional error>"}` |
| Retry topic send fails (after a technical or a functional error) | None (on the functional path the facade has already run once) | Yes, `DDP_MED_NS_Msg` = retry-send error | 500 | `{"status":"error","message":"Technical error. The lead was not accepted."}` |
| Not authenticated | Not reached (enforced by APIM / the API Service runtime before the process runs) | No | 401 (runtime) | Runtime default |

Sources: 202 and the `{"status":"accepted"}` body, 500 with an error message, and 400 allowed come from user Q9 ("Yes, all 3 are acceptable solution"). 202 after parking a technical failure comes from follow-up C ("Sitecore should get 202"). 400 for a functional error comes from the orchestrator's follow-up C proposal ("Sitecore 400"), which the user did not change. 500 for a retry-send failure follows Q9 "failure 500".

### Target

Kafka topic `gb-cg.q.leads.in.insert` (main) and `gb-cg.q.leads.in.retry` (parking), through the existing `[Confluent_Kafka]` connection.

### Deployment mode

`bridge` (process option Process Mode = Bridge, `workload="bridge"`). Source: CLAUDE.md: SHV Energy build rules, Deployment mode (Web Services Server start). Allow simultaneous executions = true (listener). Deploy C1 and C2 to the development/test environment of account `shvenergynv-6R344K` only.

### Endpoint and authentication

- API Service component C2 (type `webservice`, REST), one route: POST, resource path `leads`, linked to process C1 (operation C3).
- Effective URL: `<runtime url>/ws/rest/<base API path>/leads`. The base API path is open question 1.
- Authentication is whatever the API Service component and the advanced runtime already enforce (user, follow-up D). This spec contains no credentials. APIM's backend URL must point at the effective URL.

## Error handling

Three Try/Catch shapes: the CLAUDE.md maximum, not more.

| Try/Catch | Retry count | Wraps | Catch path |
|-----------|-------------|-------|------------|
| TC-A "Retry-topic send failure" | 0 | Everything after Start | `DDP_MED_NS_Msg` = Try/Catch message -> facade -> HTTP 500 -> Return Documents "Error" |
| TC-T "Technical" | 3 (user Q8) | Main topic produce and the 202 response | Produce to the retry topic -> HTTP 202 -> Return Documents "Accepted - parked on retry topic" |
| TC-F "Functional" | 0 (user Q8: "No retry on functional error") | Exception step raising the functional error | `DDP_MED_NS_Msg` = Try/Catch message (functional error) -> facade -> produce to the retry topic -> HTTP 400 -> Return Documents "Rejected" |

Definitions:

- **Functional error**: the request body is missing or empty, is not valid JSON, or is not a JSON object. No other content validation is done (validation is out of scope per the document). This is the orchestrator's follow-up C definition, and the user did not change it.
- **Technical error**: any error on the TC-T try path, in practice a Kafka produce failure on the main topic.

Retries in TC-T run immediately, with no back-off (skill reference `try_catch_step.md`), so 3 retries do not add a fixed delay. Each Kafka attempt still adds its own connect/timeout time against the 5 s maximum response time.

## Cache Notification Facade

- Called from two places, each preceded by a Set Properties step that sets `DDP_MED_NS_Msg` to Meta information "Try/Catch Message":
  1. TC-F Catch path, before the send to the retry topic: the message is the functional error.
  2. TC-A Catch path: the message is the retry-topic send failure.
- Not called on the success path and not on the TC-T Catch path (user, follow-up C).
- Facade: `[MED] (sub) CACHE Notification Facade` at `SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/00-SharedLibrary_v4/00-Version_4.0 (2019-12-28-baseline)/01-Facade/02-Process` (CLAUDE.md; user Q16: "reuse, always"). Process Call with Wait for process to complete = true. The parent C1 must be redeployed if the facade changes.

## Connectors

| Connection / operation | Purpose | Extensible settings | Tracking field |
|------------------------|---------|---------------------|----------------|
| C3 WSS listen operation | Receive the Sitecore lead JSON | No connection component. Every operation field the platform allows to be extended is extended (CLAUDE.md: Connector extensions). The object name and profiles are the API contract. | `email` |
| C4 `[Confluent_Kafka]` (reused, not edited) | Kafka (Confluent) connection, SASL_SSL / PLAIN | All connection settings are declared in C1's process extensions (`processOverrides`): bootstrap servers, security protocol, SASL mechanism, username/client principal, password and every other connection field. Values are set per environment through Environment Extensions and are never written into XML or this spec. Because the extension declaration lives on the process, the shared connection is not modified. | n/a |
| C7 Kafka Produce, main | Publish to `gb-cg.q.leads.in.insert` | Topic name and every other extensible operation property | `email` |
| C8 Kafka Produce, retry | Publish to `gb-cg.q.leads.in.retry` | Topic name and every other extensible operation property | `email` |
| `[SF_Connector]` | Not used. It belongs to SUB-GB-CG-043. | n/a | n/a |

Message key: none. Message header: `Retry-Count: 0` on every message, on both topics.

## Scripts

| Script | Single purpose |
|--------|----------------|
| S1 "Check JSON body" (Groovy, Data Process Custom Scripting) | For each document: read the body. If it is empty or whitespace, set `DDP_VALIDATION_ERROR` = `Functional error: request body is empty`. Otherwise parse it with `JsonSlurper`. If parsing fails, set `Functional error: request body is not valid JSON`. If the result is not a JSON object, set `Functional error: request body is not a JSON object`. Otherwise set it empty. The script never throws, and it passes the document through unchanged. |

No other scripting. Headers, status codes and response bodies use Set Properties and Message steps. Message step JSON uses the single-quote escaping rule (skill Issue #1).

## Test notes

All tests run in development/test of account `shvenergynv-6R344K` only.

| Requirement | Observable behaviour to check |
|-------------|-------------------------------|
| Naming and folder | The process is named exactly `[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]` and is in `Calor Group Limited/02-Deployable/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead`. C2, C3, C5 to C8 are in the same folder. |
| Bridge mode | Process Mode = Bridge (`workload="bridge"`). Deployed to a dev/test environment only. |
| Endpoint | API Service C2 is deployed. POST to `/ws/rest/<base path>/leads` reaches C1. |
| Happy path | POST the valid sample lead JSON (see `mapping.md`). Response 202 `{"status":"accepted"}` within 5 s. Exactly one message is on `gb-cg.q.leads.in.insert`, its body is byte-for-byte the request, it has header `Retry-Count` = `0` and no key. Nothing on the retry topic. The facade is not called. |
| Tracking field | Process Reporting shows tracked field `email` populated on the listen and produce operations. |
| Technical error | In a test environment, set the main topic extension (C7) to a non-existent or unauthorised topic. The process log shows 1 + 3 attempts on the main produce, then one message on `gb-cg.q.leads.in.retry` with the original body and `Retry-Count: 0`. Response 202 `{"status":"accepted"}`. The facade is not called. |
| Functional error | POST an empty body, a malformed JSON body (for example the document's original sample with the missing comma) and a JSON array. Each case: no retry, the facade is called with `DDP_MED_NS_Msg` = the functional error text, one message on the retry topic with the original body, response 400 `{"status":"rejected","message":"Functional error: ..."}`. Nothing on the main topic. |
| Retry-send failure | In a test environment, break both C7 and C8 topics (technical path) and, separately, only C8 (functional path). The facade is called with the retry-send error (on the functional path, after the first facade call with the functional error). Response 500 `{"status":"error","message":"Technical error. The lead was not accepted."}`. This also confirms developer verification item V1. |
| Extensions | `[Confluent_Kafka]` connection fields and the C7/C8 operation fields (including topic) appear under Environment Extensions. No environment-specific value is in component XML. The shared `[Confluent_Kafka]` component version is unchanged. |
| No banned shapes | No Notify shapes. Exactly three Try/Catch shapes (TC-A, TC-T retry 3, TC-F retry 0). |
| Volume | About 10 sequential calls all return 202 and produce 10 messages on the main topic. |

## Open questions

1. API Service base path: which Base API Path should the API Service component `PUB-GB-CG-043 Lead API` use? The route resource is `leads`, so the Boomi URL becomes `/ws/rest/<base path>/leads`, and APIM's backend must be set to this URL. The base path must not duplicate another API already deployed to the same environment. Examples: `gb-cg/sales-and-service-management-api/v1` (mirrors the APIM URL `.../gb-cg/sales-and-service-management-api/v1/leads`), or `gb-cg-leads/v1`. If APIM's backend URL is already fixed, give that URL.
