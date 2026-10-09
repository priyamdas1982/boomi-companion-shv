# Design spec: PUB-GB-CG-043

Status: DRAFT - OPEN QUESTIONS

Revision 7 (round 1 design feedback loop, 2026-10-09). Starts from approved revision 6. It answers the developer's BLOCKED report in round 1 fix mode (evidence: `interfaces/PUB-GB-CG-043/build/build-log.md`, "Attempt 4 / Round 1 fix", "Developer checks", "Log analysis" and "Blocking items"; executions 22c61363, bcec584b and 93e06b38). It applies the user's answers, relayed verbatim by the orchestrator on 2026-10-09:

1. "I have just created gb-cg.q.leads.in.retry and gb-cg.q.leads.in.insert in confluent."
2. (facade inputs) "set whatever needs to be set and available to you."
3. (retries vs runtime limit) "kafka outage should give an error back."
4. (/leads/leads reaches C1) "b" (it is a defect; change the route so only `/ws/rest/gb-cg-leads/v1/leads` reaches C1).

It also reflects the new CLAUDE.md rules "Kafka topics must exist before the build" and "Connectivity checks first". Everything not listed under "Changes in revision 7" is unchanged from revision 6. Ten questions are open (see "Open questions"), so this revision is not ready for approval yet.

## Changes in revision 7

- **Facade inputs set before every facade call (D4; user: "set whatever needs to be set and available to you").** The facade's route target `[MED] (sub) CACHE Notification` (47e2da88 v2) fails at its Document Cache Load because `DPP_MED_ProcessId` is empty (execution 22c61363). On BR-F branch 1 and BR-A branch 1, the Set Properties step before the facade call is renamed "Set facade inputs". Besides `DDP_MED_NS_Msg` it now sets every facade input that has a source available at runtime, from Boomi execution properties: `DPP_MED_ProcessId` (Process Id, the fatal one), `DPP_MED_ProcessName`, `DPP_MED_ExecutionId`, `DPP_MED_AccountId`, `DPP_MED_AtomId`, `DPP_MED_AtomName` and `DPP_MED_ContainerId` (Atom Id). The seven inputs with no runtime source and no source in the user's words, CLAUDE.md or the requirements (`DDP_MED_NS_Level`, `DDP_MED_NS_Code`, `DPP_MED_Environment`, `DPP_MED_Environment_Class`, `DPP_MED_APIURL`, `DPP_MED_TrackingId`, `DPP_MED_TrackedFields`) are open questions 4 to 10. Each one offers "leave unset" as an option, because the evidence shows the facade's map `[MED] CREATE Notification` ran with them empty. No new shapes. See "Facade inputs" and row 21.
- **A Kafka outage must return an error (user: "kafka outage should give an error back").** Evidence from execution 93e06b38: each failed C7 attempt takes about 5 s (the `operation_timeout`), TC-T retries are not immediate on this runtime (gaps of 0 s, 7-13 s), and the runtime cancels a listener execution at about 30-33 s. With retry count 3, the TC-T catch path, the facade and the 500 response never run, and the caller gets nothing. The design now requires every path to end, and return its response, well inside the runtime limit. The TC-T retry count (user Q8 asked for 3) must come down. The new value is open question 2. Whether a lead is still parked on the retry topic before the error is returned is open question 1. The status code for an outage stays 500 (user Q9: "failure 500"). Rows 19, 22 and 23; "Kafka producer settings", "Error handling" and "HTTP response per outcome" are rewritten.
- **The revision 6 statement "retries run immediately, with no back-off" is withdrawn.** It came from the skill reference `try_catch_step.md`, but on this runtime the log shows gaps of up to 13 s between attempts, cause unknown (build log, "Log analysis").
- **API route `/leads/leads` (D5; user: "b").** The current C2 route (object `leads`, URL path empty) also starts C1 for `/ws/rest/gb-cg-leads/v1/leads/leads` (execution bcec584b). The designer cannot specify, from the evidence or the skill references, a C2 route configuration that is proven to reject the extra segment. The skill says an empty route override inherits the value from the WSS operation C3 (whose object is `leads`), so moving `leads` from the object to the URL path would give `/leads/leads` as the effective route, which is worse. This is open question 3. D5 is rewritten so that it does not depend on an unproven configuration.
- **Kafka topics confirmed (user answer 1; CLAUDE.md "Kafka topics must exist before the build").** The user confirmed on 2026-10-09 that both topics exist in Confluent. Topic names are unchanged. The "Topic existence" check now relies on that confirmation, not on platform evidence. New row 25.
- **Connectivity checks first (CLAUDE.md "Connectivity checks first").** New developer check D0, run before anything else in every developer run.
- **D7 partly answered by evidence:** each failed C7 attempt ended at 5042-5165 ms, so `operation_timeout` bounded the whole attempt in the observed failure mode. The cause of the C7 failure is still unknown. The happy path is re-run once the topics exist. If C7 still fails, the developer reports and stops (D8).
- **Row 16 (review only for the failure paths) and follow-ups F2, F3** are kept. If Kafka fails by itself during a `1-DEV` run, the tester records the observed outcome as evidence for F2/F3. Nobody may force a failure.
- **Deployment note (APIM timeout)** updated to the runtime limit.
- `mapping.md` revision 7 adds a "Facade inputs" table.

## Changes in revision 6 (history)

Revision 6 answered the round 1 review findings F-1-01, F-1-02 and F-1-03 and applied the user's decisions "1. copy from CreateLead 2. acks=all, 5s timeout 3. yes", and later "1. a 2. a" (row 19 accepted at the time; `consumer_group` exception, row 20). Revision 6 change list (history):

- **D6 corrected: connection override copied from CreateLead (F-1-01, blocker; user: "1. copy from CreateLead").** The revision 5 premise was wrong. The 17-field block was not used by "45 of 46" account processes: the developer counted 22 processes with a 9-field block, 4 with the 17-field block, 1 with 10 fields, 1 with 9 fields plus xpath (the old CreateLead) and 19 with none (build log, Attempt 3, Decision 6), and the reviewer counted similar numbers. More importantly, the 17 fields had no `xpath` attribute. The skill says such fields are "declared but inert": the extension value is ignored at runtime and the connection's baked-in value is used (`process_extensions.md` § Connection Overrides; `boomi_error_reference.md` Issue #31). Also, 7 of the 17 fields (`saslExtensions` and six `oauth/...` fields) do not exist in the connection component. C1 now copies the `ConnectionOverride` block for c85b494e from account process 1b208fa6 `[Publisher]-[PUB-GB-CG-043]-[CreateLead]-...`, which binds every field with `xpath="GenericConnectionConfig/field[@id='<id>']/@value"`. The developer pulls 1b208fa6 read only and copies the block verbatim, with the same field set. See D6 for the checks.
- **Tracking-field slots named (F-1-02, wording only, no build change).** The user's tracking field `email` (Q7) is bound through the account tracked-field slots `primarykey` = static `Email` and `primaryvalue` = request profile element `email`, on C3, C7 and C8. Row 9, the Components and Connectors tables and the Tracking field test note now name these slots.
- **C7/C8 producer settings recorded (F-1-03; user: "2. acks=all, 5s timeout").** C7 and C8: `acks` = `all` (was `1`), `operation_timeout` = `5000` ms (was `30000`). `client_id` = `gb-cg.leads` and `compression_type` = `snappy` are kept from the framework Produce template 7bfb1b08. New rows 17 and 18 and a "Kafka producer settings" section.
- **Worst-case response time on the failure paths stated honestly, and raised as open question 1.** With a 5 s timeout and TC-T retry count 3, a broker outage can take about 25 s before any response, which is well over the 5 s NFR. The designer does not change the retry count or the timeout; the user decides (row 19).
- **Row 19 closed (user: "1. a"). Superseded in revision 7** by the user's answer "kafka outage should give an error back" and the runtime evidence (rows 19, 22, 23). The 5 s NFR applies to the normal path only (healthy broker, first send succeeds; and the functional-error path). Revision 6 accepted up to about 25 s on Kafka failure paths and added a deployment note for the APIM backend timeout.
- **`consumer_group` not extensible for this process, spec exception (user: "2. a").** The orchestrator compared the local pulled XML read only: the CreateLead (1b208fa6) `ConnectionOverride` for c85b494e has 9 fields (`username`, `password`, `bootstrap_servers`, `service_principal`, `security_protocol`, `sasl_mechanism`, `private_certificate`, `polling_interval`, `polling_delay`); C4 `[Confluent_NL-HQ_Kafka]` has 10 (the same 9 plus `consumer_group`). The user accepted `consumer_group` as not extensible for C1, because a Publisher only produces and `consumer_group` has no effect on a Kafka Produce. New row 20, D6 step 4 changed so the developer does not stop on `consumer_group` but still stops on any other uncovered field, and the Connectors table and "Extensions" test note updated.
- **Developer checks:** D6 rewritten. D7 added for the producer settings. Test notes "Tracking field" and "Extensions" updated, and a "Producer settings" row added.

## Changes in revision 5 (history)

