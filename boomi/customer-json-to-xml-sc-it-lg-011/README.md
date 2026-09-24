# Customer JSON to XML (SC-IT-LG-011)

A scheduled Boomi process that converts one SFDC Customer JSON document into SAP Customer XML for Liquigas.

This is the conversion only. The SFDC source and the SAP target are placeholders to be replaced with real connectors later.

## Naming

| Item | Value |
|------|-------|
| Process name | `[Scheduled]-[SC-IT-LG-011]-[Customer]-[SFDC]-[IT-LG]-[SAP]-[IT-LG]` |
| Folder path | `IT-LG / Enterprise Projects / SAP / Scheduled / SC-IT-LG-011-Customer` |
| Interface type | Scheduled |
| Integration ID | `SC-IT-LG-011` |
| Source | SFDC, IT-LG (Liquigas) |
| Target | SAP, IT-LG (Liquigas) |
| Tracking field | customerId (`DDP_customerId`) |

## Flow

```
[Start: No Data] → [Try/Catch]
   Try   → [Message: PLACEHOLDER - SFDC Customer source] → [Set Properties: DDP_customerId = customerId]
           → [Map: SFDC Customer JSON to SAP Customer XML] → [Stop: PLACEHOLDER - SAP send]
   Catch → [Set Properties: DDP_MED_NS_Msg = Try/Catch Message] → [Process Call: [MED] (sub) CACHE Notification Facade]
```

The process follows the SHV build rules:

- It has one Try/Catch (catch all, no retries).
- It has no Notify shapes and no scripting.
- The catch path sets `DDP_MED_NS_Msg` to the Try/Catch message and then calls the Cache Notification Facade (wait, abort on error, no return paths).
- It has no connectors yet, so there's nothing to set up as environment extensions. `DDP_customerId` is ready to use as the tracking field on the connectors when they're added.
- Process options: general mode, no simultaneous executions, update run dates on.

The process doesn't need bridge mode because it has no Web Services Server start and no queue listener. The schedule is set in Atom Management after deployment.

## Field mapping

| JSON (source) | Key | XML (target) | Key |
|---------------|-----|--------------|-----|
| `customerName` | 3 | `Customer/CustomerName` | 2 |
| `customerId`   | 4 | `Customer/CustomerId`   | 3 |
| `phoneNumber`  | 5 | `Customer/PhoneNumber`  | 4 |
| `city`         | 6 | `Customer/City`         | 5 |

Sample input and expected output are in `samples/`.

## Components

Created on the `main` branch in folder `SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/IT-LG/Enterprise Projects/SAP/Scheduled/SC-IT-LG-011-Customer` (`Rjo4ODYwODg3`). Not deployed and not tested.

| Component | Type | ID |
|-----------|------|----|
| `j.SFDC.Customer.IN` | `profile.json` | `a1e8c5b2-f40d-43e2-9fd6-75c2855d666c` |
| `x.SAP.Customer.OUT` | `profile.xml` | `8724bec2-a21d-4855-8728-571fb8b12609` |
| `SFDC Customer JSON to SAP Customer XML` | `transform.map` | `af005dfc-a42d-44bb-b4ea-a858b84f9d8d` |
| `[Scheduled]-[SC-IT-LG-011]-[Customer]-[SFDC]-[IT-LG]-[SAP]-[IT-LG]` | `process` | `c8ccd358-bbbb-4b3b-a7a3-cce09d434377` |
| `[MED] (sub) CACHE Notification Facade` (existing, called from the catch path) | `process` | `338df4f8-af86-44f9-855c-943d8d0d478f` |

## Next steps (not in this build)

- Replace the `PLACEHOLDER - SFDC Customer source` Message step with the Salesforce connector.
- Replace the `PLACEHOLDER - SAP send` Stop step with the SAP connector.
- Make both connectors' connection and operation settings environment extensions, and put `customerId` on them as the tracking field.
