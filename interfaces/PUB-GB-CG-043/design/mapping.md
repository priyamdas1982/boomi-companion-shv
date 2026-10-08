# Field mapping: PUB-GB-CG-043

Source profile: new JSON profile for the Sitecore web-to-lead request, received by the WSS listen operation.
It is built from the sample in the design document section 1.2.4, after that sample is corrected to valid JSON (spec open question 10).
Target profile: the Kafka message body published to `gb-cg.q.leads.in.insert`. The proposed design is pass-through:
the same JSON document with no Map step (spec open question 12). If question 12 asks for a wrapper or transformation,
a target JSON profile and a Map are added and this table is revised.

Required column: the Publisher does not validate fields. The document says "Data validation is not part of Integration scope",
so no field is enforced as required by this interface. The Salesforce-side requirements belong to SUB-GB-CG-043.

| # | Source field / path | Target field / path | Transformation / rule | Required | Example |
|---|---------------------|---------------------|-----------------------|----------|---------|
| 1 | `first-name` (root/first-name) | `first-name` (root/first-name) | Pass-through, unchanged (pending Q12) | N (no validation in scope) | `Test` |
| 2 | `last-name` (root/last-name) | `last-name` (root/last-name) | Pass-through, unchanged (pending Q12) | N (no validation in scope) | `LeadAPITesting1` |
| 3 | `phone` (root/phone) | `phone` (root/phone) | Pass-through, unchanged, string (pending Q12) | N (no validation in scope) | `07989480687` |
| 4 | `email` (root/email) | `email` (root/email) | Pass-through, unchanged (pending Q12). Proposed tracking field (Q7). Possible Kafka key (Q13). | N (no validation in scope) | `testleadapitesting1@calor.co.uk` |
| 5 | `postcode` (root/postcode) | `postcode` (root/postcode) | Pass-through, unchanged (pending Q12) | N (no validation in scope) | `GL3 1DL` |
| 6 | `address-line-one` (root/address-line-one) | `address-line-one` (root/address-line-one) | Pass-through, unchanged (pending Q12) | N (no validation in scope) | `Ref County Durham Dowco Hous` |
| 7 | OPEN: `addional-comments` as in the document, or `additional-comments` (Q11) | Same name as the source | OPEN: pass-through under the exact field name Sitecore sends (Q11, Q12) | N (no validation in scope) | `Testing Lead, please ignore` |
| 8 | `form-source` (root/form-source) | `form-source` (root/form-source) | Pass-through, unchanged (pending Q12) | N (no validation in scope) | `HE Fuel Switch Enquiry` |
| 9 | `lead-channel` (root/lead-channel, array of string) | `lead-channel` (root/lead-channel, array of string) | Pass-through, unchanged; array kept as an array (pending Q12) | N (no validation in scope) | `["Webform"]` |
| 10 | `lead-source` (root/lead-source, array of string) | `lead-source` (root/lead-source, array of string) | Pass-through, unchanged; array kept as an array (pending Q12) | N (no validation in scope) | `["Digital"]` |

Response profile (WSS output): OPEN. It depends on the HTTP status and body contract in spec open question 9.
