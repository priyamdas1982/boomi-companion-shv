# Field mapping: PUB-GB-CG-043

Revision 7 (2026-10-09). Changes from revision 6: a new section "Facade inputs" lists the properties C1 sets before each call to `[MED] (sub) CACHE Notification Facade` (user: "set whatever needs to be set and available to you"; evidence: build log "Attempt 4 / Round 1 fix", "Log analysis", execution 22c61363). Rows FI-9 to FI-15 are `OPEN` (spec open questions 4 to 10). Response row R1 now notes that a Kafka outage returns 500 (user: "kafka outage should give an error back"). The request pass-through rows, the header/key rows and the response bodies are unchanged.

Revision 6. Change from revision 5 (review finding F-1-02, wording only): row 4 now names the tracked-field slots that carry the user's tracking field `email` on C3, C7 and C8: `primarykey` = static `Email` and `primaryvalue` = request element `email`. No field rule changes. The C7/C8 producer settings changed in revision 6 (`acks` = `all`, `operation_timeout` = `5000`) do not affect any field.

Revision 5 change from revision 4: the Kafka message header `Retry-Count` is removed from this build (user: "1. b"). Messages carry no custom headers and no key. The header is follow-up F1 in the spec, for the future retry mechanism. Topics are fixed in operations C7 and C8 (user: "2. a"; CLAUDE.md: Connector extensions, Exception). This does not affect any field. All other field rules are unchanged from revision 4.

Earlier history: all open items were resolved by the user's answers (Q10, Q11, Q12, Q13, Q9). Revision 3: a functional error is not sent to any Kafka topic (user correction: "This message do not go to retry topic."). Revision 4: because of the user's "branch fix", the 400 response is built on branch 2 of a Branch shape, so the 400 `message` value (R2) comes from Meta information "Base - Try/Catch Message" (`meta.base.catcherrorsmessage`), not from `DDP_MED_NS_Msg`.

## Request: Sitecore lead JSON -> Kafka message body

