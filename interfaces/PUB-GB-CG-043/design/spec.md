# Design spec: PUB-GB-CG-043

Status: READY FOR APPROVAL

Revision 4. This revision answers the developer's BLOCKED report on revision 3 (evidence: `interfaces/PUB-GB-CG-043/build/build-log.md`, pre-build checks of 2026-10-08) with the user's decisions, which the orchestrator relayed verbatim: "1. branch fix 2. b 3. a 4. yes, 1-DEV is dev." Everything not listed under "Changes in revision 4" is unchanged from revision 3.

## Changes in revision 4

- **Facade call pattern, "branch fix" (user: "1. branch fix").** The developer found that `[MED] (sub) CACHE Notification Facade` (338df4f8-af86-44f9-855c-943d8d0d478f, version 1) has no Return Documents shape. It runs Start -> Process Route `[MED] Process Service` (wait=true, abort=true) -> Stop (continue=true) on both outcomes, so nothing comes back from the Process Call and no step after it runs. Each facade call now sits on branch 1 of its own Branch shape, and the HTTP response is built on branch 2:
  - Branch 1: Set Properties `DDP_MED_NS_Msg` = Try/Catch message, then Process Call to the facade. Branch 1 ends at the Process Call.
  - Branch 2: build the 400 response (TC-F path) or the 500 response (TC-A path), ending in Return Documents.
  - Two Branch shapes are added. Branch shapes do not count toward the Try/Catch limit. There are still exactly three Try/Catch shapes.
- **Consequences of the branch fix that the design now handles:**
  - A DDP set on branch 1 does not reach branch 2. The skill documents this in `branch_step.md` and `BOOMI_THINKING.md` ("DDPs set within branch: only follow that specific branch path"). So the 400 body on branch 2 can no longer read `DDP_MED_NS_Msg`. Branch 2 reads the Try/Catch message itself (Meta information "Base - Try/Catch Message", `meta.base.catcherrorsmessage`). The catch sets that property on the document before the Branch shape, and properties set before a Branch go down every branch (`BOOMI_THINKING.md`). Both branches therefore carry the same error text. This is checked in V5.
  - Return Documents count is unchanged at four ("Accepted", "Accepted - parked on retry topic", "Rejected - functional error", "Error"). Branch 1 returns no document, so the only document in the HTTP response is the one from branch 2.
  - The facade has no Return Documents shape, so the Process Call on branch 1 has no return paths and no outgoing connection. This is the documented "0 return paths" case (`process_call_step.md`), not an unwired outcome.
  - If the facade call on branch 1 fails, branch 2 does not run. Per `BOOMI_THINKING.md` ("When a document errors, processing halts for that document - subsequent steps and parallel branches don't execute"). On the TC-F path, the error goes to TC-A and the caller gets 500. On the TC-A path there is no enclosing Try/Catch, so the runtime returns its default error response. This matches the revision 3 behaviour for facade failures. See "HTTP response per outcome".
  - The facade runs before the response is built, so its run time counts against the 5 s maximum response time. This was already true in revision 3.
- **V4 resolved** by the branch fix. A new check, V6, confirms that branch 2 runs after the facade call on branch 1 returns.
- **Folder path (user: "2. b").** New leaf folder `PUB-GB-CG-043-Lead` under the existing sandbox path: `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead`. All new components go here. The existing folder `.../Publisher/PUB-GB-CG-043-leads` is not used and not changed.
- **Kafka connection (user: "3. a").** Reuse `[Confluent_NL-HQ_Kafka]` (c85b494e-58ab-4591-b946-76a9ec636414) in `SHV Energy N.V./00-ConnectionResources/00-Connections`. It is not edited. All its settings are extensible through process C1's extensions. It replaces `[Confluent_Kafka]`, which does not exist in a shared folder.
- **Environment (user: "4. yes, 1-DEV is dev").** `1-DEV` (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264) is the user-confirmed development target for build, deploy and test.
- **New developer checks** (listed in "Developer checks, run first"): D3 checks that extension values for the reused connection are already set in 1-DEV. D4 checks that the facade's Process Route targets run in 1-DEV. Neither changes the design. Each one stops the build and returns to the orchestrator if it fails.

