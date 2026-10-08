# Review checklist

Used by the `reviewer` agent on every review round. Each item is one checkable rule
from `CLAUDE.md`, and each one cites its source section. Cite the item ID (for example
`NAM-02`) and the CLAUDE.md section in every finding.

For each item, record PASS, FAIL or N/A in `review/findings.md` under "Checklist results".
A FAIL becomes a finding row. N/A needs a one-line reason.

Default severity is shown in brackets. The reviewer may raise a severity with a reason,
but never lower a **blocker** item.

Evidence must be specific: a file path under `build/components/`, the XML element or
attribute (for example `shapetype="catcherrors"`, `workload="bridge"`), and the shape
`name`/`userlabel` where relevant.

---

## Naming

Source: CLAUDE.md, "SHV Energy naming and structure standards" > "Process naming convention" and "Interface type".

- [ ] **NAM-01** [blocker] The process name follows the pattern
      `[<Interface type>]-[<Integration ID>]-[<Main atomic object>]-[<Source application>]-[<Source BU>]-[<Target application>]-[<Target BU>]`:
      each segment is wrapped in square brackets, and segments are joined by `-`.
- [ ] **NAM-02** [blocker] The process name contains exactly the mandatory segments for its interface type, with none omitted and none added:
      - Publisher: Source application and Source BU.
      - Subscriber: Target application and Target BU.
      - Scheduled: Source application, Source BU and Target BU, plus a target application (`Common` only if the user did not know it).
      - Mediation API: Source application, Source BU, Target application and Target BU.
      - Listener: the source and target details the user confirmed in the spec.
- [ ] **NAM-03** [blocker] The interface type segment matches the process design:
      - Publisher: the start shape is a Web Services Server and the message is published to Kafka.
      - Subscriber: triggered by a Kafka topic.
      - Scheduled: a scheduled job.
      - Mediation API: the start shape is a Web Services Server and the message goes to an application, not to Kafka or ASB.
      - Listener: prefix `LI`.
- [ ] **NAM-04** [blocker] The process name in the pulled XML matches the full process name in the approved spec exactly, character for character.
- [ ] **NAM-05** [major] Every naming value in the spec has a source of "user" or "CLAUDE.md". None was inferred from connectors, executions or platform metadata.
      Source: CLAUDE.md, "When information is missing".

## Integration ID

Source: CLAUDE.md, "Integration ID".

- [ ] **IID-01** [blocker] The Integration ID has the format `XXX-BU-SHORT-YYY`.
- [ ] **IID-02** [blocker] `XXX` matches the interface type: `PUB` Publisher, `SUB` Subscriber, `MA` Mediation API, `SC` Scheduled, `LI` Listener.
- [ ] **IID-03** [blocker] `YYY` equals the sequence number the user supplied, as recorded in the approved spec. It was not generated.

## BU-SHORT codes

Source: CLAUDE.md, "BU-SHORT codes".

- [ ] **BU-01** [blocker] Every BU code used, whether in the Integration ID, the BU segments of the process name or the folder path, is exactly one of:
      `BE-PG`, `BR-SG`, `DE-PG`, `ES-PG`, `FR-PG`, `FR-SR`, `GB-CG`, `IE-CG`, `IN-SG`, `IT-LG`, `NL-HM`, `NL-HQ`, `PL-GP`, `TR-IG`, `US-PP`.
      The code must not be abbreviated or improvised.

## Folder path

Source: CLAUDE.md, "Folder path convention".

- [ ] **FLD-01** [blocker] The component folder path is `BU-SHORT / PROJECT-TYPE / APPLICATION-NAME / INTERFACE-TYPE / [InterfaceID + InterfaceName]` and matches the approved spec exactly.
      Every component built for the interface sits in that folder, not in the account root.
- [ ] **FLD-02** [blocker] `PROJECT-TYPE` is `Digital Projects` or `Enterprise Projects`.
- [ ] **FLD-03** [blocker] `APPLICATION-NAME` is valid for the project type:
      - Digital Projects: one of Procurement, CRM, CustomerPortal, Telemetry, WebSites, Workday.
      - Enterprise Projects: the target application.

