# Design spec: PUB-GB-CG-043

Status: READY FOR APPROVAL

Revision 5. This revision answers the developer's second BLOCKED report, which was raised against revision 4 (evidence: `interfaces/PUB-GB-CG-043/build/build-log.md`, section "Attempt 2"). It applies the user's decisions, which the orchestrator relayed verbatim: "1. b 2. a. fix in CLAUDE.md rule as well as an exception." Everything not listed under "Changes in revision 5" is unchanged from revision 4. The revision 4 change notes are kept below for history.

Revision 5 finalised: the user answered open question 1 (failure-path test approach) verbatim: "C, review only for now". The technical-error path and the retry-send-failure path are verified by review only in this build. V1 for TC-T and V6 for BR-A stay unconfirmed and are recorded as follow-ups F2 and F3. Required value row 16 is closed. No questions remain open.

## Changes in revision 5

- **Kafka header `Retry-Count` removed from this build (user: "1. b").** The developer found no source showing how the Boomi Kafka connector sets a custom message header. No component in the account sets one, the framework Produce operation (7bfb1b08) has no header field, and the Boomi documentation could not be reached (build log, Attempt 2, V2). Messages are now sent with **no custom headers and no key** on both topics. The Set Properties step "Set Kafka header" is removed from the valid path, and check V2 is withdrawn. The header becomes a follow-up for the future retry mechanism (see "Follow-ups"). The user's original Q13 request is kept on record there.
- **Topics fixed in C7 and C8 (user: "2. a").** Only operations whose action is Listen accept extension overrides (skill `process_extensions.md`; build log, Attempt 2). The Kafka topic is the Produce operation's object type. So `gb-cg.q.leads.in.insert` (C7) and `gb-cg.q.leads.in.retry` (C8) are fixed in the operation components, along with every other C7/C8 operation property. This is an approved exception under CLAUDE.md "SHV Energy build rules" > "Connector extensions" > Exception: "For other operations, such as a Kafka Produce, operation properties (including the Kafka topic, which is the operation's object type) cannot be made extensible and stay fixed in the operation component. The connection those operations use must still have all its settings extensible." Connection `[Confluent_NL-HQ_Kafka]` stays fully extensible through C1's `processOverrides`.
- **Connection extension block (developer note 4).** C1 declares the connection extensions by reusing the platform-generated `processOverrides` connection block for c85b494e as it appears in 45 of the 46 account processes that declare one: 17 fields, no xpath attributes. It is not hand-authored, as `process_extensions.md` requires. The connection component and its `1-DEV` extension values are not changed.
- **API Service route (developer note 3).** C2's single REST route has an **empty URL path**, route object `leads` and method POST. This gives exactly `/ws/rest/gb-cg-leads/v1/leads`. A route path of `leads` plus object `leads` would give `/leads/leads`. The existing `[PUB-GB-CG-043] Leads API` (bd886149, base `gb-cg`, in the old `-leads` folder) uses the same empty-path pattern. It is not used or changed.
- **Test notes for the failure paths.** The technical-error and retry-send-failure tests no longer rely on topic extensions. Changing the shared connection or its `1-DEV` extension values is still forbidden. Three ways to run them are set out under "Failure-path test approach". Choosing one needs a user decision, which is open question 1.
- **Extensions test** now checks that the connection fields are extensible on C1 and that C7/C8 have no operation overrides, under the CLAUDE.md exception.
- **Developer checks:** V2 is withdrawn. D3 is marked passed (build log, Attempt 2). D5 is added for the route shape, and D6 for the connection override block.
- **Failure-path tests decided (user: "C, review only for now").** Option C is applied. The technical-error test and the retry-send-failure test do not run in `1-DEV` in this build. The reviewer verifies both paths from the built process (checklist under "Failure-path test approach"). V1 for TC-T and V6 for BR-A stay unconfirmed and become follow-ups F2 and F3 for later testing. Row 16 is closed, open question 1 is removed, and the test notes are updated. All other tests still run in `1-DEV`.

## Changes in revision 4 (history)