## Requirements

Source: the user-supplied interface design document "PUB-GB-CG-043-Web_To_Lead_Publisher_V0.1.docx"
(author A. Koyyada, version 1, 21/09/2026), converted text at
`interfaces/PUB-GB-CG-043/design/source/requirements.md`, plus the user's answers quoted below.

Scope of this spec: **the Publisher only (PUB-GB-CG-043).**

- Sitecore submits selected web forms (web-to-lead) as a JSON request through Azure APIM, in real time
  and event driven. APIM calls the Boomi REST endpoint `/ws/rest/gb-cg-leads/v1/leads`. A Boomi API Service component publishes this endpoint (user, follow-up D: "Boomi API Service component"; base path, user: "gb-cg-leads/v1").
- Boomi publishes the request body **unchanged** to the Kafka topic `gb-cg.q.leads.in.insert` (document section 1.3.2; user Q12: "unchanged").
- Every published Kafka message carries the header `Retry-Count` with value `0` (user Q13: "header as 'Retry-COunt': 0 (we will use it later in retry mechanism, not for now)"). There is no message key. The user asked for the header only.
- Errors:
  - Functional error: no retry, **not sent to any Kafka topic**. `DDP_MED_NS_Msg` is set to the Try/Catch message (the functional error), the facade is called and Sitecore gets 400 (user Q8: "No retry on functional error"; user, revision 3 correction: "I was wrong. This message do not go to retry topic.").
  - Technical error: 3 retries, then send to the retry topic `gb-cg.q.leads.in.retry` (user Q8: "3 retry on all technical errors ... If tech retries expire after 3 times, also send to retry topic."; topic name, user follow-up B: "Nice name.").
- The facade `[MED] (sub) CACHE Notification Facade` is called with `DDP_MED_NS_Msg` set to the Try/Catch message in two cases: for a functional error, and when the retry-topic send fails. It is not called on success. It is not called when a technical error is parked on the retry topic (user, follow-up C: "the Try/Catch message in DDP_MED_NS_Msg should contain the functional error and if (very rarely) send to retry topic also fail. Sitecore should get 202").
- Downstream consumer (out of scope, separate interface): SUB-GB-CG-043 reads `gb-cg.q.leads.in.insert` and creates the Lead in Salesforce. `[SF_Connector]` belongs to that interface.
- Business criticality: Medium. The data contains customer fields and is sensitive.
- NFRs: maximum API response time 5 s. Volume about 60 calls per day, peak 75 per day, average 525 per week.
- Data validation is outside integration scope (document section 1.2.1). The only "functional" check is that the body is present and is a JSON object (see Error handling).
- Build account: `shvenergynv-6R344K` (user Q6). Build, deploy and test only in environment `1-DEV` (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264), which the user confirmed is development (revision 4: "yes, 1-DEV is dev"). Never production (CLAUDE.md). The orchestrator reports that the test runtime (`shv-energy-test.boomi.cloud`) has apiType `advanced`. That is why the endpoint is an API Service component and not a bare WSS listener.

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
| 9 | Tracking field(s) | `email` (request profile element `email`). Used on the WSS listen operation C3 and on both Kafka produce operations C7 (main topic) and C8 (retry topic). | user Q7: "email" |
| 10 | Full process name | `[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]` | CLAUDE.md: Process naming convention (Publisher segments); values from rows 1, 3, 4, 5a, 5b |
| 11 | Full folder path | `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead` | user, revision 4: "2. b" (sandbox path with a new leaf folder `PUB-GB-CG-043-Lead`); CLAUDE.md: Folder path convention (levels from `GB-CG` down) |
| 12 | Kafka connection (reuse) | `[Confluent_NL-HQ_Kafka]`, ID c85b494e-58ab-4591-b946-76a9ec636414, in `SHV Energy N.V./00-ConnectionResources/00-Connections`. Not edited; all settings extensible through C1 | user, revision 4: "3. a"; user Q14: "yes always reuse"; CLAUDE.md: Connector extensions |
| 13 | Build, deploy and test environment | `1-DEV`, ID 693e8bc2-46f8-4c7f-8259-8dcf6cf0f264, confirmed by the user as development | user, revision 4: "4. yes, 1-DEV is dev."; CLAUDE.md: SHV Energy naming and structure standards (Environment) |