Revision 5. This revision answers the developer's second BLOCKED report, which was raised against revision 4 (evidence: `interfaces/PUB-GB-CG-043/build/build-log.md`, section "Attempt 2"). It applies the user's decisions, which the orchestrator relayed verbatim: "1. b 2. a. fix in CLAUDE.md rule as well as an exception." Everything not listed under "Changes in revision 5" is unchanged from revision 4. The revision 4 change notes are kept below for history.

Revision 5 finalised: the user answered open question 1 (failure-path test approach) verbatim: "C, review only for now". The technical-error path and the retry-send-failure path are verified by review only in this build. V1 for TC-T and V6 for BR-A stay unconfirmed and are recorded as follow-ups F2 and F3. Required value row 16 is closed.

Revision 5 change list (history):

- **Kafka header `Retry-Count` removed from this build (user: "1. b").** The developer found no source showing how the Boomi Kafka connector sets a custom message header. No component in the account sets one, the framework Produce operation (7bfb1b08) has no header field, and the Boomi documentation could not be reached (build log, Attempt 2, V2). Messages are now sent with **no custom headers and no key** on both topics. The Set Properties step "Set Kafka header" is removed from the valid path, and check V2 is withdrawn. The header becomes a follow-up for the future retry mechanism (see "Follow-ups"). The user's original Q13 request is kept on record there.
- **Topics fixed in C7 and C8 (user: "2. a").** Only operations whose action is Listen accept extension overrides (skill `process_extensions.md`; build log, Attempt 2). The Kafka topic is the Produce operation's object type. So `gb-cg.q.leads.in.insert` (C7) and `gb-cg.q.leads.in.retry` (C8) are fixed in the operation components, along with every other C7/C8 operation property. This is an approved exception under CLAUDE.md "SHV Energy build rules" > "Connector extensions" > Exception: "For other operations, such as a Kafka Produce, operation properties (including the Kafka topic, which is the operation's object type) cannot be made extensible and stay fixed in the operation component. The connection those operations use must still have all its settings extensible." Connection `[Confluent_NL-HQ_Kafka]` stays fully extensible through C1's `processOverrides`.
- **Connection extension block (developer note 4). Superseded in revision 6.** Revision 5 said to reuse a 17-field block with no xpath attributes "as it appears in 45 of the 46 account processes". That count was wrong and the block is inert at runtime (review finding F-1-01). See "Changes in revision 6" and D6.
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
  - Technical error: originally 3 retries, then send to the retry topic `gb-cg.q.leads.in.retry` (user Q8: "3 retry on all technical errors ... If tech retries expire after 3 times, also send to retry topic."; topic name, user follow-up B: "Nice name."). **Revision 7:** "kafka outage should give an error back" (user, 2026-10-09). The caller must get an error response before the runtime's execution limit (about 30 s, build log "Log analysis"). The retry count is open question 2 and the retry-topic parking is open question 1.
- The facade `[MED] (sub) CACHE Notification Facade` is called with `DDP_MED_NS_Msg` set to the Try/Catch message in two cases: for a functional error, and when the retry-topic send fails. It is not called on success. It is not called when a technical error is parked on the retry topic (user, follow-up C: "the Try/Catch message in DDP_MED_NS_Msg should contain the functional error and if (very rarely) send to retry topic also fail. Sitecore should get 202"). **Revision 7:** before each facade call, C1 also sets the facade inputs that are available at runtime (user: "set whatever needs to be set and available to you"; see "Facade inputs").
- Downstream consumer (out of scope, separate interface): SUB-GB-CG-043 reads `gb-cg.q.leads.in.insert` and creates the Lead in Salesforce. `[SF_Connector]` belongs to that interface.
- Business criticality: Medium. The data contains customer fields and is sensitive.
- NFRs: maximum API response time 5 s. Volume about 60 calls per day, peak 75 per day, average 525 per week.
- Data validation is outside integration scope (document section 1.2.1). The only "functional" check is that the body is present and is a JSON object (see Error handling).
- Build account: `shvenergynv-6R344K` (user Q6). Build, deploy and test only in environment `1-DEV` (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264), which the user confirmed is development (revision 4: "yes, 1-DEV is dev"). Never production (CLAUDE.md). The test runtime (`shv-energy-test.boomi.cloud`, atom 9beaf0cb) has apiType `advanced` (build log, Attempt 2). That is why the endpoint is an API Service component and not a bare WSS listener.

## Follow-ups (not in this build)

