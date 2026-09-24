# Person XML to CSV (SC-IT-LG-006)

A scheduled Boomi process that converts person XML into CSV. Each person has two fields: name and lastname.

This is the conversion only. The SAP source and the Common target are placeholders to be replaced with real connectors later.

## Naming

| Item | Value |
|------|-------|
| Process name | `[Scheduled]-[SC-IT-LG-006]-[Person]-[SAP]-[IT-LG]-[Common]-[IT-LG]` |
| Folder path | `IT-LG / Enterprise Projects / Common / Scheduled / SC-IT-LG-006-Person` |
| Interface type | Scheduled |
| Integration ID | `SC-IT-LG-006` |
| Source | SAP, IT-LG (Liquigas) |
| Target | Common, IT-LG (Liquigas) |
| Tracking field | lastname |

## Flow

```
[Start: No Data] → [Try/Catch]
   Try   → [Message: PLACEHOLDER SAP Persons XML] → [Map: Person XML to CSV] → [Stop: PLACEHOLDER Send to Common]
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

| XML (source)                | Key | CSV (target)      | Key |
|-----------------------------|-----|-------------------|-----|
| `Persons/Person/name`       | 3   | `name` (column 1) | 3   |
| `Persons/Person/lastname`   | 4   | `lastname` (column 2) | 4 |

`Person` repeats, so one XML document with N persons becomes one CSV document with a header row plus N data rows. The CSV profile is comma-delimited with a header row (`useColumnHeaders="true"`), and uses double quotes as the text qualifier, so a value containing a comma is quoted rather than splitting the row.

Sample input and expected output are in `samples/`.

## Components

| File | Type | Name |
|------|------|------|
| `profile.xml/SC-IT-LG-006_Person_XML_Profile.xml` | `profile.xml` | SC-IT-LG-006 Person XML Profile |
| `profile.flatfile/SC-IT-LG-006_Person_CSV_Profile.xml` | `profile.flatfile` | SC-IT-LG-006 Person CSV Profile |
| `transform.map/SC-IT-LG-006_Person_XML_to_CSV_Map.xml` | `transform.map` | SC-IT-LG-006 Person XML to CSV Map |
| `process/SC-IT-LG-006_Person_SAP_to_Common.xml` | `process` | `[Scheduled]-[SC-IT-LG-006]-[Person]-[SAP]-[IT-LG]-[Common]-[IT-LG]` |

Created on the `main` branch in folder `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/IT-LG/Enterprise Projects/Common/Scheduled/SC-IT-LG-006-Person` (`Rjo4ODYwMzk3`). Not deployed yet.

| Component | ID |
|-----------|----|
| SC-IT-LG-006 Person XML Profile | `e8534329-2283-49a7-aa23-dff4be27ba37` |
| SC-IT-LG-006 Person CSV Profile | `a869b8e1-bd42-46f4-a563-744431d69f58` |
| SC-IT-LG-006 Person XML to CSV Map | `6c0775e5-04fd-4ddc-9109-97f2193c7592` |
| `[Scheduled]-[SC-IT-LG-006]-[Person]-[SAP]-[IT-LG]-[Common]-[IT-LG]` | `a60ed4ff-4ee2-4bcb-bd8d-c0f248bc68d1` |
| `[MED] (sub) CACHE Notification Facade` (existing, called from the catch path) | `338df4f8-af86-44f9-855c-943d8d0d478f` |

## Loading onto the platform with the bc-integration plugin

Create the components in dependency order, and only in the development or test environment. After each create, copy the new component ID into the placeholders in the files that come after it:

1. Find or create the folder `IT-LG / Enterprise Projects / Common / Scheduled / SC-IT-LG-006-Person`. Its ID replaces `{{FOLDER_ID}}` in every file.
2. Create both profiles. Their IDs replace `{{XML_PROFILE_ID}}` and `{{CSV_PROFILE_ID}}` in the map.
3. Create the map. Its ID replaces `{{MAP_ID}}` in the process.
4. Look up the component ID of `[MED] (sub) CACHE Notification Facade`. It's in `SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/00-SharedLibrary_v4/00-Version_4.0 (2019-12-28-baseline)/01-Facade/02-Process`. Put that ID in `{{CACHE_NOTIFICATION_FACADE_ID}}` in the process.
5. Create the process.

```bash
S=<skill-path>/scripts
bash $S/boomi-component-create.sh profile.xml/SC-IT-LG-006_Person_XML_Profile.xml
bash $S/boomi-component-create.sh profile.flatfile/SC-IT-LG-006_Person_CSV_Profile.xml
bash $S/boomi-component-create.sh transform.map/SC-IT-LG-006_Person_XML_to_CSV_Map.xml
bash $S/boomi-component-create.sh process/SC-IT-LG-006_Person_SAP_to_Common.xml
```

## Next steps (not in this build)

- Replace the `PLACEHOLDER SAP Persons XML` Message step with the SAP connector. Before that, confirm which SAP interface to use: IDoc, BAPI/RFC or OData. The source profile may change to match it.
- Replace the `PLACEHOLDER Send to Common` Stop step with the real target connector, for example Disk V2 or SFTP to write the CSV file.
- Set both connectors up as environment extensions, and put lastname on them as the tracking field.