- **Facade call pattern, "branch fix" (user: "1. branch fix").** The facade `[MED] (sub) CACHE Notification Facade` (338df4f8, version 1) has no Return Documents shape. So each facade call sits on branch 1 of its own Branch shape, and the HTTP response is built on branch 2. Two Branch shapes were added. There are still exactly three Try/Catch shapes.
- A DDP set on branch 1 does not reach branch 2. So branch 2 reads Meta information "Base - Try/Catch Message" (`meta.base.catcherrorsmessage`) instead of `DDP_MED_NS_Msg`.
- Folder path (user: "2. b"), Kafka connection reuse `[Confluent_NL-HQ_Kafka]` (user: "3. a"), environment `1-DEV` (user: "4. yes, 1-DEV is dev"), checks D3 and D4 added.

## Requirements

Source: the user-supplied interface design document "PUB-GB-CG-043-Web_To_Lead_Publisher_V0.1.docx"
(author A. Koyyada, version 1, 21/09/2026), converted text at
`interfaces/PUB-GB-CG-043/design/source/requirements.md`, plus the user's answers quoted below.

Scope of this spec: **the Publisher only (PUB-GB-CG-043).**

- Sitecore submits selected web forms (web-to-lead) as a JSON request through Azure APIM, in real time
  and event driven. APIM calls the Boomi REST endpoint `/ws/rest/gb-cg-leads/v1/leads`. A Boomi API Service component publishes this endpoint (user, follow-up D: "Boomi API Service component"; base path, user: "gb-cg-leads/v1").
- Boomi publishes the request body **unchanged** to the Kafka topic `gb-cg.q.leads.in.insert` (document section 1.3.2; user Q12: "unchanged").
- Messages carry **no custom headers and no key** (revision 5, user: "1. b"). The `Retry-Count` header that the user asked for in Q13 is deferred to the future retry mechanism (see "Follow-ups").
- Errors:
  - Functional error: no retry, **not sent to any Kafka topic**. `DDP_MED_NS_Msg` is set to the Try/Catch message (the functional error), the facade is called and Sitecore gets 400 (user Q8: "No retry on functional error"; user, revision 3 correction: "I was wrong. This message do not go to retry topic.").
  - Technical error: 3 retries, then send to the retry topic `gb-cg.q.leads.in.retry` (user Q8: "3 retry on all technical errors ... If tech retries expire after 3 times, also send to retry topic."; topic name, user follow-up B: "Nice name.").
- The facade `[MED] (sub) CACHE Notification Facade` is called with `DDP_MED_NS_Msg` set to the Try/Catch message in two cases: for a functional error, and when the retry-topic send fails. It is not called on success. It is not called when a technical error is parked on the retry topic (user, follow-up C: "the Try/Catch message in DDP_MED_NS_Msg should contain the functional error and if (very rarely) send to retry topic also fail. Sitecore should get 202").
- Downstream consumer (out of scope, separate interface): SUB-GB-CG-043 reads `gb-cg.q.leads.in.insert` and creates the Lead in Salesforce. `[SF_Connector]` belongs to that interface.
- Business criticality: Medium. The data contains customer fields and is sensitive.
- NFRs: maximum API response time 5 s. Volume about 60 calls per day, peak 75 per day, average 525 per week.
- Data validation is outside integration scope (document section 1.2.1). The only "functional" check is that the body is present and is a JSON object (see Error handling).
- Build account: `shvenergynv-6R344K` (user Q6). Build, deploy and test only in environment `1-DEV` (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264), which the user confirmed is development (revision 4: "yes, 1-DEV is dev"). Never production (CLAUDE.md). The test runtime (`shv-energy-test.boomi.cloud`, atom 9beaf0cb) has apiType `advanced` (build log, Attempt 2). That is why the endpoint is an API Service component and not a bare WSS listener.

## Follow-ups (not in this build)