| # | Follow-up | Source |
|---|-----------|--------|
| F1 | Add the Kafka message header `Retry-Count` = `0` to every published message when the retry mechanism is designed. First find out how the Boomi Kafka connector sets a custom header, from Boomi documentation or a working example the user supplies. The original request was "header as 'Retry-COunt': 0 (we will use it later in retry mechanism, not for now)". | user Q13; user revision 5: "1. b" |
| F2 | Confirm **V1 for TC-T** at runtime: an error on the TC-T catch path (a failed send to `gb-cg.q.leads.in.retry`) is caught by the enclosing TC-A. Run the technical-error test (main topic produce fails 1 + N times, where N is the TC-T retry count from row 22; one message on the retry topic, 202, facade not called) and the retry-send-failure test, using option A or B from "Failure-path test approach" or another approach the user approves. Not forced in this build. Revision 7: if Kafka fails by itself during a `1-DEV` run, the tester records the observed outcome as partial F2 evidence. | user, open question 1: "C, review only for now"; revision 7 |
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
| 9 | Tracking field(s) | `email`, bound through two account tracked-field slots: **`primarykey`** (field 33185) = static text `Email`, and **`primaryvalue`** (field 33186) = request profile C5 element `email` (root/email). Both slots are set the same way on the WSS listen operation C3 and on both Kafka produce operations C7 (main topic) and C8 (retry topic). No account tracked field is named `email`, so these slots carry it (revision 6, review F-1-02; build log Attempt 3, Decision 2). | user Q7: "email" (the field); slot names are platform facts from the build log and review |
| 10 | Full process name | `[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]` | CLAUDE.md: Process naming convention (Publisher segments); values from rows 1, 3, 4, 5a, 5b |
| 11 | Full folder path | `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead` | user, revision 4: "2. b" (sandbox path with a new leaf folder `PUB-GB-CG-043-Lead`); CLAUDE.md: Folder path convention (levels from `GB-CG` down) |
| 12 | Kafka connection (reuse) | `[Confluent_NL-HQ_Kafka]`, ID c85b494e-58ab-4591-b946-76a9ec636414, in `SHV Energy N.V./00-ConnectionResources/00-Connections`. Not edited; all settings extensible through C1 except `consumer_group` (row 20) | user, revision 4: "3. a"; user Q14: "yes always reuse"; CLAUDE.md: Connector extensions |
| 13 | Build, deploy and test environment | `1-DEV`, ID 693e8bc2-46f8-4c7f-8259-8dcf6cf0f264, confirmed by the user as development | user, revision 4: "4. yes, 1-DEV is dev."; CLAUDE.md: SHV Energy naming and structure standards (Environment) |
| 14 | Kafka topics fixed in C7/C8 (not extensible) | `gb-cg.q.leads.in.insert` in C7, `gb-cg.q.leads.in.retry` in C8, fixed in the operation components | user, revision 5: "2. a"; CLAUDE.md: SHV Energy build rules, Connector extensions, Exception |
| 15 | Kafka message header | None in this build. `Retry-Count` deferred (F1) | user, revision 5: "1. b" |
| 16 | Failure-path test approach (technical error, retry-send failure) | Option C: not forced in `1-DEV` in this build; verified by review only. V1 for TC-T and V6 for BR-A stay unconfirmed (follow-ups F2, F3). Revision 7: if Kafka fails by itself during a `1-DEV` run, the observed outcome is recorded as partial F2/F3 evidence; nobody forces a failure | user, open question 1: "C, review only for now" |
| 17 | C4 connection override binding in C1 | Copy the `ConnectionOverride` block for c85b494e from account process 1b208fa6 `[Publisher]-[PUB-GB-CG-043]-[CreateLead]-...`: same field set, each field with `xpath="GenericConnectionConfig/field[@id='<id>']/@value"` (D6) | user, revision 6: "1. copy from CreateLead" |
| 18 | C7/C8 Kafka producer settings | `acks` = `all`, `operation_timeout` = `5000` ms (user). `client_id` = `gb-cg.leads`, `compression_type` = `snappy` (kept from framework template 7bfb1b08). Fixed in both operation components | user, revision 6: "2. acks=all, 5s timeout"; client_id and compression: framework template, review F-1-03 (no user change requested) |
| 19 | Response-time target on the technical-error and retry-send-failure paths | **Revision 7.** The 5 s NFR applies to the normal path only (unchanged from revision 6). On a Kafka failure path the caller must get a response (an error for an outage) before the runtime cancels the execution at about 30 s. The design budget is **20 s or less** to leave room for the unexplained retry gaps and the facade. The exact worst case depends on rows 22 and 23 (see "Kafka producer settings"). `operation_timeout` stays 5000 ms | user, 2026-10-09: "kafka outage should give an error back"; runtime limit and gaps: build log "Log analysis" (platform evidence); 20 s budget: designer, subject to approval |
| 20 | `consumer_group` on C4 not extensible for C1 (spec exception to "Connector extensions") | C1 declares the 9 fields of the CreateLead block (`username`, `password`, `bootstrap_servers`, `service_principal`, `security_protocol`, `sasl_mechanism`, `private_certificate`, `polling_interval`, `polling_delay`). `consumer_group` is not declared. Reason: this Publisher only produces to Kafka, and a consumer group has no effect on a Produce operation | user, revision 6 orchestrator question 2: "2. a"; field lists from the orchestrator's read-only comparison of the pulled XML |
| 21 | Facade inputs set by C1 before each facade call | From Boomi execution properties: `DPP_MED_ProcessId` = Process Id, `DPP_MED_ProcessName` = Process Name, `DPP_MED_ExecutionId` = Execution Id, `DPP_MED_AccountId` = Account Id, `DPP_MED_AtomId` = Atom Id, `DPP_MED_AtomName` = Atom Name, `DPP_MED_ContainerId` = Atom Id. `DDP_MED_NS_Msg` = Try/Catch message (unchanged). **OPEN:** `DDP_MED_NS_Level` (Q4), `DDP_MED_NS_Code` (Q5), `DPP_MED_Environment` (Q6), `DPP_MED_Environment_Class` (Q7), `DPP_MED_APIURL` (Q8), `DPP_MED_TrackingId` (Q9), `DPP_MED_TrackedFields` (Q10). See "Facade inputs" | user, 2026-10-09: "set whatever needs to be set and available to you"; input list: build log "Log analysis"; execution properties: skill `parameter_value_types.md` § execution; `DDP_MED_NS_Msg`: CLAUDE.md Cache Notification Facade; rest: OPEN |
| 22 | TC-T retry count | **OPEN (Q2).** Revision 6 had 3 (user Q8). With 3, the runtime cancels the execution before any response (execution 93e06b38), which breaks the user's revision 7 answer | OPEN |
| 23 | Behaviour on a Kafka outage | An error goes back to the caller: HTTP 500 `{"status":"error","message":"Technical error. The lead was not accepted."}`, after the facade call on BR-A branch 1, within the row 19 budget. Whether the lead is first offered to the retry topic (and answered 202 if that send succeeds) is **OPEN (Q1)** | user, 2026-10-09: "kafka outage should give an error back"; 500: user Q9 "failure 500"; parking: OPEN |
| 24 | C2 route configuration so that only `/ws/rest/gb-cg-leads/v1/leads` reaches C1 | **OPEN (Q3).** The current route (object `leads`, empty URL path) also passes `/leads/leads` (execution bcec584b). No configuration proven to reject the extra segment is known to the designer | user, 2026-10-09: "b" (defect, change the route); configuration: OPEN |
| 25 | Kafka topics exist in Confluent | `gb-cg.q.leads.in.insert` and `gb-cg.q.leads.in.retry` confirmed by the user on 2026-10-09 (recorded in `pipeline-state.md`, "Kafka topics confirmed") | user, 2026-10-09: "I have just created gb-cg.q.leads.in.retry and gb-cg.q.leads.in.insert in confluent."; CLAUDE.md: Kafka topics must exist before the build |

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
| C1 | `[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]` | Process | New | Interface folder | Listen process. Process Mode `bridge`, allow simultaneous executions. Declares the connection overrides for C4 (block copied from process 1b208fa6, every field with its xpath, D6) |
| C2 | `PUB-GB-CG-043 Lead API` | API Service component (`webservice`), REST | New | Interface folder | Base API path `gb-cg-leads/v1` (user: "gb-cg-leads/v1"). One REST route: method POST, route object `leads`, **URL path empty**, linked to C1 (revision 5, developer note 3). Revision 7: this route also passes `/leads/leads`; the change is open question 3 (row 24, D5) |
| C3 | `PUB-GB-CG-043 WSS Listen Lead` | Web Services Server operation (`wss`), Listen | New | Interface folder | Object/operation name `leads`. Input: single JSON document (C5). Output: single JSON document (C6). Tracking: `primarykey` = `Email`, `primaryvalue` = C5 element `email` (row 9) |
| C4 | `[Confluent_NL-HQ_Kafka]` (c85b494e-58ab-4591-b946-76a9ec636414) | Kafka connection | Reuse unchanged (user Q14: "yes always reuse"; revision 4: "3. a") | `SHV Energy N.V./00-ConnectionResources/00-Connections` | Not edited. All its settings are declared extensible on process C1 (see Connectors) |
| C5 | `PUB-GB-CG-043 Lead Request JSON` | JSON profile | New | Interface folder | Built from the corrected sample (see `mapping.md`). Field `additional-comments` (user Q11) |
| C6 | `PUB-GB-CG-043 Lead Response JSON` | JSON profile | New | Interface folder | `{"status": "...", "message": "..."}` (see `mapping.md`) |
| C7 | `PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.insert` | Kafka operation, Produce | New (user Q15: "new opretaion. always") | Interface folder | Topic `gb-cg.q.leads.in.insert`, **fixed** (not extensible, CLAUDE.md exception). No header, no key. `acks` `all`, `operation_timeout` `5000`, `client_id` `gb-cg.leads`, `compression_type` `snappy` (row 18). Tracking: `primarykey` = `Email`, `primaryvalue` = C5 element `email` (row 9) |
| C8 | `PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.retry` | Kafka operation, Produce | New (user Q15; follow-up B) | Interface folder | Topic `gb-cg.q.leads.in.retry`, **fixed** (not extensible, CLAUDE.md exception). Used only on the technical-error path. No header, no key. Producer settings as C7 (row 18). Tracking as C7 (row 9) |
| C9 | `[MED] (sub) CACHE Notification Facade` (338df4f8-af86-44f9-855c-943d8d0d478f) | Process (subprocess) | Reuse, read only (user Q16: "reuse, always") | `SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/00-SharedLibrary_v4/00-Version_4.0 (2019-12-28-baseline)/01-Facade/02-Process` | Called by Process Call (wait = true, abort = true) on branch 1 of a Branch shape. It has no Return Documents shape, so the Process Call has no return paths. Not edited |

Topics:

| Topic | Use | Source |
|-------|-----|--------|
| `gb-cg.q.leads.in.insert` | Main topic. Every accepted lead goes here | user: design document section 1.3.2 |
| `gb-cg.q.leads.in.retry` | Parking topic, **for technical errors after the TC-T retries only** (retry count: row 22; whether parking stays: Q1). Functional errors are not sent here | user, follow-up B: "Nice name."; user revision 3 correction: "This message do not go to retry topic." |

Because the topics are fixed in C7 and C8, the same topic names are used in every environment the process is promoted to (user, revision 5: "2. a"). If a later environment needs different topic names, the operation components must be changed in that release.

Prerequisite (CLAUDE.md: Kafka topics must exist before the build): both topics must exist in Confluent Kafka before the build. **The user confirmed this on 2026-10-09** ("I have just created gb-cg.q.leads.in.retry and gb-cg.q.leads.in.insert in confluent."; row 25). Nobody infers topic existence from the platform, from earlier executions or from another interface, and nobody creates topics. If a later design change names another topic, the orchestrator must get the user's confirmation for it before the build.

## Process design

Start shape: Web Services Server listen, using operation C3, exposed through API Service component C2.

Main path (TC-A, TC-T and TC-F are the labels for the three Try/Catch shapes; BR-F and BR-A are the two Branch shapes):

1. **Start** (WSS listen, C3).
2. **TC-A** Try/Catch "Retry-topic send failure", retry count 0, catch All errors. The try path continues with step 3.
3. **Data Process, Custom Scripting "Check JSON body"** (script S1): sets `DDP_VALIDATION_ERROR`. The document passes through unchanged.
4. **Decision "Body is valid JSON?"**: `DDP_VALIDATION_ERROR` equals empty.
   - **True (valid)**: go to 5.
   - **False (functional error)**: go to 6.
