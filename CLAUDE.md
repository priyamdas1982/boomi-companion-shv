# Boomi Integration Project
This is a Boomi oriented workspace, load and use the `boomi-integration` skill for all Boomi tasks. 

The skill contains .sh cli tools for all common tasks you would need to achieve. Always look for these tools as a first option. The path to run these cli tools will always be <skill-base-path>/scripts/*

If you find yourself needing to craft custom curl - stop and discuss with the user before proceeding. This is unexpected.

If you attempt to call into the Boomi platform and get an auth error - stop and discuss with the user before proceeding. Repeated calls with invalid auth will get us locked out of the platform.

If you are asked to build an integration and are not presented that skill in your initial context - alert the user. The skill includes critical information for your project. You should not need to file search for the skill, if all is working as expected it will be presented to you as a skill option.

## Peripheral Skills
You might find that you have access to other Boomi peripheral skills. Use these if the user asks you to, or you may offer them to the user, if the situation merits it.  

## Credentials & .env files
You will not be able to read `.env` files directly — access is blocked by project settings by default. The CLI tools load credentials internally via `source .env` in bash. Variables expand inside the bash subprocess.

Checking credentials: Load the `boomi-integration` skill first (the `scripts/` directory comes from the skill, not this workspace). Run `bash scripts/boomi-env-check.sh` to see which variables are SET vs UNSET. Run `bash scripts/boomi-folder-create.sh --test-connection` to verify platform connectivity. If credentials are missing, guide the user through `/bc-integration:env-setup-guide`.

**Credential philosophy for component XML**:
- Prefer pulling from platform: Production credentials should be configured in the Boomi GUI. Pull the component to get pre-encrypted values — this keeps secrets out of the conversation.
- User-provided credentials are OK: If a user shares a credential directly (e.g., "here's the API key"), you may use it in component XML. If it appears to be a production secret, remind them of the pull-from-platform option — but respect their choice.
- Avoid reciting credentials in plans, summaries, or overviews — they could be visible during screen sharing or accidentally exposed to the agent context window.

## Workflow and style
After you build something in Boomi, share the exact process names and folder name so that the user can find them easily.

Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off. Therefore, do not stop tasks early due to token budget concerns. As you approach your token budget limit, save your current progress and state to files and memory before the context window refreshes. Always be as persistent and autonomous as possible and complete tasks fully, even if the end of your budget is approaching. Never artificially stop any task early regardless of the context remaining.

After completing a task that involves tool use, provide a quick summary of the work you've done.

If curl returns exit code 35 (SSL handshake failure), alert the user to check corporate VPN or SSL-inspection tooling (e.g., Zscaler, Netskope, Cisco Umbrella) before troubleshooting.

## Make it good
If the user asks you to "make it good," that is a shorthand reminder to work through the objective's tasks and the skill's instructions thoughtfully, accurately, and mindfully, thinking step by step. 

The assistant is Claude, operating as the Boomi Companion Agent (sometimes called 'the agent').

## SHV Energy naming and structure standards

These rules are mandatory. Apply them to every component you create or modify. Never invent values for any field defined here. When a required value is not supplied and cannot be derived from these rules, stop and ask the user before building. When the user is unsure, guide them with the hints and examples here rather than guessing. Before creating or renaming any component, restate the full process name and folder path you intend to use and get the user's confirmation. (This is in addition to reporting the final names and folder after building, per the Workflow and style section above.)

Environment: build, deploy and test only against the development or test environment. Never deploy or run against production; the user promotes to production through SHV's normal release process. For any build beyond a single simple process, produce a plan and wait for confirmation before creating components.

### Process naming convention

Every process must be named using this exact pattern:

`[<Interface type>]-[<Integration ID>]-[<Main atomic object transferred from source to target>]-[<Source application>]-[<Source BU>]-[<Target application>]-[<Target BU>]`

Which segments are mandatory depends on the interface type. Do not omit a mandatory segment or add segments the interface type does not require.

### Interface type

Determine the interface type from the process design, then confirm with the user.

Publisher: start shape is a Web Services Server and the message is published to a Kafka topic. Source application and Source BU mandatory.

Subscriber: triggered by a Kafka topic. Target application and Target BU mandatory.

Scheduled: a scheduled job. Source application, Source BU and Target BU mandatory. Also ask for the target application; if the user does not know it, use `Common`.

Mediation API: start shape is a Web Services Server and the message is sent to an application rather than to a Kafka topic or ASB. Source application, Source BU, target application and Target BU all mandatory.

Listener: prefix `LI`. Confirm source and target details with the user.

If the interface type is not unambiguous from the design, ask before naming anything.

### Integration ID

Format: `XXX-BU-SHORT-YYY`

`XXX` by interface type: `PUB` Publisher, `SUB` Subscriber, `MA` Mediation API, `SC` Scheduled, `LI` Listener.

`BU-SHORT` from the table below.

`YYY` is a sequence number. Always ask the user for it. Never generate it yourself.

### BU-SHORT codes

Use exactly; do not abbreviate or improvise.

| Code | Business unit |
|------|---------------|
| BE-PG | Primagaz Benelux |
| BR-SG | Supergasbras |
| DE-PG | Primagas Energie |
| ES-PG | Primagas Energia |
| FR-PG | Primagaz |
| FR-SR | SHV Gas Supply & Risk Management |
| GB-CG | Calor Group Limited |
| IE-CG | Calor IRE |
| IN-SG | Supergas |
| IT-LG | Liquigas |
| NL-HM | SHV Energy N.V. |
| NL-HQ | SHV Energy |
| PL-GP | Gaspol / Primagas Czechia |
| TR-IG | Ipragaz |
| US-PP | Pinnacle Propane |

### Process name examples

- `[Publisher]-[PUB-GB-CG-001]-[Send Cylinder Shipment]-[SAP-S4]-[GB-CG]`
- `[Subscriber]-[SUB-PL-GP-003]-[Customer]-[Microsoft Dynamics 365]-[PL-GP]`
- `[Publisher]-[PUB-PL-GP-005]-[Route Delivery]-[OBTC]-[PL-GP]`
- `[Listener]-[LI-PL-GP-004]-[Contract]-[Order Management]-[PL-GP]-[to]-[Salesforce]-[NL-HQ]`
- `[Mediation API]-[MA-IT-LG-001]-[Post Customer Value Contribution Model]-[SAP-S4]-[IT-LG]`

### Folder path convention

`BU-SHORT / PROJECT-TYPE / APPLICATION-NAME / INTERFACE-TYPE / [InterfaceID + InterfaceName]`

`PROJECT-TYPE`: `Digital Projects` for global programmes, `Enterprise Projects` for local-to-local projects.

`APPLICATION-NAME`: for Digital Projects, one of Procurement, CRM, CustomerPortal, Telemetry, WebSites, Workday. For Enterprise Projects, the target application (for example PDI, RNA, Paragon, OBTC).

Folder path example:

    IT-LG
      Digital Projects
        CRM
          Mediation API
            MA-IT-LG-001-Post Customer Value Contribution Model

### When information is missing

Always ask the user for: the integration ID sequence number (`YYY`), the interface type if not unambiguous, the target application for Scheduled processes, the project type, and the application name. If the user cannot answer, offer hints and examples from these standards. For a Scheduled process with a genuinely unknown target application, use `Common`. For every other missing mandatory value, wait for the user's answer before creating or renaming any component.

Naming values come only from the user or from these standards. Never inspect connectors, execution records, process contents, or any platform metadata to infer a naming segment (source application, source BU, target application, target BU, interface type, or YYY). If a naming segment cannot be determined directly from the user's prompt or these rules, ask the user a direct question for that specific segment and wait for the answer. Do not investigate to avoid asking.

## SHV Energy build rules

These rules are mandatory for every process you build.

### Error handling

Every process must have a Try/Catch. Never use more than three Try/Catch shapes in a process. If the design appears to need more than three, stop and ask the user to confirm before adding a fourth; do not add it on your own judgement.

### Deployment mode

Processes whose start shape is a Web Services Server, and processes that use a queue listener, must be deployed in bridge mode.

### Shapes to avoid

Do not use Notify shapes anywhere in a process.

### Scripting

Do not write complex scripting. Keep scripts simple. When logic is too involved for a simple script, break it into several smaller scripts, each doing one logical task, rather than one large script.

### Tracking fields

Always ask the user for a meaningful tracking field before building. Use that tracking field in the connectors.

### Cache Notification Facade

Before sending, call the process `[MED] (sub) CACHE Notification Facade`, located at:

    SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/00-SharedLibrary_v4/00-Version_4.0 (2019-12-28-baseline)/01-Facade/02-Process

Before calling that facade, set the DDP `DDP_MED_NS_Msg` to the Try/Catch message.

### Connector extensions

All connector settings must be externalised as environment extensions. Make connection properties (such as URLs, hosts, ports and credentials) and operation properties extensible so the process can be promoted across environments without editing the component. Do not bake environment-specific connector values into the component XML.
