# Review findings: PUB-GB-CG-043

> Round 1 was written by the reviewer but its file write was refused by Claude Code ("Subagents should
> return findings as text, not write report files"). The orchestrator saved the reviewer's returned text
> below verbatim, on the user's instruction (2026-10-08: "3. yes").

## Round 1

Reviewed against spec revision 5 (hash e163319eb14898d5f28a5ceedd3a3f991c5b7ba579f0af7674067352d1138899, recomputed and matching), the pulled XML under `build/components/`, `build/build-log.md` "Attempt 3" and `.claude/review-checklist.md`. Platform cross-check, read only: `boomi-version-history.sh` shows C1, C2, C3, C5, C6, C7, C8 at version 1 (current, main), the same as the pulled XML. C4 c85b494e is still version 9 and C9 338df4f8 is still version 1. `boomi-component-search.sh` and `boomi-folder-list.sh` place C9 in folder RjoyOTg5MzY4 `SHV Energy N.V./02-Deployable/Framework/01-Framework_v4 (FOR DISTRIBUTION ONLY!)/00-SharedLibrary_v4/00-Version_4.0 (2019-12-28-baseline)/01-Facade/02-Process`.

### Findings

| ID | Severity | Rule / spec line | Component | Evidence | Status |
|----|----------|------------------|-----------|----------|--------|
| F-1-01 | blocker | EXT-01 / SHV Energy build rules > Connector extensions; spec.md: D6 and "Changes in revision 5" bullet 3 | [Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG] (`build/components/process/[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG].xml`) | `<ConnectionOverride id="c85b494e-...">` has 17 `<field ... overrideable="true"/>` and none has an `xpath`. The skill says such fields are "declared but inert": the extension value is ignored at runtime and the connection's baked-in value is used (`process_extensions.md` § Connection Overrides; `boomi_error_reference.md` Issue #31). C4 is a `GenericConnectionConfig` connector, and account process 1b208fa6 `[Publisher]-[PUB-GB-CG-043]-[CreateLead]-...` binds the same connection with `xpath="GenericConnectionConfig/field[@id='<id>']/@value"`. The spec's premise is also wrong. In the account processes pulled to `active-development/process/` I count 21 with a 9-field block, 5 with the 17-field block (including C1), 1 with 10 fields, 1 with 9 fields plus xpath, and 19 with no block. This is not "45 of 46". 7 of the 17 fields (`saslExtensions` and six `oauth/...` fields) do not exist in the C4 component. **Design change:** D6 tells the developer to build exactly this block with no xpath. The designer must revise D6, for example to use a platform-generated block with xpath (configure the override once in the GUI on C1 and pull it, or reuse the 1b208fa6 pattern) or to get user-confirmed evidence that this block binds at runtime. The developer then rebuilds C1. | OPEN |
| F-1-02 | minor | TRK-02 / SHV Energy build rules > Tracking fields; spec.md: Required values row 9, "Test notes" Tracking field | C3, C7, C8 (`build/components/connector-action/*.xml`) | `<TrackedField fieldId="33185" fieldName="primarykey">` = static `Email`, and `<TrackedField fieldId="33186" fieldName="primaryvalue">` = profile 27f55bec element 6 `email`. The tracked value is correct, but no tracked field is named `email`. The spec says "Tracked field `email`", and TC-02 expects "tracked field `email`" in Process Reporting. The slot choice is recorded only in build-log Decision 2. **Design change (wording only):** the spec should name the slots (`primarykey`=`Email`, `primaryvalue`=`email`) so that the tester checks the right fields. No build change is needed. | OPEN |
| F-1-03 | minor | SPC-03 / spec.md: Components C7, C8; Requirements NFR "maximum API response time 5 s" | C7 `PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.insert`, C8 `... gb-cg.q.leads.in.retry` (`build/components/connector-action/`) | `<field id="client_id" value="gb-cg.leads"/>`, `acks` `1`, `compression_type` `snappy`, `operation_timeout` `30000`. None of these values is in the spec. They come from framework template 7bfb1b08 (build-log Decision 4, which gives a reason). None of them depends on the environment, so EXT-03 is not breached. With TC-T retry 3, a broker problem could take about (1+3) x 30 s plus 30 s for C8 before any response, which is far beyond the 5 s NFR. `acks=1` can lose an acknowledged lead if the partition leader fails. **Design change:** the designer should record the C7/C8 producer settings in the spec with the user's confirmation, or confirm the template values. | OPEN |

Open: 1 blocker, 0 major, 2 minor. Disputed: 0.

### Checklist results

| Item | Result | Note |
|------|--------|------|
| NAM-01 | PASS | `name="[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]"`: every segment is bracketed and the segments are joined by `-` |
| NAM-02 | PASS | Publisher: Source application `Customer Portal` and Source BU `GB-CG`. No target segments |
| NAM-03 | PASS | shape1 `connectoraction connectorType="wss" actionType="Listen"`. Publishes to Kafka (shape6 and shape10, `connectorType="kafka"`, PRODUCE) |
| NAM-04 | PASS | Matches spec row 10 character for character (pulled XML and platform name) |
| NAM-05 | PASS | Every naming value is sourced from the user (Q1, Q2, Q3, follow-up A, design document) or CLAUDE.md (spec "Required values") |
| IID-01 | PASS | `PUB-GB-CG-043` |
| IID-02 | PASS | `PUB` = Publisher |
| IID-03 | PASS | `043` comes from the user's design document (spec row 2) |
| BU-01 | PASS | Only `GB-CG` is used (ID, name, folder) |
| FLD-01 | PASS | All 7 new components have `folderFullPath="SHV Energy N.V./01-Sandbox/01-Users/Priyam/BC/GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead"` (folderId Rjo4ODkxNDA5), which equals spec row 11. The sandbox prefix is the user's explicit choice (revision 4, "2. b") |
| FLD-02 | PASS | `Enterprise Projects` |
| FLD-03 | PASS | `Customer Portal` is the source application, not a target application. The literal CLAUDE.md hint is not met, but the spec records it as the user's explicit choice (follow-up A), and a Publisher has no target application. Left for the user to keep or change before promotion |
| ERR-01 | PASS | 3 x `shapetype="catcherrors"` (shape2 TC-A, shape5 TC-T, shape14 TC-F) |
| ERR-02 | PASS | Exactly 3 Try/Catch shapes, the maximum, accepted by the user (spec "Error handling") |
| DEP-01 | PASS | `<process ... workload="bridge" allowSimultaneous="true">`. The start shape is WSS |
| DEP-02 | N/A | No queue listener. The start shape is WSS |
| SHP-01 | PASS | No `shapetype="notify"` in C1. `test/test-report.md` lists no temporary Notify (it is still the empty template). Build-log Attempt 3 says none were added |
| SCR-01 | PASS | One script (shape3 "Check JSON body", groovy2). It only classifies the body into `DDP_VALIDATION_ERROR` and passes the document through |
| SCR-02 | PASS | About 25 lines, one loop, no nesting beyond try/catch, single responsibility |
| TRK-01 | PASS | Spec row 9: `email` (user Q7) |
| TRK-02 | PASS | Bound on C3, C7 and C8 through `primarykey`=`Email` and `primaryvalue`=profile element `email` (key 6, profile 27f55bec, which matches C5). Developer point 4: an acceptable binding of the user's field, but the spec should name the slots (F-1-02) |
| CNF-01 | PASS | shape18 and shape24 `processcall processId="338df4f8-af86-44f9-855c-943d8d0d478f" wait="true" abort="true"`. Name and folder verified read-only on the platform (see header) |
| CNF-02 | PASS | shape17 (into shape18) and shape23 (into shape24) set `dynamicdocument.DDP_MED_NS_Msg` from `meta.base.catcherrorsmessage` |
| EXT-01 | FAIL | The connection block is declared, but none of its fields has an `xpath`, so per the skill it is likely inert. See F-1-01. Developer point 1 is confirmed: the spec's D6 premise is wrong |
| EXT-02 | PASS | The only Listen operation is C3 (WSS). Its fields (objectName, profiles, input/output type) are the API contract, not environment-dependent, and the spec says so. Developer point 3: no platform-generated WSS OperationOverride exists to copy (0 of 47 pulled processes), and the skill forbids hand-authoring one, so no override is correct. C7 and C8 are PRODUCE, so they are exempt (CLAUDE.md "Connector extensions", Exception) |
| EXT-03 | PASS | No URL, host, credential or other environment value in C1, C3, C7 or C8. The topics are fixed in C7 and C8 under the CLAUDE.md exception (spec row 14). The C7/C8 fixed producer settings do not depend on the environment (F-1-03 is a spec-completeness point) |
| ENV-01 | PASS | The build log records deployments only to 1-DEV (693e8bc2-46f8-4c7f-8259-8dcf6cf0f264, user-confirmed development): C1 package 2cb065e7, C2 package d2229e66. No executions. The test report has no rounds yet |
| SPC-01 | PASS | C1, C2, C3, C5, C6, C7 and C8 are in `build/components/`. C4 and C9 are reused and were not pulled into the build, as the spec says. No extra components |
| SPC-02 | PASS | No map (pass-through, mapping rows 1 to 10): S1 re-stores the same bytes. H1/H2: `<dynamicProperties/>` on shape6 and shape10, no header or key fields in C7/C8. R1/R2: shape8 and shape12 `{"status":"accepted"}`, shape20 `{"status":"rejected","message":"'{1}'"}` from `meta.base.catcherrorsmessage`, shape26 fixed 500 text. Quote escaping is correct. C2: `urlPath="gb-cg-leads/v1"`, route `httpMethod="POST" objectName="leads" urlPath=""` (D5) |
| SPC-03 | PASS | Build log "Deviations: None". Decisions 1 to 8 each give a reason. Developer point 5 (C7/C8 values not in the spec) is raised as F-1-03. Developer point 2: `dynamicdocument.outstatuscode` has an account precedent (`[MED] - CREATE EmailAPI`, confirmed in the locally pulled XML), which V3 allows. It is still unconfirmed against Boomi docs and at runtime, and the tester must confirm it in TC-01 (202) and TC-08 (400) |
| R1 | PASS | shape5 `catcherrors catchAll="true" retryCount="3"`. Try path: shape6 (C7 583b0437) -> shape7 "Response 202" -> shape8 "Accepted" -> shape9 Return Documents "Accepted". Nothing else |
| R2 | PASS | shape5 Catch -> shape10 (C8 be398af2, `objectTypeId="gb-cg.q.leads.in.retry"`) -> shape11 "Response 202 (parked)" -> shape12 "Accepted (parked)" -> shape13 Return Documents "Accepted - parked on retry topic". No facade call, no `DDP_MED_NS_Msg`, no header or key |
| R3 | PASS (structure) | shape2 Try -> shape3 -> shape4 True -> shape5, so TC-T and its catch path sit inside the TC-A try path. Runtime behaviour is unconfirmed (V1 for TC-T, follow-up F2) |
| R4 | PASS | shape2 `catchAll="true" retryCount="0"`. Catch -> shape22 `branch numBranches="2"`, dragpoint 1 -> shape23 and dragpoint 2 -> shape25 |
| R5 | PASS | shape23 `DDP_MED_NS_Msg` = `meta.base.catcherrorsmessage` -> shape24 processcall 338df4f8, `wait="true" abort="true"`, `<returnpaths/>`, no dragpoints |
| R6 | PASS (structure) | shape25 `outstatuscode`=`500` -> shape26 `'{"status":"error","message":"Technical error. The lead was not accepted."}'` -> shape27 Return Documents "Error". Runtime order and a single-document response are unconfirmed (V6 for BR-A, follow-up F3). The status property is subject to V3 |