5. Valid path (revision 5: the "Set Kafka header" step is removed. Revision 7: retry count and catch path depend on Q1 and Q2):
   1. **TC-T** Try/Catch "Technical", **retry count N = OPEN (Q2, row 22)**, catch All errors. Revision 6 had 3; 3 cannot finish inside the runtime limit.
   2. Try: **Kafka Produce** (C4 + C7, topic `gb-cg.q.leads.in.insert`), body unchanged, no headers, no key.
   3. **Set Properties "Response 202"**: HTTP response status code 202.
   4. **Message "Accepted"**: `{"status":"accepted"}`.
   5. **Return Documents "Accepted"**.
   6. TC-T Catch (1 + N main attempts failed). **Shown as Q1 option a (keep parking, the designer's recommendation).** **Kafka Produce** (C4 + C8, topic `gb-cg.q.leads.in.retry`), original body unchanged, no headers, no key. If this send fails (a Kafka outage normally fails both topics), the error goes to TC-A, which returns 500 (step 7).
   7. **Set Properties "Response 202 (parked)"**: HTTP status 202.
   8. **Message "Accepted (parked)"**: `{"status":"accepted"}`.
   9. **Return Documents "Accepted - parked on retry topic"**.
   - If the user picks **Q1 option b (no parking)**, steps 5.6 to 5.9 are replaced by one **Exception step "Technical error"** (stop single document = true, message = Meta information "Base - Try/Catch Message"). TC-A catches it and returns 500 through BR-A (step 7). C8 is then not used by the process. The developer would not delete C8 without a further spec instruction.
6. Functional-error path (no Kafka send, no retry):
   1. **TC-F** Try/Catch "Functional", retry count 0, catch All errors.
   2. Try: **Exception step "Functional error"** (stop single document = true), message = `DDP_VALIDATION_ERROR`. TC-F catches it, so the Try/Catch message holds the functional error.
   3. TC-F Catch: **Branch BR-F "Notify then reject"**, 2 branches (`numBranches="2"`).
   4. BR-F branch 1:
      1. **Set Properties "Set facade inputs"** (renamed from "Set DDP_MED_NS_Msg" in revision 7): `DDP_MED_NS_Msg` = Meta information "Base - Try/Catch Message" (`meta.base.catcherrorsmessage`), plus the facade inputs in "Facade inputs" (functional-error values where the table has per-path values).
      2. **Process Call** `[MED] (sub) CACHE Notification Facade` (C9), wait = true, abort = true, no return paths. Branch 1 ends here.
   5. BR-F branch 2 (runs after branch 1 completes):
      1. **Set Properties "Response 400"**: HTTP status 400.
      2. **Message "Rejected"**: `{"status":"rejected","message":"<Try/Catch message>"}`. The `message` value comes from Meta information "Base - Try/Catch Message" and not from `DDP_MED_NS_Msg`, because a DDP set on branch 1 does not reach branch 2.
      3. **Return Documents "Rejected - functional error"**.
7. TC-A Catch (an error on the TC-T catch path, in practice a failed send to the retry topic during a Kafka outage, or the "Technical error" Exception step if Q1 option b is chosen; or, very rarely, an error on the TC-F catch path such as a failing facade call on BR-F branch 1):
   1. **Branch BR-A "Notify then error"**, 2 branches (`numBranches="2"`).
   2. BR-A branch 1:
      1. **Set Properties "Set facade inputs"** (renamed in revision 7): `DDP_MED_NS_Msg` = Meta information "Base - Try/Catch Message", plus the facade inputs in "Facade inputs" (technical-error values where the table has per-path values).
      2. **Process Call** `[MED] (sub) CACHE Notification Facade` (C9), wait = true, abort = true, no return paths. Branch 1 ends here.
   3. BR-A branch 2 (runs after branch 1 completes):
      1. **Set Properties "Response 500"**: HTTP status 500.
      2. **Message "Error"**: `{"status":"error","message":"Technical error. The lead was not accepted."}`. The text is fixed so that no sensitive data or connection detail is returned.
      3. **Return Documents "Error"**.

Each outcome ends in its own Return Documents shape: four in total. No two outcomes converge on one step. Every Branch dragpoint is wired. The Process Calls have no outgoing connections because the facade returns no documents. There are no Notify shapes.

Shape count summary (Q1 option a): Try/Catch 3 (TC-A, TC-T, TC-F), Branch 2 (BR-F, BR-A), Process Call 2, Return Documents 4, Exception 1, Decision 1, Data Process 1, Kafka connector steps 2. With Q1 option b: Return Documents 3, Exception 2, Kafka connector steps 1. No new shape types in revision 7; the facade inputs are added to the two existing Set Properties steps.

### Developer checks, run first

These cover facts about the platform and environment that the local skill references do not document, or that the design depends on. Check them first, in `1-DEV`. If any check fails, do not redesign and do not add a fourth Try/Catch. Stop and return to the orchestrator.

- **D0. Connectivity checks first (revision 7; CLAUDE.md "Connectivity checks first").** Before any other step in every run (build or fix): `boomi-env-check.sh` and `boomi-folder-create.sh --test-connection`; report the runtime endpoint credentials (`SERVER_AUTH_TYPE`, `SERVER_USERNAME`, `SERVER_TOKEN` or `SERVER_BEARER_TOKEN`) only as SET or EMPTY; confirm network access to every host the run needs, including the `1-DEV` runtime `shv-energy-test.boomi.cloud` and `platform.boomi.com` for execution log downloads. If any check fails, stop and return `BLOCKED: connectivity` before creating, changing or deploying anything. On an auth error, do not retry.
- **D1. Environment.** Build, deploy and test only in `1-DEV` (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264). The user confirmed it is development. Passed in Attempt 2.
- **D2. Folder.** The parent `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/GB-CG/Enterprise Projects/Customer Portal/Publisher` exists. Create the new leaf `PUB-GB-CG-043-Lead` under it. Do not use or change the existing `PUB-GB-CG-043-leads`.
- **D3. Reused connection.** Pull `[Confluent_NL-HQ_Kafka]` (c85b494e-58ab-4591-b946-76a9ec636414) read only. Do not edit or push it. Its `1-DEV` extension values must already be set. Passed in Attempt 2 (username and password set; other fields use the component defaults, which are non-empty). Do not supply connection values or credentials. Connection extension values are shared by every process in the environment that uses this connection, so never change them, including during tests.
- **D4. Facade runtime (revision 7).** The route target `[MED] (sub) CACHE Notification` (47e2da88) is deployed and runs in `1-DEV` (build log, "Log analysis"), so the revision 6 route-target concern is closed. The failure in execution 22c61363 was the empty `DPP_MED_ProcessId`. Set the facade inputs on both "Set facade inputs" steps exactly as the "Facade inputs" table says, with Execution property values (`valueType="execution"`, title case, for example `Process Id`). Then run one functional-error test and confirm in the process log that the route target's Document Cache Load completes and that the 400 response comes back from BR-F branch 2. If the facade path fails on another empty input, stop and return to the orchestrator with the exact error and property name; do not set a value the spec does not give. Do not deploy, edit or push shared framework components (338df4f8, 76eb8a3a, 47e2da88, 911b9276).
- **D5. API route (revision 7, pending Q3).** The revision 5 route (object `leads`, empty URL path) passes both `/ws/rest/gb-cg-leads/v1/leads` (execution 93e06b38) and `/ws/rest/gb-cg-leads/v1/leads/leads` (execution bcec584b). Do not change C2 until Q3 is answered and this check is rewritten. Do not try `objectName=""` with `urlPath="leads"`: an empty override inherits the object `leads` from C3 (skill `api_service_component.md`, "URL Path Construction"), which would make the effective route `/leads/leads`. Until then, the check is: POST `/ws/rest/gb-cg-leads/v1/leads` reaches C1.
- **D6. Connection override block (revision 6, replaces the revision 5 text; user: "1. copy from CreateLead").** The revision 5 instruction (17 fields, no xpath, "45 of 46" processes) was wrong and is withdrawn (review F-1-01).
  1. Pull account process 1b208fa6 `[Publisher]-[PUB-GB-CG-043]-[CreateLead]-...` **read only**. Do not edit, push or deploy it.
  2. In C1's `processOverrides`, replace the current 17-field `ConnectionOverride` for c85b494e with the `ConnectionOverride` block for c85b494e from 1b208fa6, copied verbatim: the same field set, `label`, `overrideable` and `xpath` values, each `xpath` in the form `GenericConnectionConfig/field[@id='<id>']/@value`. Do not hand-author fields, add fields or drop fields. The build log records this block as 9 fields with xpath (Attempt 3, Decision 6); use what the pulled 1b208fa6 actually contains.
  3. Confirm that **every copied field id exists** in the pulled C4 component (`GenericConnectionConfig/field[@id='<id>']`). If any copied field does not exist in C4, stop and return to the orchestrator.
  4. List any C4 connection field that the copied block does **not** cover, and record the list in the build log. **`consumer_group` is expected to be uncovered and is accepted** (row 20; user: "2. a"): do not stop on it and do not add it. If any **other** C4 field is not covered, stop and return to the orchestrator with the field id. Do not add it yourself, because CLAUDE.md requires all connection settings to be extensible and the skill forbids hand-authoring override fields.
  5. Do not declare any operation overrides for C7 or C8 (CLAUDE.md: Connector extensions, Exception).
  6. After pushing and redeploying C1, run `boomi-extensions.sh get` and confirm that the c85b494e connection fields are present in `1-DEV` and that the c85b494e extension values are unchanged (same hash before and after, as in Attempt 3). Do not run `set`. Note: once the binding has xpaths, the existing `1-DEV` extension values for c85b494e take effect at runtime for C1, as they already do for 1b208fa6. That is the intended behaviour.
- **D7. Producer settings (revision 6; user: "2. acks=all, 5s timeout").** In C7 and C8 set `acks` = `all` and `operation_timeout` = `5000`. Keep `client_id` = `gb-cg.leads` and `compression_type` = `snappy`. No other C7/C8 field changes (no header, no key, no partition). Record in the build log whether the connector's `operation_timeout` bounds the whole send, including any wait for broker metadata. If the documentation or an account precedent shows it does not, record that in the build log and continue; do not add other producer settings that the spec does not list. **Revision 7:** passed for the components (C7 v2, C8 v2). Partial runtime evidence: each failed C7 attempt in executions 93e06b38 and bcec584b ended at 5042-5165 ms, so the timeout bounded the attempt in that failure mode. Runtime acceptance of `acks` = `all` is still unconfirmed until a produce succeeds.
- **D8. Happy path after topic confirmation (revision 7).** Topics are confirmed by the user (row 25). Re-run the happy-path test once. If C7 succeeds, confirm 202 within 5 s. If C7 still fails, the run is a natural Kafka failure: record the total execution time, the HTTP status and body the caller received, and which shapes ran (C8, facade, BR-A). The caller must get a response before the runtime limit (rows 19, 23). Then get the Kafka error text if any tool shows it, record it, and stop and return to the orchestrator. Do not run the happy path again to "try" settings, do not change `acks`, the timeout or the connection, and do not conclude that a topic is missing.
- **V1.** An error raised on the catch path of an inner Try/Catch (TC-T or TC-F), including on a Branch below it, must be caught by the enclosing TC-A. If the platform does not behave this way, the design would need a fourth Try/Catch. Do not add one. Stop and return to the orchestrator (CLAUDE.md: Error handling). In this build V1 for TC-T is **not confirmed at runtime** (user: "C, review only for now"). The reviewer checks only that the TC-T catch path sits inside the TC-A try path. Runtime confirmation is follow-up F2. The TC-F part of V1 arises only if the facade call on BR-F branch 1 fails, and no test in this build exercises it.
- **V2. Withdrawn in revision 5.** No Kafka header is set in this build (user: "1. b"; follow-up F1).
- **V3.** HTTP response status: set it with the Web Services Server response status-code document property (Set Properties, Connector properties, Web Services Server). This is not documented locally. Confirm the exact property against Boomi documentation or an existing account process that sets it. Confirm the status in the first test of each outcome.
- **V4. Resolved in revision 4.** The branch fix puts the response on branch 2, so it does not depend on the facade returning a document.
- **V5.** The Exception step's text must reach the TC-F Try/Catch message as `Functional error: ...`, and that same text must be readable on BR-F branch 2. Confirm in the test log and in the 400 body.
- **V6.** After the Process Call on branch 1 returns, the runtime runs branch 2. Confirm in the process log that, for one request, the facade runs first and then the 400 (or 500) Return Documents step runs. Confirm that the HTTP response contains only the branch 2 document. In this build V6 is confirmed for **BR-F only**, by the functional-error test. V6 for BR-A is **not confirmed at runtime** (user: "C, review only for now"). The reviewer checks the BR-A structure instead, and runtime confirmation is follow-up F3.
- **Base path uniqueness.** Passed in Attempt 2: no API Service in the account uses `gb-cg-leads/v1`. Recheck just before deploying.
- **Topic existence (revision 7; CLAUDE.md "Kafka topics must exist before the build").** The user confirmed both topics on 2026-10-09 (row 25; `pipeline-state.md` "Kafka topics confirmed"). Before building, check that `pipeline-state.md` still records that confirmation for exactly these two topic names. If it does not, stop and return to the orchestrator. Never infer topic existence from the platform, from executions or from another interface, and never create a topic.

### HTTP response per outcome

| Outcome | Kafka result | Facade called | HTTP status | Response body |
|---------|--------------|---------------|-------------|---------------|
| Valid body, main topic send succeeds (first try or within N retries; N from row 22) | Message on `gb-cg.q.leads.in.insert` | No | 202 | `{"status":"accepted"}` |
| Valid body, main topic fails 1 + N times, retry topic send succeeds (Q1 option a only) | Message on `gb-cg.q.leads.in.retry` | No | 202 | `{"status":"accepted"}` |
| **Kafka outage**: valid body, main topic fails 1 + N times, and the retry topic send also fails (Q1 option a) or is not attempted (Q1 option b) | None | Yes, once (BR-A branch 1). `DDP_MED_NS_Msg` = the last Kafka error | 500 (BR-A branch 2), within the row 19 budget | `{"status":"error","message":"Technical error. The lead was not accepted."}` |
| Functional error (body missing, empty, not valid JSON, or not a JSON object) | None. No retry and no topic | Yes, once (BR-F branch 1). `DDP_MED_NS_Msg` = functional error | 400 (BR-F branch 2) | `{"status":"rejected","message":"<functional error>"}` |
| Functional error and the facade call on BR-F branch 1 fails (very rare) | None | Attempted on BR-F branch 1. BR-F branch 2 does not run. TC-A catches the facade error and calls the facade again on BR-A branch 1 | 500 (BR-A branch 2) | `{"status":"error","message":"Technical error. The lead was not accepted."}` |
| Any TC-A case where the facade call on BR-A branch 1 also fails (very rare) | As above | Attempted, failed | Runtime default error status (not set by the process) | Runtime default. BR-A branch 2 does not run and there is no enclosing Try/Catch |
| Not authenticated | Not reached. APIM or the API Service runtime rejects the call before the process runs | No | 401 (runtime) | Runtime default |
| Any execution still running when the runtime limit (about 30 s) is reached | Whatever completed before the cancel | Only if reached before the cancel | None. The runtime cancels the execution and the caller gets no response (execution 93e06b38) | None |

The last row is not a designed outcome. It is what the runtime does, and the design must keep every path well inside the limit (rows 19, 22). A Try/Catch cannot catch the cancellation: in 93e06b38 TC-A sent the document to its error path and the runtime cancelled straight away.

Sources: 202 with the `{"status":"accepted"}` body, 500 with an error message, and 400 as an allowed response all come from user Q9 ("Yes, all 3 are acceptable solution"). 202 after parking a technical failure comes from follow-up C ("Sitecore should get 202"). 400 for a functional error comes from the orchestrator's follow-up C proposal ("Sitecore 400"), which the user did not change and which the revision 3 relay confirms. 500 for a retry-send failure follows Q9 "failure 500", and is the error that a Kafka outage returns (user, 2026-10-09: "kafka outage should give an error back"). The two facade-failure rows are not user decisions. They are what the accepted Try/Catch structure and the user's branch fix do when the facade fails.

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
| TC-A "Retry-topic send failure" | 0 | Everything after Start | Branch BR-A: (1) "Set facade inputs" (`DDP_MED_NS_Msg` = Try/Catch message, plus "Facade inputs") -> facade; (2) HTTP 500 -> Return Documents "Error" |
| TC-T "Technical" | **N = OPEN (Q2, row 22)**. Revision 6: 3 (user Q8) | Main topic produce and the 202 response | Q1 option a: produce to the retry topic -> HTTP 202 -> Return Documents "Accepted - parked on retry topic"; a failed retry send goes to TC-A (500). Q1 option b: Exception step "Technical error" -> TC-A (500) |
| TC-F "Functional" | 0 (user Q8: "No retry on functional error") | Exception step raising the functional error | Branch BR-F: (1) "Set facade inputs" (`DDP_MED_NS_Msg` = Try/Catch message (functional error), plus "Facade inputs") -> facade; (2) HTTP 400 with the Try/Catch message -> Return Documents "Rejected - functional error". No Kafka send (user revision 3 correction) |

Definitions:

- **Functional error**: the request body is missing or empty, is not valid JSON, or is not a JSON object. No other content validation is done, because validation is out of scope per the document. This is the orchestrator's follow-up C definition, and the user did not change it.
- **Technical error**: any error on the TC-T try path. In practice this is a Kafka produce failure on the main topic.

**Revision 7 correction.** Revision 6 said TC-T retries run immediately, with no back-off (skill reference `try_catch_step.md`). On the `1-DEV` runtime they do not: the gaps between attempts were 0 s, 11 s and 7 s (93e06b38) and 0 s, 13 s and 1 s (bcec584b), cause unknown. Each failed Kafka attempt also takes about 5 s (the `operation_timeout`). The runtime cancels a listener execution at about 30-33 s, and no Try/Catch can catch that. So the retry count must be low enough that the whole failure path, including the facade, ends inside the row 19 budget (see "Kafka producer settings"). On the 400 and 500 paths the facade's run time also counts, because branch 2 starts only after branch 1 completes.

## Cache Notification Facade

- Called from two places. Each call is on branch 1 of a Branch shape and is preceded on that branch by the Set Properties step "Set facade inputs", which sets `DDP_MED_NS_Msg` to Meta information "Base - Try/Catch Message" and the other inputs in "Facade inputs" below:
  1. BR-F branch 1 (TC-F catch path): the message is the functional error. BR-F branch 2 then returns the 400 response. Nothing is sent to Kafka.
  2. BR-A branch 1 (TC-A catch path): the message is the Kafka outage error (the failed retry-topic send, or the "Technical error" Exception if Q1 option b is chosen), or, very rarely, a facade failure on BR-F branch 1. BR-A branch 2 then returns the 500 response.
- Not called on the success path or on the TC-T catch path (user, follow-up C).
- In normal operation the facade runs at most once per request. It runs twice only if the facade call on BR-F branch 1 itself fails (see "HTTP response per outcome").
- Facade: `[MED] (sub) CACHE Notification Facade` (338df4f8-af86-44f9-855c-943d8d0d478f) at `SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/00-SharedLibrary_v4/00-Version_4.0 (2019-12-28-baseline)/01-Facade/02-Process` (CLAUDE.md; user Q16: "reuse, always"). Process Call with wait = true and abort = true, and no return paths, because the facade ends both of its paths in Stop and has no Return Documents shape. The facade is read only. If it changes, the parent C1 must be redeployed.

### Facade inputs (revision 7)

User: "set whatever needs to be set and available to you." The input list is the developer's evidence (build log, "Log analysis", execution 22c61363): the facade's "Input:" description list, the route target 47e2da88 XML and the PropertyGet functions in map `[MED] CREATE Notification` (911b9276). Facts from that evidence:

- Only `DPP_MED_ProcessId` is proven fatal. The route target copies it into `DDP_MED_ProcessId`, the index key of a Document Cache, and the cache load fails when it is empty.
- The map `[MED] CREATE Notification` ran without error with every other input empty. Shapes after the failing cache load have not run yet, so it is not proven that they accept empty inputs. D4 covers this.
- DPPs are process-wide, so values set in C1 reach the facade and its Process Route target. That is how `DPP_MED_ProcessCallStack` showed C1's name in the route target's log.

All values are set in the existing Set Properties step "Set facade inputs" on BR-F branch 1 and on BR-A branch 1, before the Process Call. No new shapes and no scripts. "Execution property" means a Set Properties source value of type Execution Property (`valueType="execution"`, skill `parameter_value_types.md` § execution). These are read from the runtime when the step runs, so in C1 they describe C1 and its execution.

| # | Property | Kind | Value | Source |
|---|----------|------|-------|--------|
| FI-1 | `DDP_MED_NS_Msg` | DDP | Meta information "Base - Try/Catch Message" (`meta.base.catcherrorsmessage`) | CLAUDE.md: Cache Notification Facade (unchanged) |
| FI-2 | `DPP_MED_ProcessId` | DPP | Execution property `Process Id` | user: "set whatever needs to be set and available to you"; fatal input (22c61363) |
| FI-3 | `DPP_MED_ProcessName` | DPP | Execution property `Process Name` | as FI-2 |
| FI-4 | `DPP_MED_ExecutionId` | DPP | Execution property `Execution Id` | as FI-2 |
| FI-5 | `DPP_MED_AccountId` | DPP | Execution property `Account Id` | as FI-2 |
| FI-6 | `DPP_MED_AtomId` | DPP | Execution property `Atom Id` | as FI-2 |
| FI-7 | `DPP_MED_AtomName` | DPP | Execution property `Atom Name` | as FI-2 |
| FI-8 | `DPP_MED_ContainerId` | DPP | Execution property `Atom Id`. "Container" is Boomi's older name for a runtime (Atom, Molecule or Cloud attachment), and the Boomi Platform API calls the runtime ID the container ID. There is no separate `Container Id` execution property | as FI-2; platform fact. If the user knows the framework expects something else here, they can correct it at approval |
| FI-9 | `DDP_MED_NS_Level` | DDP | **OPEN (Q4)**. Per path: functional error (BR-F) and technical error (BR-A) | OPEN |
| FI-10 | `DDP_MED_NS_Code` | DDP | **OPEN (Q5)**. Per path, as FI-9 | OPEN |
| FI-11 | `DPP_MED_Environment` | DPP | **OPEN (Q6)** | OPEN |
| FI-12 | `DPP_MED_Environment_Class` | DPP | **OPEN (Q7)** | OPEN |
| FI-13 | `DPP_MED_APIURL` | DPP | **OPEN (Q8)** | OPEN |
| FI-14 | `DPP_MED_TrackingId` | DPP | **OPEN (Q9)** | OPEN |
| FI-15 | `DPP_MED_TrackedFields` | DPP | **OPEN (Q10)** | OPEN |

Rules for the developer:

- Set every row the same way on both branches, except FI-9 and FI-10, which may differ by path once Q4 and Q5 are answered.
- Order inside the step: FI-1 first, then the rest in table order.
- A row answered "leave unset" is not set at all (not set to an empty string).
- No credential and no customer data goes into these properties unless the user's answer to Q9 or Q10 explicitly puts the `email` value there.
- Do not copy values from other processes or from the framework's map defaults.

## Connectors

| Connection / operation | Purpose | Extensible settings | Tracking field |
|------------------------|---------|---------------------|----------------|
| C3 WSS listen operation | Receive the Sitecore lead JSON | No connection component. Every operation field the platform allows to be extended is extended (CLAUDE.md: Connector extensions; Listen operations accept overrides). The object name and profiles are the API contract. No platform-generated WSS operation override exists in the account to copy, so none is declared (build log Decision 5; review EXT-02 PASS). | `primarykey` = `Email`, `primaryvalue` = `email` |
| C4 `[Confluent_NL-HQ_Kafka]` (c85b494e-58ab-4591-b946-76a9ec636414, reused, not edited) | Kafka (Confluent) connection | All connection settings are declared in C1's `processOverrides` by copying the `ConnectionOverride` block for c85b494e from process 1b208fa6 (CreateLead), each field bound with `xpath="GenericConnectionConfig/field[@id='<id>']/@value"` (user, revision 6: "1. copy from CreateLead"; D6). That block covers 9 of C4's 10 fields. **Exception: `consumer_group` is not extensible for C1** (row 20; user: "2. a"), because a Publisher only produces and a consumer group has no effect on a Produce. Values are set per environment through Environment Extensions. They are never written into XML or this spec. The shared connection is not modified. In `1-DEV` the existing values are used as they are and never changed (D3). | n/a |
| C7 Kafka Produce, main | Publish to `gb-cg.q.leads.in.insert` | **None (approved exception).** Produce is not a Listen operation, so no operation property can be extended. The topic and all other operation properties, including the producer settings in "Kafka producer settings", are fixed in C7 (user, revision 5: "2. a"; CLAUDE.md: SHV Energy build rules, Connector extensions, Exception). No environment-specific connection value is in C7. | `primarykey` = `Email`, `primaryvalue` = `email` |
| C8 Kafka Produce, retry | Publish to `gb-cg.q.leads.in.retry` (technical errors only) | **None (approved exception)**, as for C7. | `primarykey` = `Email`, `primaryvalue` = `email` |
| `[SF_Connector]` | Not used. It belongs to SUB-GB-CG-043. | n/a | n/a |

Message key: none. Message headers: none in this build (user, revision 5: "1. b"; follow-up F1).

### Kafka producer settings (C7 and C8, revision 6)

| Field | Value | Source |
|-------|-------|--------|
| `acks` | `all` | user, revision 6: "2. acks=all" |
| `operation_timeout` | `5000` (ms) | user, revision 6: "5s timeout" |
| `client_id` | `gb-cg.leads` | framework Produce template 7bfb1b08 (build log Decision 4). Not environment-specific. Kept, no reason found to change it |
| `compression_type` | `snappy` | framework Produce template 7bfb1b08. Kept, no reason found to change it |

These values are the same in every environment, so fixing them in the operation components does not breach "Connector extensions" (review EXT-03 PASS).

Effect of `acks` = `all`: the broker acknowledges a send only after all in-sync replicas have it, so an acknowledged lead is not lost if the partition leader fails. A send can be a little slower, and it fails if too few in-sync replicas are available. Such a failure is a technical error and follows the TC-T path.

**Worst-case response time on a Kafka failure (revision 7, from runtime evidence).** Measured in `1-DEV` (build log, "Log analysis"): each failed C7 attempt took about 5 s; the gap before the first retry was 0 s in both runs; later gaps were 1-13 s, cause unknown; the runtime cancelled the execution at about 30-33 s. The facade's full run time is not yet measured (its failed run in 22c61363 took under 1 s for two calls). The estimates below assume C8 behaves like C7 during an outage (about 5 s) and, for the upper figure, a 13 s gap before every retry after the first.

| TC-T retry count N | Outage path with Q1 option a (park attempt, then 500) | Outage path with Q1 option b (no park, 500) | Fits the 20 s budget (row 19)? |
|--------------------|------------------------------------------------------|---------------------------------------------|--------------------------------|
| 0 | 5 + 5 = about 10 s + facade | about 5 s + facade | Yes, with a wide margin |
| 1 | 5 + 0 + 5 + 5 = about 15 s + facade; up to about 28 s + facade if a 13 s gap occurs before the retry (not seen so far) | about 10 s + facade; up to about 23 s + facade | Yes on the observed timing; at risk if a long gap occurs before the first retry |
| 2 | about 20 s + facade with no gaps; about 31-33 s + facade with the gap seen before retry 2 in both runs (11 s, 13 s) | about 15 s + facade with no gaps; about 26-28 s + facade with the observed gap | No |
| 3 (revision 6) | Cancelled by the runtime before any response (93e06b38) | Same | No |

Other points:

- Happy path, broker healthy: one main send, normally well under 5 s. A main send that recovers on retry n costs about (n + 1) x 5 s plus gaps.
- The functional-error path has no Kafka send; it costs the facade run time only.
- A send that times out may still have reached the broker. With retries, the same lead can appear more than once on the main topic, or on both topics. The downstream SUB-GB-CG-043 should tolerate duplicates. This is noted for information only and does not change this build.
- The designer does not change `operation_timeout` (user, revision 6: "5s timeout") or add a wait between retries.

The retry count is open question 2 and the parking choice is open question 1.

### Deployment note: APIM backend timeout

For the user and the APIM team (not a Boomi build step). Revision 7: Boomi now aims to answer every request, including a Kafka outage, within about 20 s, and the `1-DEV` runtime cancels a listener execution at about 30 s. The Azure APIM backend timeout for the operation that calls `/ws/rest/gb-cg-leads/v1/leads` should therefore be **at least 30 s**, so that APIM never cuts off a Boomi response that is still on its way. If it is shorter than the Boomi worst case, Sitecore sees a gateway timeout for a lead that Boomi may still park on the retry topic. The developer and tester do not change APIM; the tester records this note as a pre-production action for the user.

## Scripts

| Script | Single purpose |
|--------|----------------|
| S1 "Check JSON body" (Groovy, Data Process Custom Scripting) | For each document, read the body. If it is empty or whitespace, set `DDP_VALIDATION_ERROR` = `Functional error: request body is empty`. Otherwise parse it with `JsonSlurper`. If parsing fails, set `Functional error: request body is not valid JSON`. If the result is not a JSON object, set `Functional error: request body is not a JSON object`. Otherwise set it to empty. The script never throws, and it passes the document through unchanged. Accepted by the user (revision 3 relay). |

No other scripting. Status codes and response bodies use Set Properties and Message steps. Message step JSON uses the single-quote escaping rule (skill Issue #1).

## Failure-path test approach

**Decision: option C (user: "C, review only for now").** In this build the technical-error path (TC-T retries, then the retry topic) and the retry-send-failure path (TC-A catch, BR-A, facade, 500) are verified by review only. They are not run in `1-DEV`. Options A and B are kept below for the later runtime tests (follow-ups F2 and F3).

Review checklist for these two paths (the reviewer checks the built C1 XML and records the evidence in `review/findings.md`; the tester refers to it):

- R1. TC-T has retry count N (row 22; revision 6 had 3) and catches All errors. Its try path holds only the C7 produce, Set Properties "Response 202", Message "Accepted" and Return Documents "Accepted".
- R2. Q1 option a: the TC-T catch path goes to the C8 produce (topic `gb-cg.q.leads.in.retry`, fixed in C8), then Set Properties "Response 202 (parked)", Message "Accepted (parked)" and Return Documents "Accepted - parked on retry topic". There is no facade call, no Set Properties for `DDP_MED_NS_Msg` and no header or key on this path. Q1 option b: the TC-T catch path holds only the Exception step "Technical error".
- R3. TC-T (with its catch path) sits inside the TC-A try path, so an error on the TC-T catch path can reach TC-A. Runtime behaviour is unconfirmed (V1 for TC-T, F2).
- R4. TC-A has retry count 0 and catches All errors. Its catch path goes to Branch BR-A with `numBranches="2"` and both dragpoints wired.
- R5. BR-A branch 1: Set Properties "Set facade inputs" (`DDP_MED_NS_Msg` = Meta information "Base - Try/Catch Message", then the "Facade inputs" rows), then a Process Call to C9 (338df4f8) with wait = true, abort = true and no return paths.
- R6. BR-A branch 2: Set Properties HTTP status 500, Message `{"status":"error","message":"Technical error. The lead was not accepted."}`, Return Documents "Error". Runtime order and single-document response are unconfirmed (V6 for BR-A, F3).

Background (from revision 5): topics are fixed in C7 and C8, so they can no longer be broken through operation extensions. The shared connection and its `1-DEV` extension values must not be changed (D3). The technical-error and retry-send-failure paths need a Kafka produce to fail without touching either of those. These were the three options:

- **Option A: block topic writes on the Kafka side (recommended).** The Confluent cluster administrator temporarily removes write (produce) permission for the `1-DEV` Kafka principal used by `[Confluent_NL-HQ_Kafka]`, on these topics only:
  - Technical-error test: remove write on `gb-cg.q.leads.in.insert` only. Expected: 1 + N failed attempts on the main produce (N from row 22; revision 5 text said 3), one message on `gb-cg.q.leads.in.retry`, 202 `{"status":"accepted"}`, facade not called.
  - Retry-send-failure test: remove write on both topics. Expected: 1 + N failed main attempts, a failed retry-topic send, BR-A branch 1 calls the facade once, BR-A branch 2 returns 500. This also confirms V1 for TC-T and V6 for BR-A.
  - The administrator restores the permissions straight after each test.
  - This tests the real deployed C1 through the real endpoint with no Boomi change. It affects only these two new topics, which no other publisher writes to, and it does not change read access for SUB-GB-CG-043. It needs someone outside Boomi with Confluent admin rights. The 5 s response-time check does not apply to these two tests.
- **Option B: temporary test harness in Boomi.** The developer makes a temporary copy of C1, in a test subfolder of the interface folder. The copy starts with a no-data Start and a Message step holding the sample lead, as in the skill's `process_testing_guide.md`. It uses copies of C7 and C8 that point at a topic name that does not exist. It is deployed to `1-DEV`, run with `boomi-test-execute.sh`, then undeployed and deleted. Limits:
  - It does not test the real C1 or the HTTP status codes, which are seen only in the process log.
  - A missing topic fails only if topic auto-creation is off on the cluster. The failure may come only after the producer's metadata timeout, which can be up to 60 s per attempt and so several minutes for 1 + 3 attempts.
  - It adds temporary components and a deployment. A process name and folder for the harness would be needed from the user, because CLAUDE.md naming applies to every process.
- **Option C: do not test these two paths in `1-DEV`.** They are verified only by review of the built process: the TC-T retry count is 3, the TC-T catch path goes to the C8 produce, and the TC-A catch path goes to BR-A. V1 for TC-T and V6 for BR-A stay unconfirmed. The risk is that a failed retry-topic send behaves differently from the design in production. V6 is still confirmed on the BR-F path by the functional-error test.

## Test notes

All tests run in `1-DEV` (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264) of account `shvenergynv-6R344K` only. Never change the `[Confluent_NL-HQ_Kafka]` component or its `1-DEV` extension values.

Exception (user: "C, review only for now"): the **Technical error** and **Retry-send failure / Kafka outage** rows are not forced in `1-DEV` in this build. They are verified by review only (R1 to R6 under "Failure-path test approach"). The tester records each as "not tested in dev, verified by review" with a pointer to the review evidence, and records V1 for TC-T and V6 for BR-A as unconfirmed (follow-ups F2, F3). The tester must not break a topic, the connection or its extension values to force these paths. Revision 7: if Kafka fails by itself during a `1-DEV` run, the tester records what happened (total time, HTTP status and body, shapes that ran) against the expected behaviour in those rows, as partial F2/F3 evidence. Every other row runs in `1-DEV`.

| Requirement | Observable behaviour to check |
|-------------|-------------------------------|
| Naming and folder | The process is named exactly `[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]` and is in `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead`. C2, C3 and C5 to C8 are in the same folder. Nothing new is in `.../Publisher/PUB-GB-CG-043-leads`. |
| Bridge mode | Process Mode = Bridge (`workload="bridge"`). Deployed to `1-DEV` only. |
| Endpoint | API Service C2 is deployed with base path `gb-cg-leads/v1`. A POST to `/ws/rest/gb-cg-leads/v1/leads` reaches C1. **`/ws/rest/gb-cg-leads/v1/leads/leads`: expected result depends on Q3** (row 24, D5). Until Q3 is answered this part is not tested. |
| Happy path | POST the valid sample lead JSON (see `mapping.md`). The response is 202 `{"status":"accepted"}` within 5 s. Exactly one message is on `gb-cg.q.leads.in.insert`. Its body is byte-for-byte the request, and it has **no custom headers and no key**. Nothing is on the retry topic. The facade is not called. |
| Tracking field | In Process Reporting for the happy-path execution, the tracked fields **`primarykey`** = `Email` and **`primaryvalue`** = the request's `email` value (for the sample, `testleadapitesting1@calor.co.uk`) are populated for the listen operation C3 and the produce operation C7. There is no tracked field named `email`; do not look for one (row 9). C8 is set the same way but runs only on the technical-error path (review only in this build). |
| Producer settings | C7 and C8 component XML: `acks` = `all`, `operation_timeout` = `5000`, `client_id` = `gb-cg.leads`, `compression_type` = `snappy` (row 18, D7). |
| Technical error (Q1 option a only) | **Review only in this build** (user: "C, review only for now"; R1 to R3). Not forced in `1-DEV`. Record "not tested in dev, verified by review" with the review evidence, and V1 for TC-T as unconfirmed (F2). Expected behaviour when it is later run (F2): 1 + N attempts on the main produce (row 22), then one message on `gb-cg.q.leads.in.retry` with the original body, no headers and no key. The response is 202 `{"status":"accepted"}` within the row 19 budget. The facade is not called. Topics and connection extension values are not changed in Boomi. |
| Functional error | POST an empty body, a malformed JSON body (for example the document's original sample with the missing comma) and a JSON array. For each case: no retry; BR-F branch 1 calls the facade exactly once with `DDP_MED_NS_Msg` = the functional error text; then BR-F branch 2 returns 400 `{"status":"rejected","message":"Functional error: ..."}` with the same text (V5, V6); **nothing on the main topic and nothing on the retry topic**; no Kafka produce appears in the process log. The facade run completes without error, including the route target's Document Cache Load (D4). |
| Facade inputs | C1 XML: both "Set facade inputs" steps set exactly the "Facade inputs" rows that have a value, FI-1 first, with Execution property sources for FI-2 to FI-8; rows answered "leave unset" are absent. In the functional-error run log, the route target 47e2da88 no longer fails with "Could not determine value for Index key: DDP_MED_ProcessId". |
| Retry-send failure / Kafka outage | **Review only in this build** (user: "C, review only for now"; R3 to R6). Not forced in `1-DEV`. Record "not tested in dev, verified by review" with the review evidence, and V1 for TC-T and V6 for BR-A as unconfirmed (F2, F3). Expected behaviour (user: "kafka outage should give an error back"): after 1 + N failed main attempts and a failed retry-topic send (Q1 option a) or no retry-topic send (Q1 option b), BR-A branch 1 calls the facade once with the Kafka error. Then BR-A branch 2 returns 500 `{"status":"error","message":"Technical error. The lead was not accepted."}`, **within the row 19 budget and never with no response**. That run confirms V1 for TC-T and V6 for BR-A. If Kafka fails by itself in a `1-DEV` run, record the observed outcome against this row. |
| Extensions | C1's `processOverrides` holds the `ConnectionOverride` for c85b494e copied from process 1b208fa6 (D6): the same field set, every field has an `xpath` of the form `GenericConnectionConfig/field[@id='<id>']/@value`, and every field id exists in the C4 component. There are no fields without an xpath. The only C4 field not declared is `consumer_group`, which is an accepted exception (row 20; user: "2. a"); any other undeclared C4 field is a defect. Under Environment Extensions in `1-DEV`, the `[Confluent_NL-HQ_Kafka]` connection fields appear. C7 and C8 have no operation overrides, and their topics are fixed in the component XML, as the CLAUDE.md "Connector extensions" exception allows. No environment-specific connection value is in any component XML. The shared `[Confluent_NL-HQ_Kafka]` component version is unchanged, and its `1-DEV` extension values are the same after testing as before. |
| No banned shapes | No Notify shapes. Exactly three Try/Catch shapes (TC-A retry 0, TC-T retry N from row 22, TC-F retry 0). Two Branch shapes (BR-F, BR-A), each with `numBranches="2"` and both dragpoints wired. Four Return Documents shapes (three with Q1 option b). No Set Properties step for a Kafka header. |
| Kafka topics confirmed | `pipeline-state.md` records the user's confirmation of both topic names (row 25). The tester does not check topic existence on the platform. |
| Volume | About 10 sequential calls all return 202 and produce 10 messages on the main topic. |

## Open questions

Revision 7. Questions 4 to 10 all offer "a. leave unset" as the first option. You can answer them together, for example "4-10: a". Evidence for "leave unset": the framework map `[MED] CREATE Notification` ran without error with these values empty. The rest of the facade path has not yet run past the cache load, so if a later facade step needs one of them, the developer stops at D4 and the question comes back.

1. **Kafka outage: should the lead still be offered to the retry topic before the error is returned?** You said "kafka outage should give an error back". Earlier you asked for failed leads to be parked on `gb-cg.q.leads.in.retry` with a 202 response (Q8 and follow-up C).
   - a. Keep parking (designer's recommendation). After the main-topic retries fail, send the lead to the retry topic. If that works, for example when only the main topic has a problem, answer 202 because the lead is safe. If it also fails, which is what normally happens when the whole Kafka cluster is down, call the facade and answer 500. Costs about 5 s more on an outage.
   - b. Stop parking. After the main-topic retries fail, call the facade and answer 500 straight away. The retry topic is no longer written by this process.
   - c. Something else (please describe, for example park and still answer with an error code).
2. **TC-T retry count: how many retries of the main-topic send?** You asked for 3 (Q8). With 3, the `1-DEV` runtime stopped the execution at about 30 s and the caller got no response (execution 93e06b38). Each failed attempt takes about 5 s, and the runtime added gaps of up to 13 s between later retries. See the table in "Kafka producer settings".
   - a. 1 retry (designer's recommendation). With 1a, about 15 s plus the facade on the observed timing. Up to about 28 s if a long gap occurs before the retry, which has not been seen so far.
   - b. 0 retries. About 10 s (with 1a) or 5 s (with 1b) plus the facade. Safest against the 30 s limit. One failed send is enough to give up.
   - c. 2 retries. Not recommended: on the observed timing it reaches about 31-33 s with 1a, which is past the runtime limit.
3. **API route: what should happen to `/ws/rest/gb-cg-leads/v1/leads/leads`?** You said it is a defect ("b"). The designer cannot give a C2 route setting that is proven to reject the extra segment: the current route (object `leads`, empty URL path) passes it, and the local Boomi references do not describe extra-segment matching. The obvious alternative (empty object, URL path `leads`) would inherit the object `leads` from the WSS operation and make the route `/leads/leads` itself.
   - a. Investigate first. The developer looks for Boomi documentation (help.boomi.com was not reachable from the build machine before) or an account API Service that rejects extra segments, and reports the setting. The designer then adds it in revision 8. Nothing changes in C2 until then.
   - b. Accept it as a known platform behaviour for now. APIM only forwards `/leads`, so Sitecore cannot reach `/leads/leads`. Only a caller with the Boomi runtime credentials can. D5 then checks only that `/leads` reaches C1 and records what `/leads/leads` does.
   - c. You give the setting or approach to use (for example from your Boomi or APIM team).
4. **`DDP_MED_NS_Level`: what notification level should the facade receive?** Needed for the functional error (400 path) and for the technical error / Kafka outage (500 path).
   - a. Leave unset.
   - b. Give the two values, as used by your other SHV framework callers of the facade (one for the functional error, one for the technical error).
5. **`DDP_MED_NS_Code`: what notification code should the facade receive?** Same two paths as question 4.
   - a. Leave unset.
   - b. Give the two codes, as your other SHV framework callers use them.
6. **`DPP_MED_Environment`: what environment name should the facade receive?** It differs per environment, so it cannot be fixed in the process.
   - a. Leave unset.
   - b. Set it from an extensible process property, with the value set per environment in Environment Extensions. Please give the `1-DEV` value (for example `1-DEV`, the Boomi environment name) and confirm the developer may set that one extension value for C1 in `1-DEV`.
7. **`DPP_MED_Environment_Class`: what environment class should the facade receive?**
   - a. Leave unset.
   - b. Give the value for `1-DEV` and say how it should differ in other environments. For example, Boomi itself classifies environments as Test or Production, and your framework may use its own codes.
8. **`DPP_MED_APIURL`: what API URL should the facade receive?**
   - a. Leave unset.
   - b. The fixed path `/ws/rest/gb-cg-leads/v1/leads` (the same in every environment).
   - c. The full URL per environment, set from an extensible process property (for `1-DEV`: `https://shv-energy-test.boomi.cloud/ws/rest/gb-cg-leads/v1/leads`).
9. **`DPP_MED_TrackingId`: what tracking ID should the facade receive?**
   - a. Leave unset.
   - b. The request's `email` value (your tracking field, Q7). Note: this puts customer data into the notification.
   - c. The execution ID (the same value as `DPP_MED_ExecutionId`).
   - d. Something else (please name it).
10. **`DPP_MED_TrackedFields`: what tracked-fields value should the facade receive?**
    - a. Leave unset.
    - b. Give the value and its format (for example a field name and value pair such as `Email=<request email>`, if that is what your framework expects). Note: putting the email here puts customer data into the notification.

Earlier questions, all answered: revision 5 question 1 (failure-path test approach): "C, review only for now" (row 16). Round 1 review decisions: "1. copy from CreateLead 2. acks=all, 5s timeout" (rows 17, 18). Revision 6 questions: response time on Kafka failure paths and `consumer_group` coverage: "1. a 2. a" (rows 19, 20; row 19 superseded in revision 7). Developer BLOCKED in round 1 fix (2026-10-09): topics created (row 25), "set whatever needs to be set and available to you" (row 21), "kafka outage should give an error back" (rows 19, 23), "b" for `/leads/leads` (row 24).