| # | Follow-up | Source |
|---|-----------|--------|
| F1 | Add the Kafka message header `Retry-Count` = `0` to every published message when the retry mechanism is designed. First find out how the Boomi Kafka connector sets a custom header, from Boomi documentation or a working example the user supplies. The original request was "header as 'Retry-COunt': 0 (we will use it later in retry mechanism, not for now)". | user Q13; user revision 5: "1. b" |
| F2 | Confirm **V1 for TC-T** at runtime: an error on the TC-T catch path (a failed send to `gb-cg.q.leads.in.retry`) is caught by the enclosing TC-A. Run the technical-error test (main topic produce fails 1 + 3 times, one message on the retry topic, 202, facade not called) and the retry-send-failure test, using option A or B from "Failure-path test approach" or another approach the user approves. Not tested in this build. | user, open question 1: "C, review only for now" |
| F3 | Confirm **V6 for BR-A** at runtime: on the TC-A catch path, BR-A branch 1 calls the facade once with `DDP_MED_NS_Msg` = the retry-send error, then BR-A branch 2 returns 500 `{"status":"error","message":"Technical error. The lead was not accepted."}`, and the HTTP response holds only the branch 2 document. Run with the retry-send-failure test in F2. Not tested in this build. | user, open question 1: "C, review only for now" |

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
| 14 | Kafka topics fixed in C7/C8 (not extensible) | `gb-cg.q.leads.in.insert` in C7, `gb-cg.q.leads.in.retry` in C8, fixed in the operation components | user, revision 5: "2. a"; CLAUDE.md: SHV Energy build rules, Connector extensions, Exception |
| 15 | Kafka message header | None in this build. `Retry-Count` deferred (F1) | user, revision 5: "1. b" |
| 16 | Failure-path test approach (technical error, retry-send failure) | Option C: not tested in `1-DEV` in this build; verified by review only. V1 for TC-T and V6 for BR-A stay unconfirmed (follow-ups F2, F3) | user, open question 1: "C, review only for now" |

Source is one of: `user: "<answer>"`, `CLAUDE.md: <section>`, or `OPEN`.

Notes:

