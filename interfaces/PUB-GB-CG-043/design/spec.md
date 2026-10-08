# Design spec: PUB-GB-CG-043

Status: DRAFT - OPEN QUESTIONS

## Requirements

Source: the user-supplied interface design document "PUB-GB-CG-043-Web_To_Lead_Publisher_V0.1.docx"
(author A. Koyyada, version 1, 21/09/2026), converted text at
`interfaces/PUB-GB-CG-043/design/source/requirements.md`. The user has given no other answers yet.

Scope of this spec: **the Publisher only (PUB-GB-CG-043).**

- Sitecore submits selected web forms (web-to-lead) as a JSON request via Azure APIM, in real time
  and event driven. APIM gets an OAuth 2.0 token and then calls the Boomi REST endpoint.
- The Boomi listener receives the JSON request body and publishes it to the Kafka topic
  `gb-cg.q.leads.in.insert` (document section 1.3.2).
- Downstream consumer (out of scope, separate interface): the Subscriber SUB-GB-CG-043 listens to
  that topic and creates the Lead in Salesforce. The Salesforce connector `[SF_Connector]` and
  the Sitecore-to-Salesforce field mapping workbook belong to that interface, not this one.
- Business criticality: Medium. Data contains customer fields and is sensitive.
- NFRs: API response time 5 s (max 5 s); about 60 calls per day, peak 75 per day, average 525 per week.
- Data validation is out of integration scope (document section 1.2.1, "Data Format Validation").
- On a connectivity error, Boomi retries 3 times and then invokes error handling to notify support
  (document section 1.2.1, "Notes").
- Technical and process failures are captured with the common framework notification and logging facade
  (document section 1.3.2).
- Existing connector to reuse: Kafka `[Confluent_Kafka]` (Is New = No), in
  `Calor Group Limited/00-ConnectionResources/00-Connections`. SASL_SSL, SASL mechanism PLAIN.
  Credentials and client principals are deliberately not repeated here.
- The document names the account `Calorgrouplimited-3SH5SL` and the deployment location
  "Boomi MCS - API / Real-Time Cluster" (see open question 6).

## Required values

| # | Value | Answer | Source |
|---|-------|--------|--------|
| 1 | Interface type | Publisher (Web Services Server start, publishes to a Kafka topic) | user: design document title "Interface Design and Specification (Publisher)" and process name "[Publisher]-[PUB-GB-CG-043]-..." in section 1.3.2; matches CLAUDE.md: Interface type (Publisher) |
| 2 | Integration ID sequence number (YYY) | 043 | user: design document interface ID "PUB-GB-CG-043" (sections 1.1 and 1.3.2) |
| 3 | Integration ID | PUB-GB-CG-043 (`PUB` = Publisher, `GB-CG` = Calor Group Limited, `043`). Equals the orchestrator folder ID. | CLAUDE.md: Integration ID, BU-SHORT codes; user: design document |
| 4 | Main atomic object | Document gives two forms: "CreateLead" and "leads". Not resolved. | OPEN (question 1) |
| 5a | Source application | Document gives two forms: "Customer Portal" and "Sitecore". Not resolved. | OPEN (question 2) |
| 5b | Source BU | GB-CG | user: design document "Business Units and Applications" table (Calor GB, GB-CG, Sitecore) and process names in section 1.3.2 |
| 6a | Target application | Not required for this interface type (Publisher). | CLAUDE.md: Interface type (Publisher: Source application and Source BU mandatory) |
| 6b | Target BU | Not required for this interface type (Publisher). | CLAUDE.md: Interface type (Publisher) |
| 7 | Project type | Document says "Enterprise Projects"; this conflicts with the application-name rule for Enterprise Projects. Not resolved. | OPEN (question 3) |
| 8 | Application name | Document says "Customer Portal"; valid value depends on question 3. Not resolved. | OPEN (question 4) |
| 9 | Tracking field(s) | Document proposes `email` (profile element `email`, "Customer email will be passed"). Proposed on the WSS listen operation and the Kafka produce operation. Needs confirmation. | OPEN (question 7) |
| 10 | Full process name | `[Publisher]-[PUB-GB-CG-043]-[<Main atomic object>]-[<Source application>]-[GB-CG]` | OPEN (depends on questions 1 and 2) |
| 11 | Full folder path | `GB-CG / <Project type> / <Application name> / Publisher / PUB-GB-CG-043-<Interface name>` | OPEN (depends on questions 1, 3, 4 and 5) |