Source profile: `PUB-GB-CG-043 Lead Request JSON` (C5), received by the WSS listen operation C3.
It is built from the sample in the design document section 1.2.4, corrected to valid JSON. The missing comma after
`"form-source":"HE Fuel Switch Enquiry"` is a document typo only (user Q10: "yes"). The comments field is named
`additional-comments` (user Q11: "type", meaning the document's "addional-comments" is a typo).

Target: the Kafka message body on `gb-cg.q.leads.in.insert` (and, for a technical error after 3 retries only, on `gb-cg.q.leads.in.retry`). A body that fails the functional check (empty, not valid JSON, not a JSON object) is not published anywhere. It gets a 400 response.
It is pass-through: the request body is published unchanged, with no Map step (user Q12: "unchanged").
The rows below describe the contract. The developer must not add a map.

Required column: the Publisher validates no individual field. Data validation is out of integration scope per the document.
The only check is that the body is present and is a JSON object (script S1 in the spec). The Salesforce-side requirements belong to SUB-GB-CG-043.

| # | Source field / path | Target field / path | Transformation / rule | Required | Example |
|---|---------------------|---------------------|-----------------------|----------|---------|
| 1 | `first-name` (root/first-name) | `first-name` (root/first-name) | Pass-through, unchanged | N | `Test` |
| 2 | `last-name` (root/last-name) | `last-name` (root/last-name) | Pass-through, unchanged | N | `LeadAPITesting1` |
| 3 | `phone` (root/phone) | `phone` (root/phone) | Pass-through, unchanged (string, leading zero kept) | N | `07989480687` |
| 4 | `email` (root/email) | `email` (root/email) | Pass-through, unchanged. Tracking field (user Q7) on C3, C7 and C8, through tracked-field slots `primarykey` = static `Email` and `primaryvalue` = this element (spec row 9). Not used as a Kafka key (no key) | N | `testleadapitesting1@calor.co.uk` |
| 5 | `postcode` (root/postcode) | `postcode` (root/postcode) | Pass-through, unchanged | N | `GL3 1DL` |
| 6 | `address-line-one` (root/address-line-one) | `address-line-one` (root/address-line-one) | Pass-through, unchanged | N | `Ref County Durham Dowco Hous` |
| 7 | `additional-comments` (root/additional-comments) | `additional-comments` (root/additional-comments) | Pass-through, unchanged | N | `Testing Lead, please ignore` |
| 8 | `form-source` (root/form-source) | `form-source` (root/form-source) | Pass-through, unchanged | N | `HE Fuel Switch Enquiry` |
| 9 | `lead-channel` (root/lead-channel, array of string) | `lead-channel` (root/lead-channel, array of string) | Pass-through, unchanged; array kept as an array | N | `["Webform"]` |
| 10 | `lead-source` (root/lead-source, array of string) | `lead-source` (root/lead-source, array of string) | Pass-through, unchanged; array kept as an array | N | `["Digital"]` |

Corrected sample (test payload and profile source):

```json
{
  "first-name": "Test",
  "last-name": "LeadAPITesting1",
  "phone": "07989480687",
  "email": "testleadapitesting1@calor.co.uk",
  "postcode": "GL3 1DL",
  "address-line-one": "Ref County Durham Dowco Hous",
  "additional-comments": "Testing Lead, please ignore",
  "form-source": "HE Fuel Switch Enquiry",
  "lead-channel": ["Webform"],
  "lead-source": ["Digital"]
}
```

## Kafka message header and key

| # | Source | Target | Transformation / rule | Required | Example |
|---|--------|--------|-----------------------|----------|---------|
| H1 | n/a | Kafka message header `Retry-Count` | **Not set in this build** (user, revision 5: "1. b"). Deferred to follow-up F1, the future retry mechanism. The original request was `Retry-Count` = `0` on every message (user Q13) | N | (none) |
| H2 | n/a | Kafka message key | None. No key is set (user Q13 asked only for the header) | N | (none) |

## Response: WSS output -> APIM / Sitecore

Response profile: `PUB-GB-CG-043 Lead Response JSON` (C6). Built by Message steps; the HTTP status is set per outcome (spec, "HTTP response per outcome").

| # | Source | Target field / path | Transformation / rule | Required | Example |
|---|--------|---------------------|-----------------------|----------|---------|
| R1 | Static per outcome | `status` (root/status) | `accepted` (202), `rejected` (400) or `error` (500). Revision 7: a Kafka outage returns `error` (500) within the spec row 19 budget; whether a lead parked on the retry topic still gets `accepted` (202) depends on spec open question 1 | Y | `accepted` |
| R2 | 202: omitted. 400: Meta information "Base - Try/Catch Message" (`meta.base.catcherrorsmessage`), read on BR-F branch 2. It holds the functional error text from script S1 via the Exception step, the same text that BR-F branch 1 puts in `DDP_MED_NS_Msg`. 500: fixed text | `message` (root/message) | Omitted on 202 (body is exactly `{"status":"accepted"}`, user Q9). 400 must not read `DDP_MED_NS_Msg`, because that DDP is set on branch 1 and does not reach branch 2 (revision 4). 500 text is fixed so no sensitive data or connection detail is returned | N | `Functional error: request body is not valid JSON` |

## Facade inputs: C1 -> `[MED] (sub) CACHE Notification Facade` (revision 7)

Set in the Set Properties step "Set facade inputs" on BR-F branch 1 (functional error) and on BR-A branch 1 (technical error / Kafka outage), before the Process Call (spec "Facade inputs"). Order: FI-1 first, then table order. A row answered "leave unset" is not set at all. "Execution property" = Set Properties source of type Execution Property (`valueType="execution"`), read when the step runs, so it describes C1 and its execution.

| # | Source | Target property | Transformation / rule | Required | Example |
|---|--------|-----------------|-----------------------|----------|---------|
| FI-1 | Meta information "Base - Try/Catch Message" (`meta.base.catcherrorsmessage`) | DDP `DDP_MED_NS_Msg` | Copied as is | Y (CLAUDE.md) | `Functional error: request body is not valid JSON` |
| FI-2 | Execution property `Process Id` | DPP `DPP_MED_ProcessId` | Copied as is. Fatal if empty: the route target's Document Cache index key | Y (proven) | `135044a4-ad21-4ba0-b4d7-5e5c21fac446` |
| FI-3 | Execution property `Process Name` | DPP `DPP_MED_ProcessName` | Copied as is | N | `[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]` |
| FI-4 | Execution property `Execution Id` | DPP `DPP_MED_ExecutionId` | Copied as is | N | `execution-22c61363-80dd-4f5e-aaa5-5fb369afbd7d-2026.10.09` |
| FI-5 | Execution property `Account Id` | DPP `DPP_MED_AccountId` | Copied as is | N | `shvenergynv-6R344K` |
| FI-6 | Execution property `Atom Id` | DPP `DPP_MED_AtomId` | Copied as is | N | the `1-DEV` runtime ID (9beaf0cb-...) |
| FI-7 | Execution property `Atom Name` | DPP `DPP_MED_AtomName` | Copied as is | N | `MCS_NL-HM_DEV_1` |
| FI-8 | Execution property `Atom Id` | DPP `DPP_MED_ContainerId` | Copied as is ("container" = Boomi runtime; spec FI-8) | N | same as FI-6 |
| FI-9 | OPEN (spec Q4) | DDP `DDP_MED_NS_Level` | OPEN; may differ between BR-F and BR-A | OPEN | OPEN |
| FI-10 | OPEN (spec Q5) | DDP `DDP_MED_NS_Code` | OPEN; may differ between BR-F and BR-A | OPEN | OPEN |
| FI-11 | OPEN (spec Q6) | DPP `DPP_MED_Environment` | OPEN | OPEN | OPEN |
| FI-12 | OPEN (spec Q7) | DPP `DPP_MED_Environment_Class` | OPEN | OPEN | OPEN |
| FI-13 | OPEN (spec Q8) | DPP `DPP_MED_APIURL` | OPEN | OPEN | OPEN |
| FI-14 | OPEN (spec Q9) | DPP `DPP_MED_TrackingId` | OPEN | OPEN | OPEN |
| FI-15 | OPEN (spec Q10) | DPP `DPP_MED_TrackedFields` | OPEN | OPEN | OPEN |