- The Publisher pattern has exactly five segments: interface type, integration ID, main atomic object, source application and source BU. No target segments are added.
- **Deviation from the CLAUDE.md hint (user's explicit choice).** CLAUDE.md says that for Enterprise Projects the APPLICATION-NAME level is the target application (for example PDI, RNA, Paragon, OBTC). For this interface the user explicitly chose "Customer Portal" (follow-up A), which is the source application. This is recorded as the user's decision, not a derived value.
- **Folder root (user's explicit choice, revision 4).** The CLAUDE.md levels `GB-CG / Enterprise Projects / Customer Portal / Publisher / PUB-GB-CG-043-Lead` sit under the sandbox prefix `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/`. The user chose this prefix.
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
| C1 | `[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]` | Process | New | Interface folder | Listen process. Process Mode `bridge`, allow simultaneous executions. Declares the connection overrides for C4 (platform-generated block, D6) |
| C2 | `PUB-GB-CG-043 Lead API` | API Service component (`webservice`), REST | New | Interface folder | Base API path `gb-cg-leads/v1` (user: "gb-cg-leads/v1"). One REST route: method POST, route object `leads`, **URL path empty**, linked to C1 (revision 5, developer note 3) |
| C3 | `PUB-GB-CG-043 WSS Listen Lead` | Web Services Server operation (`wss`), Listen | New | Interface folder | Object/operation name `leads`. Input: single JSON document (C5). Output: single JSON document (C6). Tracked field `email` |
| C4 | `[Confluent_NL-HQ_Kafka]` (c85b494e-58ab-4591-b946-76a9ec636414) | Kafka connection | Reuse unchanged (user Q14: "yes always reuse"; revision 4: "3. a") | `SHV Energy N.V./00-ConnectionResources/00-Connections` | Not edited. All its settings are declared extensible on process C1 (see Connectors) |
| C5 | `PUB-GB-CG-043 Lead Request JSON` | JSON profile | New | Interface folder | Built from the corrected sample (see `mapping.md`). Field `additional-comments` (user Q11) |
| C6 | `PUB-GB-CG-043 Lead Response JSON` | JSON profile | New | Interface folder | `{"status": "...", "message": "..."}` (see `mapping.md`) |
| C7 | `PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.insert` | Kafka operation, Produce | New (user Q15: "new opretaion. always") | Interface folder | Topic `gb-cg.q.leads.in.insert`, **fixed** (not extensible, CLAUDE.md exception). No header, no key. Tracked field `email` |
| C8 | `PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.retry` | Kafka operation, Produce | New (user Q15; follow-up B) | Interface folder | Topic `gb-cg.q.leads.in.retry`, **fixed** (not extensible, CLAUDE.md exception). Used only on the technical-error path. No header, no key. Tracked field `email` |
| C9 | `[MED] (sub) CACHE Notification Facade` (338df4f8-af86-44f9-855c-943d8d0d478f) | Process (subprocess) | Reuse, read only (user Q16: "reuse, always") | `SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/00-SharedLibrary_v4/00-Version_4.0 (2019-12-28-baseline)/01-Facade/02-Process` | Called by Process Call (wait = true, abort = true) on branch 1 of a Branch shape. It has no Return Documents shape, so the Process Call has no return paths. Not edited |

Topics:

| Topic | Use | Source |
|-------|-----|--------|
| `gb-cg.q.leads.in.insert` | Main topic. Every accepted lead goes here | user: design document section 1.3.2 |
| `gb-cg.q.leads.in.retry` | Parking topic, **for technical errors after 3 retries only**. Functional errors are not sent here | user, follow-up B: "Nice name."; user revision 3 correction: "This message do not go to retry topic." |

Because the topics are fixed in C7 and C8, the same topic names are used in every environment the process is promoted to (user, revision 5: "2. a"). If a later environment needs different topic names, the operation components must be changed in that release.

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
5. Valid path (revision 5: the "Set Kafka header" step is removed; nothing else changes):
   1. **TC-T** Try/Catch "Technical", **retry count 3**, catch All errors.
   2. Try: **Kafka Produce** (C4 + C7, topic `gb-cg.q.leads.in.insert`), body unchanged, no headers, no key.
   3. **Set Properties "Response 202"**: HTTP response status code 202.
   4. **Message "Accepted"**: `{"status":"accepted"}`.
   5. **Return Documents "Accepted"**.
   6. TC-T Catch (all 3 retries failed): **Kafka Produce** (C4 + C8, topic `gb-cg.q.leads.in.retry`), original body unchanged, no headers, no key.
   7. **Set Properties "Response 202 (parked)"**: HTTP status 202.
   8. **Message "Accepted (parked)"**: `{"status":"accepted"}`.
   9. **Return Documents "Accepted - parked on retry topic"**.
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

Each outcome ends in its own Return Documents shape: four in total. No two outcomes converge on one step. Every Branch dragpoint is wired. The Process Calls have no outgoing connections because the facade returns no documents. There are no Notify shapes.

Shape count summary: Try/Catch 3 (TC-A, TC-T, TC-F), Branch 2 (BR-F, BR-A), Process Call 2, Return Documents 4, Exception 1, Decision 1, Data Process 1, Kafka connector steps 2.

### Developer checks, run first

These cover facts about the platform and environment that the local skill references do not document, or that the design depends on. Check them first, in `1-DEV`. If any check fails, do not redesign and do not add a fourth Try/Catch. Stop and return to the orchestrator.

- **D1. Environment.** Build, deploy and test only in `1-DEV` (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264). The user confirmed it is development. Passed in Attempt 2.
- **D2. Folder.** The parent `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/GB-CG/Enterprise Projects/Customer Portal/Publisher` exists. Create the new leaf `PUB-GB-CG-043-Lead` under it. Do not use or change the existing `PUB-GB-CG-043-leads`.
- **D3. Reused connection.** Pull `[Confluent_NL-HQ_Kafka]` (c85b494e-58ab-4591-b946-76a9ec636414) read only. Do not edit or push it. Its `1-DEV` extension values must already be set. Passed in Attempt 2 (username and password set; other fields use the component defaults, which are non-empty). Do not supply connection values or credentials. Connection extension values are shared by every process in the environment that uses this connection, so never change them, including during tests.
- **D4. Facade runtime.** The facade calls a Process Route (`[MED] Process Service`). Process Route targets are not bundled with the parent deploy (skill `process_route_step.md`). In the first functional-error test, confirm that the facade call completes without error in `1-DEV`. If it fails because a route target is not deployed there, stop and return to the orchestrator. Do not deploy or edit shared framework components.
- **D5. API route (revision 5).** In C2, configure the single REST route with method POST, route object `leads` and an **empty URL path**. In the first test, confirm that a POST to `/ws/rest/gb-cg-leads/v1/leads` reaches C1 and that `/ws/rest/gb-cg-leads/v1/leads/leads` does not. If the effective path differs, stop and return to the orchestrator.
- **D6. Connection override block (revision 5).** In C1, declare the C4 connection extensions by copying the platform-generated `processOverrides` connection block for c85b494e as it appears in 45 of the 46 account processes that declare one (17 fields, no xpath attributes). Do not hand-author it, and do not declare any operation overrides for C7 or C8 (CLAUDE.md: Connector extensions, Exception). After pushing C1, confirm with `boomi-extensions.sh get` that the connection fields appear for C1 in `1-DEV`. Do not run `set`.
- **V1.** An error raised on the catch path of an inner Try/Catch (TC-T or TC-F), including on a Branch below it, must be caught by the enclosing TC-A. If the platform does not behave this way, the design would need a fourth Try/Catch. Do not add one. Stop and return to the orchestrator (CLAUDE.md: Error handling). In this build V1 for TC-T is **not confirmed at runtime** (user: "C, review only for now"). The reviewer checks only that the TC-T catch path sits inside the TC-A try path. Runtime confirmation is follow-up F2. The TC-F part of V1 arises only if the facade call on BR-F branch 1 fails, and no test in this build exercises it.
- **V2. Withdrawn in revision 5.** No Kafka header is set in this build (user: "1. b"; follow-up F1).
- **V3.** HTTP response status: set it with the Web Services Server response status-code document property (Set Properties, Connector properties, Web Services Server). This is not documented locally. Confirm the exact property against Boomi documentation or an existing account process that sets it. Confirm the status in the first test of each outcome.
- **V4. Resolved in revision 4.** The branch fix puts the response on branch 2, so it does not depend on the facade returning a document.
- **V5.** The Exception step's text must reach the TC-F Try/Catch message as `Functional error: ...`, and that same text must be readable on BR-F branch 2. Confirm in the test log and in the 400 body.
- **V6.** After the Process Call on branch 1 returns, the runtime runs branch 2. Confirm in the process log that, for one request, the facade runs first and then the 400 (or 500) Return Documents step runs. Confirm that the HTTP response contains only the branch 2 document. In this build V6 is confirmed for **BR-F only**, by the functional-error test. V6 for BR-A is **not confirmed at runtime** (user: "C, review only for now"). The reviewer checks the BR-A structure instead, and runtime confirmation is follow-up F3.
- **Base path uniqueness.** Passed in Attempt 2: no API Service in the account uses `gb-cg-leads/v1`. Recheck just before deploying.
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

Sources: 202 with the `{"status":"accepted"}` body, 500 with an error message, and 400 as an allowed response all come from user Q9 ("Yes, all 3 are acceptable solution"). 202 after parking a technical failure comes from follow-up C ("Sitecore should get 202"). 400 for a functional error comes from the orchestrator's follow-up C proposal ("Sitecore 400"), which the user did not change and which the revision 3 relay confirms. 500 for a retry-send failure follows Q9 "failure 500". The two facade-failure rows are not user decisions. They are what the accepted Try/Catch structure and the user's branch fix do when the facade fails.

### Target

Kafka topic `gb-cg.q.leads.in.insert` (main) and `gb-cg.q.leads.in.retry` (parking, technical errors only), through the existing `[Confluent_NL-HQ_Kafka]` connection. Topics fixed in C7 and C8.

### Deployment mode

`bridge` (process option Process Mode = Bridge, `workload="bridge"`). Source: CLAUDE.md: SHV Energy build rules, Deployment mode (Web Services Server start). Allow simultaneous executions = true (listener). Deploy C1 and C2 to `1-DEV` (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264) of account `shvenergynv-6R344K` only. The facade C9 is a Process Call, not a Process Route, from C1, so the C1 deploy bundles it. Its internal Process Route targets are not bundled (see D4).

### Endpoint and authentication

- API Service component C2 (type `webservice`, REST), base API path `gb-cg-leads/v1` (user: "gb-cg-leads/v1"). One route: method POST, route object `leads`, URL path empty, linked to process C1 (operation C3). The effective path is `/<base>/<object>/<url path>`, so an empty URL path gives `/gb-cg-leads/v1/leads` (build log, Attempt 2, decision 2; D5).
- Effective URL: `<runtime url>/ws/rest/gb-cg-leads/v1/leads`. APIM's backend URL must point at this URL.
- Before deploying, the developer rechecks that no other API Service already deployed to `1-DEV` uses the base path `gb-cg-leads/v1`. If one does, stop and return to the orchestrator.
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
- Facade: `[MED] (sub) CACHE Notification Facade` (338df4f8-af86-44f9-855c-943d8d0d478f) at `SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/00-SharedLibrary_v4/00-Version_4.0 (2019-12-28-baseline)/01-Facade/02-Process` (CLAUDE.md; user Q16: "reuse, always"). Process Call with wait = true and abort = true, and no return paths, because the facade ends both of its paths in Stop and has no Return Documents shape. The facade is read only. If it changes, the parent C1 must be redeployed.

## Connectors

| Connection / operation | Purpose | Extensible settings | Tracking field |
|------------------------|---------|---------------------|----------------|
| C3 WSS listen operation | Receive the Sitecore lead JSON | No connection component. Every operation field the platform allows to be extended is extended (CLAUDE.md: Connector extensions; Listen operations accept overrides). The object name and profiles are the API contract. | `email` |
| C4 `[Confluent_NL-HQ_Kafka]` (c85b494e-58ab-4591-b946-76a9ec636414, reused, not edited) | Kafka (Confluent) connection | All connection settings are declared in C1's `processOverrides` by copying the platform-generated block for c85b494e used in 45 of 46 account processes (17 fields, no xpath attributes; D6). Values are set per environment through Environment Extensions. They are never written into XML or this spec. The shared connection is not modified. In `1-DEV` the existing values are used as they are and never changed (D3). | n/a |
| C7 Kafka Produce, main | Publish to `gb-cg.q.leads.in.insert` | **None (approved exception).** Produce is not a Listen operation, so no operation property can be extended. The topic and all other operation properties are fixed in C7 (user, revision 5: "2. a"; CLAUDE.md: SHV Energy build rules, Connector extensions, Exception). No environment-specific connection value is in C7. | `email` |
| C8 Kafka Produce, retry | Publish to `gb-cg.q.leads.in.retry` (technical errors only) | **None (approved exception)**, as for C7. | `email` |
| `[SF_Connector]` | Not used. It belongs to SUB-GB-CG-043. | n/a | n/a |

Message key: none. Message headers: none in this build (user, revision 5: "1. b"; follow-up F1).

## Scripts

| Script | Single purpose |
|--------|----------------|
| S1 "Check JSON body" (Groovy, Data Process Custom Scripting) | For each document, read the body. If it is empty or whitespace, set `DDP_VALIDATION_ERROR` = `Functional error: request body is empty`. Otherwise parse it with `JsonSlurper`. If parsing fails, set `Functional error: request body is not valid JSON`. If the result is not a JSON object, set `Functional error: request body is not a JSON object`. Otherwise set it to empty. The script never throws, and it passes the document through unchanged. Accepted by the user (revision 3 relay). |

No other scripting. Status codes and response bodies use Set Properties and Message steps. Message step JSON uses the single-quote escaping rule (skill Issue #1).

## Failure-path test approach

**Decision: option C (user: "C, review only for now").** In this build the technical-error path (TC-T retries, then the retry topic) and the retry-send-failure path (TC-A catch, BR-A, facade, 500) are verified by review only. They are not run in `1-DEV`. Options A and B are kept below for the later runtime tests (follow-ups F2 and F3).

Review checklist for these two paths (the reviewer checks the built C1 XML and records the evidence in `review/findings.md`; the tester refers to it):

- R1. TC-T has retry count 3 and catches All errors. Its try path holds only the C7 produce, Set Properties "Response 202", Message "Accepted" and Return Documents "Accepted".
- R2. The TC-T catch path goes to the C8 produce (topic `gb-cg.q.leads.in.retry`, fixed in C8), then Set Properties "Response 202 (parked)", Message "Accepted (parked)" and Return Documents "Accepted - parked on retry topic". There is no facade call, no Set Properties for `DDP_MED_NS_Msg` and no header or key on this path.
- R3. TC-T (with its catch path) sits inside the TC-A try path, so an error on the TC-T catch path can reach TC-A. Runtime behaviour is unconfirmed (V1 for TC-T, F2).
- R4. TC-A has retry count 0 and catches All errors. Its catch path goes to Branch BR-A with `numBranches="2"` and both dragpoints wired.
- R5. BR-A branch 1: Set Properties `DDP_MED_NS_Msg` = Meta information "Base - Try/Catch Message", then a Process Call to C9 (338df4f8) with wait = true, abort = true and no return paths.
- R6. BR-A branch 2: Set Properties HTTP status 500, Message `{"status":"error","message":"Technical error. The lead was not accepted."}`, Return Documents "Error". Runtime order and single-document response are unconfirmed (V6 for BR-A, F3).

Background (from revision 5): topics are fixed in C7 and C8, so they can no longer be broken through operation extensions. The shared connection and its `1-DEV` extension values must not be changed (D3). The technical-error and retry-send-failure paths need a Kafka produce to fail without touching either of those. These were the three options:

- **Option A: block topic writes on the Kafka side (recommended).** The Confluent cluster administrator temporarily removes write (produce) permission for the `1-DEV` Kafka principal used by `[Confluent_NL-HQ_Kafka]`, on these topics only:
  - Technical-error test: remove write on `gb-cg.q.leads.in.insert` only. Expected: 1 + 3 failed attempts on the main produce, one message on `gb-cg.q.leads.in.retry`, 202 `{"status":"accepted"}`, facade not called.
  - Retry-send-failure test: remove write on both topics. Expected: 1 + 3 failed main attempts, a failed retry-topic send, BR-A branch 1 calls the facade once, BR-A branch 2 returns 500. This also confirms V1 for TC-T and V6 for BR-A.
  - The administrator restores the permissions straight after each test.
  - This tests the real deployed C1 through the real endpoint with no Boomi change. It affects only these two new topics, which no other publisher writes to, and it does not change read access for SUB-GB-CG-043. It needs someone outside Boomi with Confluent admin rights. The 5 s response-time check does not apply to these two tests.
- **Option B: temporary test harness in Boomi.** The developer makes a temporary copy of C1, in a test subfolder of the interface folder. The copy starts with a no-data Start and a Message step holding the sample lead, as in the skill's `process_testing_guide.md`. It uses copies of C7 and C8 that point at a topic name that does not exist. It is deployed to `1-DEV`, run with `boomi-test-execute.sh`, then undeployed and deleted. Limits:
  - It does not test the real C1 or the HTTP status codes, which are seen only in the process log.
  - A missing topic fails only if topic auto-creation is off on the cluster. The failure may come only after the producer's metadata timeout, which can be up to 60 s per attempt and so several minutes for 1 + 3 attempts.
  - It adds temporary components and a deployment. A process name and folder for the harness would be needed from the user, because CLAUDE.md naming applies to every process.
- **Option C: do not test these two paths in `1-DEV`.** They are verified only by review of the built process: the TC-T retry count is 3, the TC-T catch path goes to the C8 produce, and the TC-A catch path goes to BR-A. V1 for TC-T and V6 for BR-A stay unconfirmed. The risk is that a failed retry-topic send behaves differently from the design in production. V6 is still confirmed on the BR-F path by the functional-error test.

## Test notes

All tests run in `1-DEV` (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264) of account `shvenergynv-6R344K` only. Never change the `[Confluent_NL-HQ_Kafka]` component or its `1-DEV` extension values.

Exception (user: "C, review only for now"): the **Technical error** and **Retry-send failure** rows are not run in `1-DEV` in this build. They are verified by review only (R1 to R6 under "Failure-path test approach"). The tester records each as "not tested in dev, verified by review" with a pointer to the review evidence, and records V1 for TC-T and V6 for BR-A as unconfirmed (follow-ups F2, F3). The tester must not break a topic, the connection or its extension values to force these paths. Every other row runs in `1-DEV`.

| Requirement | Observable behaviour to check |
|-------------|-------------------------------|
| Naming and folder | The process is named exactly `[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]` and is in `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead`. C2, C3 and C5 to C8 are in the same folder. Nothing new is in `.../Publisher/PUB-GB-CG-043-leads`. |
| Bridge mode | Process Mode = Bridge (`workload="bridge"`). Deployed to `1-DEV` only. |
| Endpoint | API Service C2 is deployed with base path `gb-cg-leads/v1` and one route: POST, object `leads`, empty URL path. A POST to `/ws/rest/gb-cg-leads/v1/leads` reaches C1. `/ws/rest/gb-cg-leads/v1/leads/leads` does not (D5). |
| Happy path | POST the valid sample lead JSON (see `mapping.md`). The response is 202 `{"status":"accepted"}` within 5 s. Exactly one message is on `gb-cg.q.leads.in.insert`. Its body is byte-for-byte the request, and it has **no custom headers and no key**. Nothing is on the retry topic. The facade is not called. |
| Tracking field | Process Reporting shows tracked field `email` populated on the listen and produce operations. |
| Technical error | **Review only in this build** (user: "C, review only for now"; R1 to R3). Not run in `1-DEV`. Record "not tested in dev, verified by review" with the review evidence, and V1 for TC-T as unconfirmed (F2). Expected behaviour when it is later run (F2): 1 + 3 attempts on the main produce, then one message on `gb-cg.q.leads.in.retry` with the original body, no headers and no key. The response is 202 `{"status":"accepted"}`. The facade is not called. Topics and connection extension values are not changed in Boomi. |
| Functional error | POST an empty body, a malformed JSON body (for example the document's original sample with the missing comma) and a JSON array. For each case: no retry; BR-F branch 1 calls the facade exactly once with `DDP_MED_NS_Msg` = the functional error text; then BR-F branch 2 returns 400 `{"status":"rejected","message":"Functional error: ..."}` with the same text (V5, V6); **nothing on the main topic and nothing on the retry topic**; no Kafka produce appears in the process log. The facade run completes without error (D4). |
| Retry-send failure | **Review only in this build** (user: "C, review only for now"; R3 to R6). Not run in `1-DEV`. Record "not tested in dev, verified by review" with the review evidence, and V1 for TC-T and V6 for BR-A as unconfirmed (F2, F3). Expected behaviour when it is later run (F2, F3): after 1 + 3 attempts on the main topic and a failed retry-topic send, BR-A branch 1 calls the facade once with the retry-send error. Then BR-A branch 2 returns 500 `{"status":"error","message":"Technical error. The lead was not accepted."}`. That run confirms V1 for TC-T and V6 for BR-A. |
| Extensions | Under Environment Extensions for C1 in `1-DEV`, the `[Confluent_NL-HQ_Kafka]` connection fields appear (17 fields, D6). C7 and C8 have no operation overrides, and their topics are fixed in the component XML, as the CLAUDE.md "Connector extensions" exception allows. No environment-specific connection value is in any component XML. The shared `[Confluent_NL-HQ_Kafka]` component version is unchanged, and its `1-DEV` extension values are the same after testing as before. |
| No banned shapes | No Notify shapes. Exactly three Try/Catch shapes (TC-A retry 0, TC-T retry 3, TC-F retry 0). Two Branch shapes (BR-F, BR-A), each with `numBranches="2"` and both dragpoints wired. Four Return Documents shapes. No Set Properties step for a Kafka header. |
| Volume | About 10 sequential calls all return 202 and produce 10 messages on the main topic. |

## Open questions

None. Revision 5 question 1 (failure-path test approach) was answered by the user: "C, review only for now" (row 16).