Source is one of: `user: "<answer>"`, `CLAUDE.md: <section>`, or `OPEN`.

Notes on rows 10 and 11:

- The Publisher pattern has exactly five segments: interface type, integration ID, main atomic object,
  source application, source BU. No target segments are added.
- The document shows the name in two forms, neither final:
  `[Publisher]-[PUB-GB-CG-043]-[CreateLead-[Customer Portal]-[GB-CG]` (section 1.3.2 text, also missing a closing bracket) and
  `[Publisher]-[PUB-GB-CG-043]-[leads]-[Customer Portal]-[GB-CG]` (section 1.3.2 table).
- The document folder is `Calor Group Limited/02-Deployable/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-leads`.
  The CLAUDE.md convention starts at the BU-SHORT level. See questions 3, 4 and 5.

## Process design

- Start shape: Web Services Server (`wss`) listen operation, Action = Listen, input type single JSON document
  with the request JSON profile (see `mapping.md`), output type single JSON document (response).
  Endpoint object name per question 18; authentication from APIM to Boomi per question 19.
  The developer must run `boomi-shared-server-info.sh` first and pick a bare WSS listener or an API Service Component based on the atom `apiType` (skill rule).
- Main steps (Try path):
  1. Start (WSS listen) -> Try/Catch TC1.
  2. Kafka connector, Produce action with `[Confluent_Kafka]` and the produce operation (question 15).
     The message body is the request body, unchanged, subject to question 12. The message key is set per question 13;
     if a key is required, one Set Properties step before the Kafka step sets it.
  3. Message step: builds the success response body (question 9).
  4. Return Documents (success).
- Catch path (TC1): Set Properties `DDP_MED_NS_Msg` -> Process Call `[MED] (sub) CACHE Notification Facade`
  -> Message step that builds the error response body (question 9) -> its own Return Documents (error).
  Success and error each end in their own Return Documents. There are no converging outcomes and no Notify shapes.
- Target: Kafka topic `gb-cg.q.leads.in.insert` (user: design document section 1.3.2 "Kafka Topic Name").
  It is consumed downstream by SUB-GB-CG-043 (out of scope).
- Deployment mode (workload): `bridge`. Source: CLAUDE.md: SHV Energy build rules, Deployment mode (Web Services Server start).
  This does not conflict with the document's "Boomi MCS - API / Real-Time Cluster" location. In bridge mode execution history and logs are kept, but document payloads are not.
  Other process options are per the skill defaults for listeners (`allowSimultaneous="true"`).
- Environment: build, deploy and test in development or test only, never production (CLAUDE.md). The target account and environment depend on question 6.

## Error handling

One Try/Catch, which is within the CLAUDE.md limit of three.

| Try/Catch | Wraps | Catch path |
|-----------|-------|------------|
| TC1 (catch "All errors"; retry count per question 8, proposed 3 if confirmed) | Everything after the Start shape: the optional key Set Properties, the Kafka produce, the success response Message and Return Documents | Set Properties `DDP_MED_NS_Msg` = Try/Catch message (Meta information, Base > Try/Catch Message) -> Process Call `[MED] (sub) CACHE Notification Facade` -> Message (error response, question 9) -> Return Documents (error) |

The document's exception table (400 Bad request, 401 Unauthorized, 500 technical) is not yet tied to process behaviour:

- 401 is enforced by APIM or the Boomi listener authentication before the process runs. No process step handles it.
- 400 has no trigger because validation is out of scope. See question 9.
- 500 is the catch path. The status and body are set per question 9.

## Cache Notification Facade

- Where `DDP_MED_NS_Msg` is set to the Try/Catch message: the first step on the TC1 Catch path is a Set Properties step.
  It sets dynamic document property `DDP_MED_NS_Msg` from Meta information "Try/Catch Message".
