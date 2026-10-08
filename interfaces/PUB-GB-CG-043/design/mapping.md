# Field mapping: PUB-GB-CG-043

Revision 5. Change from revision 4: the Kafka message header `Retry-Count` is removed from this build (user: "1. b"). Messages carry no custom headers and no key. The header is follow-up F1 in the spec, for the future retry mechanism. Topics are fixed in operations C7 and C8 (user: "2. a"; CLAUDE.md: Connector extensions, Exception). This does not affect any field. All other field rules are unchanged from revision 4.

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
| 4 | `email` (root/email) | `email` (root/email) | Pass-through, unchanged. Tracking field on C3, C7 and C8 (user Q7). Not used as a Kafka key (no key) | N | `testleadapitesting1@calor.co.uk` |
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
| R1 | Static per outcome | `status` (root/status) | `accepted` (202), `rejected` (400) or `error` (500) | Y | `accepted` |
| R2 | 202: omitted. 400: Meta information "Base - Try/Catch Message" (`meta.base.catcherrorsmessage`), read on BR-F branch 2. It holds the functional error text from script S1 via the Exception step, the same text that BR-F branch 1 puts in `DDP_MED_NS_Msg`. 500: fixed text | `message` (root/message) | Omitted on 202 (body is exactly `{"status":"accepted"}`, user Q9). 400 must not read `DDP_MED_NS_Msg`, because that DDP is set on branch 1 and does not reach branch 2 (revision 4). 500 text is fixed so no sensitive data or connection detail is returned | N | `Functional error: request body is not valid JSON` |
