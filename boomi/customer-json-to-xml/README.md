# Customer JSON to XML (SC-GB-CG-002)

A scheduled Boomi process that converts customer JSON into XML. Each customer has four fields: ID, name, phone number and city.

This is the conversion only. The Salesforce source and the SAP-S4 target are placeholders to be replaced with real connectors later.

## Naming

| Item | Value |
|------|-------|
| Process name | `[Scheduled]-[SC-GB-CG-002]-[Customer]-[Salesforce]-[GB-CG]-[SAP-S4]-[GB-CG]` |
| Folder path | `GB-CG / Digital Projects / CRM / Scheduled / SC-GB-CG-002-Customer` |
| Interface type | Scheduled |
| Integration ID | `SC-GB-CG-002` |
| Source | Salesforce, GB-CG (Calor Group Limited) |
| Target | SAP-S4, GB-CG (Calor Group Limited) |
| Tracking field | Customer ID |

## Flow

```
[Start: No Data] → [Try/Catch]
   Try   → [Message: PLACEHOLDER Salesforce Customers JSON] → [Map: Customer JSON to XML] → [Stop: PLACEHOLDER Send to SAP-S4]
   Catch → [Set Properties: DDP_MED_NS_Msg = Try/Catch Message] → [Process Call: [MED] (sub) CACHE Notification Facade]
```

The process follows the SHV build rules:

- It has one Try/Catch, so it stays within the limit of three.
- It has no Notify shapes.
- It uses no scripting.
- The catch path sets `DDP_MED_NS_Msg` to the Try/Catch message and then calls the Cache Notification Facade.
- It has no connectors yet, so there's nothing to set up as environment extensions or to put the tracking field on.

The process doesn't need bridge mode because it has no Web Services Server start and no queue listener. The schedule itself is set in Atom Management after deployment. It isn't part of the component XML.

## Field mapping

| JSON (source)               | Key | XML (target)                          | Key |
|-----------------------------|-----|---------------------------------------|-----|
| `customers[].customerId`    | 7   | `Customers/Customer/CustomerID`       | 3   |
| `customers[].customerName`  | 8   | `Customers/Customer/CustomerName`     | 4   |
| `customers[].phoneNumber`   | 9   | `Customers/Customer/PhoneNumber`      | 5   |
| `customers[].city`          | 10  | `Customers/Customer/City`             | 6   |

`customers` is a JSON array and `Customer` repeats in the XML, so one JSON document with N customers becomes one XML document with N `Customer` elements. All fields are text, so leading zeros in IDs and `+`/`-` in phone numbers are kept.

Sample input and expected output are in `samples/`.

## Components

| File | Type | Name |
|------|------|------|
| `profile.json/SC-GB-CG-002_Customer_JSON_Profile.xml` | `profile.json` | SC-GB-CG-002 Customer JSON Profile |
| `profile.xml/SC-GB-CG-002_Customer_XML_Profile.xml` | `profile.xml` | SC-GB-CG-002 Customer XML Profile |
| `transform.map/SC-GB-CG-002_Customer_JSON_to_XML_Map.xml` | `transform.map` | SC-GB-CG-002 Customer JSON to XML Map |
| `process/SC-GB-CG-002_Customer_Salesforce_to_SAP-S4.xml` | `process` | `[Scheduled]-[SC-GB-CG-002]-[Customer]-[Salesforce]-[GB-CG]-[SAP-S4]-[GB-CG]` |

None of these components exist on the platform yet.

## Loading onto the platform with the bc-integration plugin

Create the components in dependency order, and only in the development or test environment. After each create, copy the new component ID into the placeholders in the files that come after it:

1. Find or create the folder `GB-CG / Digital Projects / CRM / Scheduled / SC-GB-CG-002-Customer`. Its ID replaces `{{FOLDER_ID}}` in every file.
2. Create both profiles. Their IDs replace `{{JSON_PROFILE_ID}}` and `{{XML_PROFILE_ID}}` in the map.
3. Create the map. Its ID replaces `{{MAP_ID}}` in the process.
4. Look up the component ID of `[MED] (sub) CACHE Notification Facade`. It's in `SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/00-SharedLibrary_v4/00-Version_4.0 (2019-12-28-baseline)/01-Facade/02-Process`. Put that ID in `{{CACHE_NOTIFICATION_FACADE_ID}}` in the process.
5. Create the process.

```bash
S=<skill-path>/scripts
bash $S/boomi-component-create.sh profile.json/SC-GB-CG-002_Customer_JSON_Profile.xml
bash $S/boomi-component-create.sh profile.xml/SC-GB-CG-002_Customer_XML_Profile.xml
bash $S/boomi-component-create.sh transform.map/SC-GB-CG-002_Customer_JSON_to_XML_Map.xml
bash $S/boomi-component-create.sh process/SC-GB-CG-002_Customer_Salesforce_to_SAP-S4.xml
```

## Next steps (not in this build)

- Replace the `PLACEHOLDER Salesforce Customers JSON` Message step with a Salesforce query for Customer name, ID, phone and city. The Salesforce connection has to be created in the GUI. The Salesforce connector returns XML, so the source profile may change.
- Replace the `PLACEHOLDER Send to SAP-S4` Stop step with the SAP-S4 connector. Before that, confirm which SAP interface to use: IDoc, BAPI/RFC or OData.
- Set both connectors up as environment extensions, and put Customer ID on them as the tracking field.
