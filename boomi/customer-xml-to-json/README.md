# Customer XML to JSON

A Boomi process that converts a customer XML document into JSON. Each customer has three fields: ID, name, and phone number.

## Flow

```
Customer XML to JSON (reusable, Data Passthrough)
  [Start: Data Passthrough] → [Map: Customer XML to JSON Map] → [Return Documents: Customer JSON]

TEST Customer XML to JSON (harness)
  [Start: No Data] → [Message: sample XML] → [Process Call] → [Notify: log JSON] → [Stop]
```

You can call the main process from any parent process, such as a WSS listener, a Disk/SFTP pickup or a scheduled job. The test harness is there because the Boomi execute API can't inject a document into a process.

## Field mapping

| XML (source)                          | Key | JSON (target)               | Key |
|---------------------------------------|-----|-----------------------------|-----|
| `Customers/Customer/CustomerID`       | 3   | `customers[].customerId`    | 7   |
| `Customers/Customer/CustomerName`     | 4   | `customers[].customerName`  | 8   |
| `Customers/Customer/PhoneNumber`      | 5   | `customers[].phoneNumber`   | 9   |

`Customer` repeats in the XML (`maxOccurs="-1"`) and `customers` is a JSON array, so one XML document with N customers becomes one JSON document with N array entries. All fields are character type, so leading zeros in IDs and `+`/`-` in phone numbers are kept.

Sample input and expected output are in `samples/`.

## Components

| File | Type | Name |
|------|------|------|
| `profile.xml/Customer_XML_Profile.xml` | `profile.xml` | Customer XML Profile |
| `profile.json/Customer_JSON_Profile.xml` | `profile.json` | Customer JSON Profile |
| `transform.map/Customer_XML_to_JSON_Map.xml` | `transform.map` | Customer XML to JSON Map |
| `process/Customer_XML_to_JSON.xml` | `process` | Customer XML to JSON |
| `process/TEST_Customer_XML_to_JSON.xml` | `process` | TEST Customer XML to JSON |

## Deploying with the bc-integration plugin

Create the components in dependency order. After each create, copy the generated component ID into the placeholders of the files that come after it:

1. `boomi-folder-create.sh "CustomerXmlToJson"` gives you `{{FOLDER_ID}}` (used in every file)
2. Create both profiles. They give you `{{XML_PROFILE_ID}}` and `{{JSON_PROFILE_ID}}`, which go in the map.
3. Create the map. It gives you `{{MAP_ID}}`, which goes in `Customer_XML_to_JSON.xml`.
4. Create the main process. It gives you `{{PROCESS_ID}}`, which goes in `TEST_Customer_XML_to_JSON.xml`.
5. Create the test process, then deploy it and run it with `boomi-test-execute.sh --process-id <test-process-id>`. The Notify step logs the JSON.

```bash
S=<skill-path>/scripts
bash $S/boomi-component-create.sh profile.xml/Customer_XML_Profile.xml
bash $S/boomi-component-create.sh profile.json/Customer_JSON_Profile.xml
bash $S/boomi-component-create.sh transform.map/Customer_XML_to_JSON_Map.xml
bash $S/boomi-component-create.sh process/Customer_XML_to_JSON.xml
bash $S/boomi-component-create.sh process/TEST_Customer_XML_to_JSON.xml
bash $S/boomi-deploy.sh process/TEST_Customer_XML_to_JSON.xml
```

If a parent process deploys the main process, redeploy the parent whenever you change the main process.