Source is one of: `user: "<answer>"`, `CLAUDE.md: <section>`, or `OPEN`.

Notes:

- The Publisher pattern has exactly five segments: interface type, integration ID, main atomic object, source application and source BU. No target segments are added.
- **Deviation from the CLAUDE.md hint (user's explicit choice).** CLAUDE.md says that for Enterprise Projects the APPLICATION-NAME level is the target application (for example PDI, RNA, Paragon, OBTC). For this interface the user explicitly chose "Customer Portal" (follow-up A), which is the source application. This is recorded as the user's decision, not a derived value.
- **Folder root (user's explicit choice, revision 4).** The CLAUDE.md levels `GB-CG / Enterprise Projects / Customer Portal / Publisher / PUB-GB-CG-043-Lead` sit under the sandbox prefix `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/`. The user chose this prefix. The revision 3 root `Calor Group Limited/02-Deployable/` does not exist in the account (build log).
- Folder tree, as it appears in the account `shvenergynv-6R344K`. Only the leaf is new. The developer creates it under the existing `Publisher` folder:

      SHV Energy N.V.
        01-Sandbox
          01-Users
            Priyam
              BC
                GB-CG
                  Enterprise Projects
                    Customer Portal
                      Publisher
                        PUB-GB-CG-043-Lead      (new)
                        PUB-GB-CG-043-leads     (existing, not used, not changed)

## Components

All new components go into the interface folder (row 11) unless stated otherwise. The names below are proposals and are confirmed when the spec is approved. Only the process name is governed by the CLAUDE.md naming convention.

| # | Component | Type | New / reuse | Location | Notes |
|---|-----------|------|-------------|----------|-------|
| C1 | `[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]` | Process | New | Interface folder | Listen process. Process Mode `bridge`, allow simultaneous executions |
| C2 | `PUB-GB-CG-043 Lead API` | API Service component (`webservice`), REST | New | Interface folder | Base API path `gb-cg-leads/v1` (user: "gb-cg-leads/v1"). One REST route: POST, resource path `leads`, linked to C1 |
| C3 | `PUB-GB-CG-043 WSS Listen Lead` | Web Services Server operation (`wss`), Listen | New | Interface folder | Object/operation name `leads`. Input: single JSON document (C5). Output: single JSON document (C6). Tracked field `email` |
| C4 | `[Confluent_NL-HQ_Kafka]` (c85b494e-58ab-4591-b946-76a9ec636414) | Kafka connection | Reuse unchanged (user Q14: "yes always reuse"; revision 4: "3. a") | `SHV Energy N.V./00-ConnectionResources/00-Connections` | Not edited. All its settings are declared extensible on process C1 (see Connectors) |
| C5 | `PUB-GB-CG-043 Lead Request JSON` | JSON profile | New | Interface folder | Built from the corrected sample (see `mapping.md`). Field `additional-comments` (user Q11) |
| C6 | `PUB-GB-CG-043 Lead Response JSON` | JSON profile | New | Interface folder | `{"status": "...", "message": "..."}` (see `mapping.md`) |
| C7 | `PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.insert` | Kafka operation, Produce | New (user Q15: "new opretaion. always") | Interface folder | Topic `gb-cg.q.leads.in.insert`. Tracked field `email` |
| C8 | `PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.retry` | Kafka operation, Produce | New (user Q15; follow-up B) | Interface folder | Topic `gb-cg.q.leads.in.retry`. Used only on the technical-error path. Tracked field `email` |
| C9 | `[MED] (sub) CACHE Notification Facade` (338df4f8-af86-44f9-855c-943d8d0d478f) | Process (subprocess) | Reuse, read only (user Q16: "reuse, always") | `SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/00-SharedLibrary_v4/00-Version_4.0 (2019-12-28-baseline)/01-Facade/02-Process` | Called by Process Call (wait = true, abort = true) on branch 1 of a Branch shape. It has no Return Documents shape, so the Process Call has no return paths. Not edited |

Topics:

| Topic | Use | Source |
|-------|-----|--------|
| `gb-cg.q.leads.in.insert` | Main topic. Every accepted lead goes here | user: design document section 1.3.2 |
| `gb-cg.q.leads.in.retry` | Parking topic, **for technical errors after 3 retries only**. Functional errors are not sent here | user, follow-up B: "Nice name."; user revision 3 correction: "This message do not go to retry topic." |

Prerequisite (not a design decision, accepted by the user): both topics must already exist on the Confluent cluster that `[Confluent_NL-HQ_Kafka]` points to in `1-DEV`. Boomi cannot create Confluent topics. If a topic is missing, the developer or tester stops and reports it to the orchestrator.

## Process design

Start shape: Web Services Server listen, using operation C3, exposed through API Service component C2.

Main path (TC-A, TC-T and TC-F are the labels for the three Try/Catch shapes; BR-F and BR-A are the two Branch shapes):

1. **Start** (WSS listen, C3).
2. **TC-A** Try/Catch "Retry-topic send failure", retry count 0, catch All errors. The try path continues with step 3.
3. **Data Process, Custom Scripting "Check JSON body"** (script S1): sets `DDP_VALIDATION_ERROR`. The document passes through unchanged.
4. **Decision "Body is valid JSON?"**: `DDP_VALIDATION_ERROR` equals empty.
   - **True (valid)**: go to 5.
   - **False (functional error)**: go to 6.
5. Valid path (unchanged from revision 3):
   1. **Set Properties "Set Kafka header"**: sets the Kafka message header `Retry-Count` = `0` (static) as a document property, which the Kafka connector writes as a message header. It is set before TC-T, so the property travels on the document into the TC-T catch path.
   2. **TC-T** Try/Catch "Technical", **retry count 3**, catch All errors.
   3. Try: **Kafka Produce** (C4 + C7, topic `gb-cg.q.leads.in.insert`), body unchanged, header `Retry-Count: 0`.
   4. **Set Properties "Response 202"**: HTTP response status code 202.
   5. **Message "Accepted"**: `{"status":"accepted"}`.
   6. **Return Documents "Accepted"**.
   7. TC-T Catch (all 3 retries failed): **Kafka Produce** (C4 + C8, topic `gb-cg.q.leads.in.retry`), original body unchanged, header `Retry-Count: 0`.
   8. **Set Properties "Response 202 (parked)"**: HTTP status 202.
   9. **Message "Accepted (parked)"**: `{"status":"accepted"}`.
   10. **Return Documents "Accepted - parked on retry topic"**.
6. Functional-error path (no Kafka send, no retry):
   1. **TC-F** Try/Catch "Functional", retry count 0, catch All errors.
   2. Try: **Exception step "Functional error"** (stop single document = true), message = `DDP_VALIDATION_ERROR`. TC-F catches it, so the Try/Catch message holds the functional error.
   3. TC-F Catch: **Branch BR-F "Notify then reject"**, 2 branches (`numBranches="2"`).
   4. BR-F branch 1:
      1. **Set Properties "Set DDP_MED_NS_Msg"**: `DDP_MED_NS_Msg` = Meta information "Base - Try/Catch Message" (`meta.base.catcherrorsmessage`).
      2. **Process Call** `[MED] (sub) CACHE Notification Facade` (C9), wait = true, abort = true, no return paths. Branch 1 ends here.
   5. BR-F branch 2 (runs after branch 1 completes):
      1. **Set Properties "Response 400"**: HTTP status 400.
      2. **Message "Rejected"**: `{"status":"rejected","message":"<Try/Catch message>"}`. The `message` value comes from Meta information "Base - Try/Catch Message" and not from `DDP_MED_NS_Msg`, because a DDP set on branch 1 does not reach branch 2.
      3. **Return Documents "Rejected - functional error"**.
7. TC-A Catch (an error on the TC-T catch path, in practice a failed send to the retry topic; or, very rarely, an error on the TC-F catch path such as a failing facade call on BR-F branch 1):
   1. **Branch BR-A "Notify then error"**, 2 branches (`numBranches="2"`).
   2. BR-A branch 1:
      1. **Set Properties "Set DDP_MED_NS_Msg"**: `DDP_MED_NS_Msg` = Meta information "Base - Try/Catch Message".
      2. **Process Call** `[MED] (sub) CACHE Notification Facade` (C9), wait = true, abort = true, no return paths. Branch 1 ends here.
   3. BR-A branch 2 (runs after branch 1 completes):
      1. **Set Properties "Response 500"**: HTTP status 500.
      2. **Message "Error"**: `{"status":"error","message":"Technical error. The lead was not accepted."}`. The text is fixed so that no sensitive data or connection detail is returned.
      3. **Return Documents "Error"**.

Each outcome ends in its own Return Documents shape: four in total, the same as revision 3. No two outcomes converge on one step. Every Branch dragpoint is wired. The Process Calls have no outgoing connections because the facade returns no documents. There are no Notify shapes.

Shape count summary: Try/Catch 3 (TC-A, TC-T, TC-F), Branch 2 (BR-F, BR-A), Process Call 2, Return Documents 4, Exception 1, Decision 1, Data Process 1, Kafka connector steps 2.

### Developer checks, run first

These cover facts about the platform and environment that the local skill references do not document, or that the design depends on. Check them first, in `1-DEV`. If any check fails, do not redesign and do not add a fourth Try/Catch. Stop and return to the orchestrator.

- **D1. Environment.** Build, deploy and test only in `1-DEV` (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264). The user confirmed it is development (revision 4: "4. yes, 1-DEV is dev."). This answers the "Environment classification NOT CONFIRMED" result in the build log.
- **D2. Folder.** The parent `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/GB-CG/Enterprise Projects/Customer Portal/Publisher` exists. Create the new leaf `PUB-GB-CG-043-Lead` under it. Do not use or change the existing `PUB-GB-CG-043-leads`.
- **D3. Reused connection.** Pull `[Confluent_NL-HQ_Kafka]` (c85b494e-58ab-4591-b946-76a9ec636414) read only. Do not edit or push it. Check that its environment extension values are already set in `1-DEV`. If they are not set, stop and return to the orchestrator. Do not supply connection values or credentials yourself. Connection extension values are shared by every process in the environment that uses this connection, so never change them, including during tests.
- **D4. Facade runtime.** The facade calls a Process Route (`[MED] Process Service`). Process Route targets are not bundled with the parent deploy (skill `process_route_step.md`). In the first functional-error test, confirm that the facade call completes without error in `1-DEV`. If it fails because a route target is not deployed there, stop and return to the orchestrator. Do not deploy or edit shared framework components.
- **V1.** An error raised on the catch path of an inner Try/Catch (TC-T or TC-F), including on a Branch below it, must be caught by the enclosing TC-A. If the platform does not behave this way, the design would need a fourth Try/Catch. Do not add one. Stop and return to the orchestrator (CLAUDE.md: Error handling).
- **V2.** Kafka message header: the local skill has no Kafka connector reference. Use the Kafka connector's own mechanism for custom message headers (a document property or an operation header setting), following `references/guides/problem_solving_guide.md`. The header name must be exactly `Retry-Count` and the value `0`.
- **V3.** HTTP response status: set it with the Web Services Server response status-code document property (Set Properties, Connector properties, Web Services Server). This is not documented locally. Confirm the exact property against Boomi documentation.
- **V4. Resolved in revision 4.** The facade has no Return Documents shape (build log, 2026-10-08). The branch fix puts the response on branch 2, so it does not depend on the facade returning a document.
- **V5.** The Exception step's text must reach the TC-F Try/Catch message as `Functional error: ...`, and that same text must be readable on BR-F branch 2. Confirm in the test log and in the 400 body.
- **V6.** After the Process Call on branch 1 returns, the runtime runs branch 2. Confirm in the process log that, for one request, the facade runs first and then the 400 (or 500) Return Documents step runs. Confirm that the HTTP response contains only the branch 2 document.
- **Base path uniqueness.** Before deploying, check that no other API Service already deployed to `1-DEV` uses the base path `gb-cg-leads/v1`. If one does, stop and return to the orchestrator.
- **Topic existence.** Both `gb-cg.q.leads.in.insert` and `gb-cg.q.leads.in.retry` exist on the cluster that `[Confluent_NL-HQ_Kafka]` points to in `1-DEV`. If not, stop and return to the orchestrator.

### HTTP response per outcome

| Outcome | Kafka result | Facade called | HTTP status | Response body |
|---------|--------------|---------------|-------------|---------------|
| Valid body, main topic send succeeds (first try or within 3 retries) | Message on `gb-cg.q.leads.in.insert` | No | 202 | `{"status":"accepted"}` |
| Valid body, main topic fails 1 + 3 times, retry topic send succeeds | Message on `gb-cg.q.leads.in.retry` | No | 202 | `{"status":"accepted"}` |
| Valid body, main topic fails 1 + 3 times, retry topic send also fails | None | Yes, once (BR-A branch 1). `DDP_MED_NS_Msg` = retry-send error | 500 (BR-A branch 2) | `{"status":"error","message":"Technical error. The lead was not accepted."}` |
| Functional error (body missing, empty, not valid JSON, or not a JSON object) | None. No retry and no topic | Yes, once (BR-F branch 1). `DDP_MED_NS_Msg` = functional error | 400 (BR-F branch 2) | `{"status":"rejected","message":"<functional error>"}` |
| Functional error and the facade call on BR-F branch 1 fails (very rare) | None | Attempted on BR-F branch 1. BR-F branch 2 does not run. TC-A catches the facade error and calls the facade again on BR-A branch 1 | 500 (BR-A branch 2) | `{"status":"error","message":"Technical error. The lead was not accepted."}` |
| Any TC-A case where the facade call on BR-A branch 1 also fails (very rare) | As above | Attempted, failed | Runtime default error status (not set by the process) | Runtime default. BR-A branch 2 does not run and there is no enclosing Try/Catch |
| Not authenticated | Not reached. APIM or the API Service runtime rejects the call before the process runs | No | 401 (runtime) | Runtime default |

Sources: 202 with the `{"status":"accepted"}` body, 500 with an error message, and 400 as an allowed response all come from user Q9 ("Yes, all 3 are acceptable solution"). 202 after parking a technical failure comes from follow-up C ("Sitecore should get 202"). 400 for a functional error comes from the orchestrator's follow-up C proposal ("Sitecore 400"), which the user did not change and which the revision 3 relay confirms. 500 for a retry-send failure follows Q9 "failure 500". The two facade-failure rows are not user decisions. They are what the accepted Try/Catch structure and the user's branch fix do when the facade fails. They are the same as in revision 3 and are listed so the behaviour is visible.

### Target

Kafka topic `gb-cg.q.leads.in.insert` (main) and `gb-cg.q.leads.in.retry` (parking, technical errors only), through the existing `[Confluent_NL-HQ_Kafka]` connection.

### Deployment mode

`bridge` (process option Process Mode = Bridge, `workload="bridge"`). Source: CLAUDE.md: SHV Energy build rules, Deployment mode (Web Services Server start). Allow simultaneous executions = true (listener). Deploy C1 and C2 to `1-DEV` (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264) of account `shvenergynv-6R344K` only. The facade C9 is a Process Call, not a Process Route, from C1, so the C1 deploy bundles it. Its internal Process Route targets are not bundled (see D4).

### Endpoint and authentication

- API Service component C2 (type `webservice`, REST), base API path `gb-cg-leads/v1` (user: "gb-cg-leads/v1"), one route: POST, resource path `leads`, linked to process C1 (operation C3).
- Effective URL: `<runtime url>/ws/rest/gb-cg-leads/v1/leads`. APIM's backend URL must point at this URL.
- Before deploying, the developer checks that no other API Service already deployed to `1-DEV` uses the base path `gb-cg-leads/v1`. If one does, stop and return to the orchestrator.
- Authentication is whatever the API Service component and the advanced runtime already enforce (user, follow-up D). This spec contains no credentials.

## Error handling

Three Try/Catch shapes, which is the CLAUDE.md maximum. The user accepted this structure (revision 3 relay). The two Branch shapes added in revision 4 are not Try/Catch shapes and do not count toward the limit (user, revision 4: "branch fix").

| Try/Catch | Retry count | Wraps | Catch path |
|-----------|-------------|-------|------------|
| TC-A "Retry-topic send failure" | 0 | Everything after Start | Branch BR-A: (1) `DDP_MED_NS_Msg` = Try/Catch message -> facade; (2) HTTP 500 -> Return Documents "Error" |
| TC-T "Technical" | 3 (user Q8) | Main topic produce and the 202 response | Produce to the retry topic -> HTTP 202 -> Return Documents "Accepted - parked on retry topic" |
| TC-F "Functional" | 0 (user Q8: "No retry on functional error") | Exception step raising the functional error | Branch BR-F: (1) `DDP_MED_NS_Msg` = Try/Catch message (functional error) -> facade; (2) HTTP 400 with the Try/Catch message -> Return Documents "Rejected - functional error". No Kafka send (user revision 3 correction) |

Definitions:

- **Functional error**: the request body is missing or empty, is not valid JSON, or is not a JSON object. No other content validation is done, because validation is out of scope per the document. This is the orchestrator's follow-up C definition, and the user did not change it.
- **Technical error**: any error on the TC-T try path. In practice this is a Kafka produce failure on the main topic.

Retries in TC-T run immediately, with no back-off (skill reference `try_catch_step.md`), so the 3 retries add no fixed delay. Each Kafka attempt still adds its own connect and timeout time, which counts against the 5 s maximum response time. On the 400 and 500 paths the facade's run time also counts, because branch 2 starts only after branch 1 completes.

## Cache Notification Facade

- Called from two places. Each call is on branch 1 of a Branch shape and is preceded on that branch by a Set Properties step that sets `DDP_MED_NS_Msg` to Meta information "Base - Try/Catch Message":
  1. BR-F branch 1 (TC-F catch path): the message is the functional error. BR-F branch 2 then returns the 400 response. Nothing is sent to Kafka.
  2. BR-A branch 1 (TC-A catch path): the message is the retry-topic send failure (or, very rarely, a facade failure on BR-F branch 1). BR-A branch 2 then returns the 500 response.
- Not called on the success path or on the TC-T catch path (user, follow-up C).
- In normal operation the facade runs at most once per request. It runs twice only if the facade call on BR-F branch 1 itself fails (see "HTTP response per outcome").
- Facade: `[MED] (sub) CACHE Notification Facade` (338df4f8-af86-44f9-855c-943d8d0d478f) at `SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/00-SharedLibrary_v4/00-Version_4.0 (2019-12-28-baseline)/01-Facade/02-Process` (CLAUDE.md; user Q16: "reuse, always"). Process Call with wait = true and abort = true, and no return paths, because the facade ends both of its paths in Stop and has no Return Documents shape (build log). The facade is read only. If it changes, the parent C1 must be redeployed.

## Connectors

| Connection / operation | Purpose | Extensible settings | Tracking field |
|------------------------|---------|---------------------|----------------|
| C3 WSS listen operation | Receive the Sitecore lead JSON | No connection component. Every operation field the platform allows to be extended is extended (CLAUDE.md: Connector extensions). The object name and profiles are the API contract. | `email` |
| C4 `[Confluent_NL-HQ_Kafka]` (c85b494e-58ab-4591-b946-76a9ec636414, reused, not edited) | Kafka (Confluent) connection | All connection settings are declared in C1's process extensions (`processOverrides`): bootstrap servers, security protocol, SASL mechanism, username/client principal, password and every other connection field. Values are set per environment through Environment Extensions. They are never written into XML or this spec. Because the extension declaration lives on the process, the shared connection is not modified. In `1-DEV` the existing values are used as they are and never changed (D3). | n/a |
| C7 Kafka Produce, main | Publish to `gb-cg.q.leads.in.insert` | Topic name and every other extensible operation property | `email` |
| C8 Kafka Produce, retry | Publish to `gb-cg.q.leads.in.retry` (technical errors only) | Topic name and every other extensible operation property | `email` |
| `[SF_Connector]` | Not used. It belongs to SUB-GB-CG-043. | n/a | n/a |

Message key: none. Message header: `Retry-Count: 0` on every message that is sent, on both topics.

## Scripts

| Script | Single purpose |
|--------|----------------|
| S1 "Check JSON body" (Groovy, Data Process Custom Scripting) | For each document, read the body. If it is empty or whitespace, set `DDP_VALIDATION_ERROR` = `Functional error: request body is empty`. Otherwise parse it with `JsonSlurper`. If parsing fails, set `Functional error: request body is not valid JSON`. If the result is not a JSON object, set `Functional error: request body is not a JSON object`. Otherwise set it to empty. The script never throws, and it passes the document through unchanged. Accepted by the user (revision 3 relay). |

No other scripting. Headers, status codes and response bodies use Set Properties and Message steps. Message step JSON uses the single-quote escaping rule (skill Issue #1).

## Test notes

All tests run in `1-DEV` (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264) of account `shvenergynv-6R344K` only.

| Requirement | Observable behaviour to check |
|-------------|-------------------------------|
| Naming and folder | The process is named exactly `[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]` and is in `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead`. C2, C3 and C5 to C8 are in the same folder. Nothing new is in `.../Publisher/PUB-GB-CG-043-leads`. |
| Bridge mode | Process Mode = Bridge (`workload="bridge"`). Deployed to `1-DEV` only. |
| Endpoint | API Service C2 is deployed with base path `gb-cg-leads/v1`. A POST to `/ws/rest/gb-cg-leads/v1/leads` reaches C1. |
| Happy path | POST the valid sample lead JSON (see `mapping.md`). The response is 202 `{"status":"accepted"}` within 5 s. Exactly one message is on `gb-cg.q.leads.in.insert`, its body is byte-for-byte the request, it has header `Retry-Count` = `0` and no key. Nothing is on the retry topic. The facade is not called. |
| Tracking field | Process Reporting shows tracked field `email` populated on the listen and produce operations. |
| Technical error | Set the C7 operation's topic extension in `1-DEV` to a non-existent or unauthorised topic. Change only the C7 operation extension, never the shared connection's values, and restore C7 afterwards. The process log shows 1 + 3 attempts on the main produce, then one message on `gb-cg.q.leads.in.retry` with the original body and `Retry-Count: 0`. The response is 202 `{"status":"accepted"}`. The facade is not called. |
| Functional error | POST an empty body, a malformed JSON body (for example the document's original sample with the missing comma) and a JSON array. For each case: no retry; BR-F branch 1 calls the facade exactly once with `DDP_MED_NS_Msg` = the functional error text; then BR-F branch 2 returns 400 `{"status":"rejected","message":"Functional error: ..."}` with the same text (V5, V6); **nothing on the main topic and nothing on the retry topic**; no Kafka produce appears in the process log. The facade run completes without error (D4). |
| Retry-send failure | Break both the C7 and C8 topic extensions (operation extensions only; restore them afterwards) and send a valid lead. After 1 + 3 attempts on the main topic and a failed retry-topic send, BR-A branch 1 calls the facade once with the retry-send error. Then BR-A branch 2 returns 500 `{"status":"error","message":"Technical error. The lead was not accepted."}`. This also confirms V1 for TC-T and V6 for BR-A. |
| Extensions | The `[Confluent_NL-HQ_Kafka]` connection fields and the C7/C8 operation fields (including topic) appear under Environment Extensions for C1. No environment-specific value is in component XML. The shared `[Confluent_NL-HQ_Kafka]` component version is unchanged, and its `1-DEV` extension values are the same after testing as before. |
| No banned shapes | No Notify shapes. Exactly three Try/Catch shapes (TC-A retry 0, TC-T retry 3, TC-F retry 0). Two Branch shapes (BR-F, BR-A), each with `numBranches="2"` and both dragpoints wired. Four Return Documents shapes. |
| Volume | About 10 sequential calls all return 202 and produce 10 messages on the main topic. |

## Open questions

None. All required values and design decisions have a user or CLAUDE.md source.