- Where `[MED] (sub) CACHE Notification Facade` is called: a Process Call step right after that Set Properties step on the Catch path,
  with Wait for process to complete = true. Facade location per CLAUDE.md:
  `SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/00-SharedLibrary_v4/00-Version_4.0 (2019-12-28-baseline)/01-Facade/02-Process`.
  Whether this exists in the build account is question 16. Whether the facade is also called on the success path before the Kafka send is question 17.

## Connectors

| Connection / operation | Purpose | Extensible settings | Tracking field |
|------------------------|---------|---------------------|----------------|
| WSS listen operation (new; name per question 18) | Receive the Sitecore lead JSON from APIM | No connection component. The object name and profiles are part of the API contract, not environment-specific. Any operation setting that can be extended is extended (CLAUDE.md: Connector extensions). | `email` from the request profile (pending question 7) |
| `[Confluent_Kafka]` connection (existing, `Calor Group Limited/00-ConnectionResources/00-Connections`) | Kafka (Confluent Cloud) broker connection | All of them: bootstrap servers/broker list, security protocol, SASL mechanism, username/client principal, password, plus any other connection field. Values are supplied per environment through extensions, never written into XML or this spec. Status per question 14. | n/a |
| Kafka Produce operation (existing or new per question 15) | Publish to topic `gb-cg.q.leads.in.insert` | Topic name and every other operation property that can be extended (CLAUDE.md: Connector extensions) | `email` (pending question 7) |
| `[SF_Connector]` | Not used by this interface. Belongs to SUB-GB-CG-043. | n/a | n/a |

## Scripts

| Script | Single purpose |
|--------|----------------|
| None | No scripting is needed. Property setting and the response bodies use standard Set Properties and Message steps. |

## Test notes

All tests run in development or test only.

| Requirement | Observable behaviour to check |
|-------------|-------------------------------|
| Naming and folder | The process name and folder path exactly match rows 10 and 11 once approved. The process is in the approved folder. |
| Bridge mode | The process option Process Mode = Bridge (`workload="bridge"`), and the deployment is in the dev/test environment. |
| Receive and publish | POST a valid sample lead JSON (corrected per question 10) to the listener. The execution succeeds and exactly one message appears on `gb-cg.q.leads.in.insert`. Its body matches the request (per question 12) and its key is per question 13. |
| Response contract | The success response status and body match question 9. The response returns within 5 s. |
| Tracking field | Process Reporting shows the tracked field `email` populated on the listen and produce operations (per question 7). |
| Error path | Force a Kafka failure, for example an invalid topic extension value in a test environment. TC1 catches it, and retries happen per question 8 (visible in the process log). `DDP_MED_NS_Msg` holds the Try/Catch message. The facade subprocess runs. The error response status and body match question 9. |
| Extensions | The Kafka connection and operation settings appear under Environment Extensions. No environment-specific value is hard-coded in the component XML. |
| No banned shapes | The process contains no Notify shapes and at most three Try/Catch shapes (expected: one). |
| Volume | A small burst of calls (about 10 in sequence, well within the 75 per day peak) all succeed without errors. |

## Open questions

