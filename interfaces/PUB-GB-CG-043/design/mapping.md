# Field mapping: PUB-GB-CG-043

Revision 2. All earlier open items are resolved by the user's answers (Q10, Q11, Q12, Q13, Q9).

## Request: Sitecore lead JSON -> Kafka message body

Source profile: `PUB-GB-CG-043 Lead Request JSON` (C5), received by the WSS listen operation C3.
It is built from the sample in the design document section 1.2.4, corrected to valid JSON. The missing comma after
`"form-source":"HE Fuel Switch Enquiry"` is a document typo only (user Q10: "yes"). The comments field is named
`additional-comments` (user Q11: "type", meaning the document's "addional-comments" is a typo).

Target: the Kafka message body on `gb-cg.q.leads.in.insert` (and, on error, on `gb-cg.q.leads.in.retry`).
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

## Kafka message header

| # | Source | Target | Transformation / rule | Required | Example |
|---|--------|--------|-----------------------|----------|---------|
| H1 | Static value | Kafka message header `Retry-Count` | Always `0` on every message, on both the main and the retry topic (user Q13). It is not used by this interface yet | Y | `0` |
| H2 | n/a | Kafka message key | None. No key is set (user Q13 asked only for the header) | N | (none) |

## Response: WSS output -> APIM / Sitecore

Response profile: `PUB-GB-CG-043 Lead Response JSON` (C6). Built by Message steps; the HTTP status is set per outcome (spec, "HTTP response per outcome").

| # | Source | Target field / path | Transformation / rule | Required | Example |
|---|--------|---------------------|-----------------------|----------|---------|
| R1 | Static per outcome | `status` (root/status) | `accepted` (202), `rejected` (400) or `error` (500) | Y | `accepted` |
| R2 | 202: omitted. 400: `DDP_MED_NS_Msg` (functional error text from script S1 via the Exception step). 500: fixed text | `message` (root/message) | Omitted on 202 (body is exactly `{"status":"accepted"}`, user Q9). 500 text is fixed so no sensitive data or connection detail is returned | N | `Functional error: request body is not valid JSON` |