## Error handling

Source: CLAUDE.md, "SHV Energy build rules" > "Error handling".

- [ ] **ERR-01** [blocker] Every process has at least one Try/Catch shape (`shapetype="catcherrors"`).
- [ ] **ERR-02** [blocker] No process has more than three Try/Catch shapes. A fourth is allowed only when the spec records the user's explicit confirmation.

## Deployment mode

Source: CLAUDE.md, "SHV Energy build rules" > "Deployment mode".

- [ ] **DEP-01** [blocker] Every process whose start shape is a Web Services Server has `workload="bridge"` on its `<process>` element.
- [ ] **DEP-02** [blocker] Every process that uses a queue listener has `workload="bridge"`.

## Shapes to avoid

Source: CLAUDE.md, "SHV Energy build rules" > "Shapes to avoid".

- [ ] **SHP-01** [blocker] No process contains a Notify shape (`shapetype="notify"`).
      The only exception is a temporary Notify that `test/test-report.md` lists as added for testing in the current round and not yet removed. Raise that as a **major**: it must still be deleted.
      Before `/build-interface` can finish, a final pull must show no Notify shapes in any process.

## Scripting

Source: CLAUDE.md, "SHV Energy build rules" > "Scripting".

- [ ] **SCR-01** [major] Every script (inline Data Process script, Process Script component, or map script) does one logical task.
- [ ] **SCR-02** [major] No script is complex. As a guide, flag any script over about 40 lines, with nested loops, or with several unrelated responsibilities. Logic that is too involved must be split into several smaller single-purpose scripts.

## Tracking fields

Source: CLAUDE.md, "SHV Energy build rules" > "Tracking fields".

- [ ] **TRK-01** [blocker] The spec records the tracking field the user supplied.
- [ ] **TRK-02** [blocker] That tracking field is configured in the connector operations, in the operation's `<Tracking><TrackedFields>` (or the connector's equivalent), as listed in the spec.

## Cache Notification Facade

Source: CLAUDE.md, "SHV Energy build rules" > "Cache Notification Facade".

- [ ] **CNF-01** [blocker] Before sending, the process calls `[MED] (sub) CACHE Notification Facade` (a Process Call shape, `shapetype="processcall"`).
      The called process must be the one in
      `SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/00-SharedLibrary_v4/00-Version_4.0 (2019-12-28-baseline)/01-Facade/02-Process`.
      Verify the `processId` against a read-only pull or search of that folder.
- [ ] **CNF-02** [blocker] On the path into that Process Call, a Set Properties shape sets the DDP `DDP_MED_NS_Msg` to the Try/Catch message before the call.

## Connector extensions

Source: CLAUDE.md, "SHV Energy build rules" > "Connector extensions".

- [ ] **EXT-01** [blocker] Every connection used by the process has its settings (URLs, hosts, ports, credentials and similar) declared as extensible in `<bns:processOverrides>`.
- [ ] **EXT-02** [blocker] Every Listen operation's environment-dependent properties are declared as extensible in `<bns:processOverrides>`. Operations with any other action (for example Kafka Produce) cannot be extended in Boomi and are exempt; see the exception in CLAUDE.md.
- [ ] **EXT-03** [blocker] No environment-specific connector value is fixed in component XML without also being extensible.

## Environment

Source: CLAUDE.md, "SHV Energy naming and structure standards" (Environment paragraph).

- [ ] **ENV-01** [blocker] `build/build-log.md` and `test/test-report.md` record only development or test environment deployments. Any production deployment or execution is a blocker.

## Spec conformance

Source: the approved spec, `design/spec.md` and `design/mapping.md`.

- [ ] **SPC-01** [major] Every component listed in the spec exists in `build/components/`, and there are no unexplained extra components.
- [ ] **SPC-02** [major] Every mapping row in `design/mapping.md` is implemented in the map, or is listed as a deviation in `build/build-log.md`.
- [ ] **SPC-03** [major] Every deviation in `build/build-log.md` has a reason. Any deviation that touches a naming, folder, tracking-field or CLAUDE.md rule is a blocker.