1. Main atomic object: which value goes in the third segment of the process name? The document uses "CreateLead" (section 1.3.2 text) and "leads" (section 1.3.2 table and the folder leaf "PUB-GB-CG-043-leads"). CLAUDE.md examples use a business object or action, such as "Customer", "Route Delivery" or "Send Cylinder Shipment". Options: "CreateLead", "leads", or another value such as "Lead".
2. Source application: which application goes in the fourth segment of the process name, "Sitecore" or "Customer Portal"? The document's process names use "Customer Portal". Its "Business Units and Applications" table and "Source - Data Provider" section name Sitecore as the sending system. CLAUDE.md examples use the originating system name, such as "SAP-S4", "OBTC" or "Microsoft Dynamics 365".
3. Project type: is this "Enterprise Projects" (local-to-local, as the document's folder path says) or "Digital Projects" (global programme)? CLAUDE.md: "Digital Projects for global programmes, Enterprise Projects for local-to-local projects". The document's application folder "Customer Portal" matches the Digital Projects list value "CustomerPortal".
4. Application name: which exact value goes in the APPLICATION-NAME folder level? CLAUDE.md: for Digital Projects it must be one of Procurement, CRM, CustomerPortal, Telemetry, WebSites or Workday. For Enterprise Projects it is the target application (for example PDI, RNA, Paragon or OBTC). "Customer Portal" (the document's value) is not the target application of this flow. The target is Kafka, and ultimately Salesforce.
5. Folder root and leaf: should the CLAUDE.md tree `GB-CG / <Project type> / <Application name> / Publisher / ...` be created under "Calor Group Limited/02-Deployable/" (as the document shows) or somewhere else, such as the workspace's configured target folder? Should the leaf be "PUB-GB-CG-043-" followed by the main atomic object from question 1 (the document shows "PUB-GB-CG-043-leads")?
6. Build account and environment: the document names the account "Calorgrouplimited-3SH5SL" and the deployment location "Boomi MCS - API / Real-Time Cluster". Is that the account this workspace builds in? Which development or test environment and runtime should the developer deploy to? CLAUDE.md allows development or test only, never production.
7. Tracking field: do you confirm `email` (document section 1.3.3) as the tracking field, used on both the WSS listen operation and the Kafka produce operation? The document marks this data as sensitive customer data, and a tracked email will be visible in Process Reporting. If not, which field should be used instead, for example "form-source" or a generated request ID?
8. Retry behaviour: the document says "For any connectivity error, Boomi will retry 3 times before invoking the error handling process". Should this be the Try/Catch retry count = 3 on TC1, with the facade as the "error handling process"? Note that this retries all errors, not only connectivity errors, and retries add time against the 5 s maximum response time. Or should it be retry settings on the Kafka connector/operation only?
9. API response contract: what HTTP status and response body should Boomi return to Sitecore/APIM on success (for example 200 or 202 with `{"status":"accepted"}`) and on failure (for example 500 with an error message)? When, if ever, should the process return 400, given that the document says data validation is out of scope?
10. Sample JSON: the document's sample is invalid JSON because a comma is missing after `"form-source":"HE Fuel Switch Enquiry"`. Is this only a document error, with the real Sitecore payload being valid JSON with the same fields? Can you provide or confirm a valid sample for the request profile?
11. Field name "addional-comments": is "addional-comments" the exact field name Sitecore sends (typo included), or is the real field "additional-comments"?
12. Kafka message body: should the Publisher publish the Sitecore request body unchanged (pass-through, no map), or wrap or transform it, for example by adding metadata for SUB-GB-CG-043?
13. Kafka message key and headers: should the Kafka message have a key, for example `email`, or no key? Are any message headers required by SUB-GB-CG-043?
14. Kafka connection reuse: should the developer reuse the existing `[Confluent_Kafka]` connection in "Calor Group Limited/00-ConnectionResources/00-Connections" as is? CLAUDE.md requires all connection settings to be extensible. If its settings are not already extensions, may the developer change this shared connection, or must a new connection be created, and in which folder?
15. Kafka produce operation: is there an existing Kafka produce operation for topic `gb-cg.q.leads.in.insert` to reuse (name and folder), or must the developer create one? If new, which folder: the process folder from question 11 of the required values, or the shared connections folder? Does the topic already exist in the development/test Confluent cluster?
16. Facade location: CLAUDE.md places `[MED] (sub) CACHE Notification Facade` under "SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/...". Does that component exist in the build account from question 6, or is there a Calor copy the process should call instead (name and folder)?
17. Facade on success path: CLAUDE.md says "Before sending, call the process [MED] (sub) CACHE Notification Facade" and set `DDP_MED_NS_Msg` to the Try/Catch message, and that message exists only on the Catch path. This design calls the facade only on the Catch path. Should it also be called on the success path just before the Kafka send? If so, what value should `DDP_MED_NS_Msg` carry there?
18. Listener endpoint name: what object name or path should the Boomi WSS operation expose (for example "leads", giving `/ws/rest/leads` or similar)? The document gives only the APIM URL `.../gb-cg/sales-and-service-management-api/v1/leads`.
19. APIM-to-Boomi authentication: how does APIM authenticate to the Boomi listener (for example Basic auth with a shared web server user)? The document only describes Sitecore-to-APIM OAuth 2.0.
