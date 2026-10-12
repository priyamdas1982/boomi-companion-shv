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

> The Round 1 re-review below was returned as text by the reviewer because its file write was refused again ("Subagents should return findings as text"). The orchestrator saved it verbatim on 2026-10-12, as it did for Round 1 on the user's instruction.

## Round 1 re-review (revision 9)

Reviewed 2026-10-12 against spec revision 9 (`design/spec.md`, `design/mapping.md`). Hash recomputed from the repo root with the pipeline method (`sha256sum interfaces/PUB-GB-CG-043/design/spec.md interfaces/PUB-GB-CG-043/design/mapping.md | sha256sum`): 449c119cc3d76fcd3edf91e564459ba629abcfaf2cadbbceab6488b32a917078, which matches `pipeline-state.md`. A plain `sha256sum spec.md` gives e2a27e29..., which is expected because it is a different command. Also reviewed: the pulled XML in `build/components/`, `build/build-log.md` Attempts 4 to 8, `build/fix-response.md` (Round 1 to revision 9), `.claude/review-checklist.md`, spec review items R1 to R9, and CLAUDE.md, including "Kafka send failures", "Kafka topics must exist before the build" and "Connectivity checks first".

Platform cross-check, read only (`boomi-version-history.sh`): C1 135044a4 v4, C2 4c878feb v2, C3 0f214069 v1, C5 27f55bec v1, C6 f07edecd v1, C7 583b0437 v3 and C8 be398af2 v2 are the current versions on main, the same as the files in `build/components/`. C4 c85b494e is still v9 and C9 338df4f8 is still v1. C1 was pulled with `boomi-component-pull.sh` to a scratch path outside `interfaces/`, and `cmp` shows it is byte-identical to `build/components/process/[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG].xml`. `boomi-component-search.sh` puts C9 in folderId RjoyOTg5MzY4 (`.../01-Facade/02-Process`), the same folder as in Round 1. The C1 `ConnectionOverride` for c85b494e was diffed against the locally pulled 1b208fa6 (CreateLead) and is identical: 9 fields, each with `xpath`. Every field id exists in the local C4 copy, and C4 has exactly one more field, `consumer_group`. C1 contains no reference to `be398af2`.

### Round 1 findings re-checked

| ID | Severity | Rule / spec line | Component | Evidence | Status |
|----|----------|------------------|-----------|----------|--------|
| F-1-01 | blocker | EXT-01 / SHV Energy build rules > Connector extensions; spec.md: D6, rows 17 and 20 | C1 (`build/components/process/[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG].xml`) | `<ConnectionOverride id="c85b494e-58ab-4591-b946-76a9ec636414">` has 9 fields (`username`, `password`, `bootstrap_servers`, `service_principal`, `security_protocol`, `sasl_mechanism`, `private_certificate`, `polling_interval`, `polling_delay`), each with `xpath="GenericConnectionConfig/field[@id='<id>']/@value"`. The block is identical to the 1b208fa6 block. Every id exists in C4. The only uncovered field is `consumer_group`, which spec row 20 accepts (user: "2. a"). Build log Attempt 8 D6.6: the 1-DEV extension hash is unchanged before and after the deploy. Fix verified. | CLOSED |
| F-1-02 | minor | TRK-02 / SHV Energy build rules > Tracking fields; spec.md: row 9, Test notes "Tracking field" | C3, C7 (`build/components/connector-action/`) | Spec row 9 and the Test notes now name the slots: `primarykey` (33185) = `Email`, `primaryvalue` (33186) = C5 element `email`. C3 v1 and C7 v3 have `<TrackedField fieldId="33185" fieldName="primarykey">` with static `Email`, and `fieldId="33186" fieldName="primaryvalue"` with profile 27f55bec element 6 `email (Root/Object/email)`. The spec and the build agree. | CLOSED |
| F-1-03 | minor | SPC-03; spec.md: row 18, "Kafka producer settings", D7 | C7 `PUB-GB-CG-043 Kafka Produce gb-cg.q.leads.in.insert` (`build/components/connector-action/`) | The spec now records the C7 values with their sources: `acks` `all` (user), `operation_timeout` `3000` (user "1a"), and `client_id`/`compression_type` (template; recorded, no change requested). C7 v3 has `acks`=`all`, `operation_timeout`=`3000`, `client_id`=`gb-cg.leads` and `compression_type`=`snappy`. C8 keeps 5000, is unreferenced and is unchanged (F4). The NFR concern is handled by rows 19, 22 and 26. | CLOSED |

### Findings (revision 9)

| ID | Severity | Rule / spec line | Component | Evidence | Status |
|----|----------|------------------|-----------|----------|--------|
| F-1R-01 | minor | SPC-03 (spec conformance); spec.md: "Failure-path test approach" options A and C, "Error handling" intro, header Status | `design/spec.md` (no component) | Stale text contradicts the approved rows. Option C says "the TC-T retry count is 3, the TC-T catch path goes to the C8 produce". Option A technical-error says "one message on `gb-cg.q.leads.in.retry`, 202 `{"status":"accepted"}`". The "Error handling" intro says "The two Branch shapes added in revision 4", but there are now three (BR-K). Line 3 still says `Status: READY FOR APPROVAL` although the spec is approved. The build follows the current rows (R1, R2, rows 22 and 30), so no build change is needed. The risk is that the tester, who is rewriting the cases in parallel, takes failure-path expectations from the stale option text. **Design change (wording only):** mark options A and C as revision 5 history or update them to the revision 7 to 9 behaviour, say "three Branch shapes", and update the status line. | OPEN |
| F-1R-02 | minor | SPC-03; CLAUDE.md SHV Energy build rules > Kafka send failures; spec.md: V9, row 30, Follow-ups F2 | C1 BR-K `shape30` (`build/components/process/...xml`) | The guard "never a 202 after a failed send" rests on V9: a document that fails on BR-K branch 1 (C7) is not given to branch 2. V9 has no runtime proof for a C7 failure. Its runtime evidence, 22c61363, is a failing Process Call (abort = true) on BR-F, not a connector document error. The developer's documentation lookup found no source that says the opposite (see the assessment below). The user accepted review only for failure paths (row 16), so this is not a build defect. However, follow-up F2 lists only "V1 for TC-T" and does not list the V9 runtime check. That check appears only in D8 and in the Test notes "Kafka failure" row. If V9 were wrong, the result would be a breach of "Kafka send failures". **Design change (wording only):** add "V9: BR-K branch 2 does not run on a failed C7 attempt" to F2, so the user sees it as an open runtime confirmation. No build change. | OPEN |

Open: 0 blocker, 0 major, 2 minor. Disputed: 0.

**Assessment of the item the developer flagged (build log Attempt 8, V9).** The help.boomi.com "Branch step" sentence "Each branch receives a full copy of every document that enters the Branch step. Boomi Integration doesn't divide or split incoming documents across branches" does **not** contradict the design. In context, the sentence explains that branches are not split or load-balanced: every branch sees the whole document set. It says nothing about a document that has already failed on an earlier branch while an enclosing Try/Catch is active. The developer's reading in the build log is correct. Three sources support the design:

1. Skill `BOOMI_THINKING.md` (Try-Catch Steps): "When a document errors, processing halts for that document - subsequent steps and parallel branches don't execute."
2. help.boomi.com "Try/Catch step": "For any failed documents, the Try path is always executed first, followed by the Catch path."
3. Runtime 22c61363: the branch 2 skip ("No documents found") was logged before the TC-A error path.

C7 has `returnApplicationErrors="false"`, so a Kafka error fails the document rather than passing on as output. 93e06b38 shows TC-T catching and retrying C7 errors. The success leg is proven at runtime (04e4af6d: C7 once, "No documents found. Skipping execution for the Sent step.", then Response 202, then 202 `{"status":"accepted"}`). What remains is that the failure leg has not been observed with a C7 error specifically. It is accepted as review only (row 16) and should be visible in F2 (F-1R-02). No blocker or major is raised.

Other points checked since Round 1, with no finding:

- **Facade inputs:** shape23 (BR-A) and shape17 (BR-F) set FI-1 `DDP_MED_NS_Msg` = `meta.base.catcherrorsmessage` first. Then, in table order, they set FI-2 to FI-8 as `process.DPP_MED_*` with `valueType="execution"`: `Process Id`, `Process Name`, `Execution Id`, `Account Id`, `Atom Id`, `Atom Name`, and `Atom Id` for ContainerId. FI-9 to FI-15 are absent. D4 passed at runtime (22292eff: Document Cache Load succeeded, then 400).
- **TC-A placement:** shape4 True -> shape2 (TC-A), False -> shape14 (TC-F). shape14, shape16 and shape22 are not downstream of shape2's Try dragpoint.
- **TC-T:** shape5 has `retryCount="2"` (3 attempts). C7 `operation_timeout` is `3000`.
- **Exception "Kafka send failed":** shape28 has `stopsingledoc="true"`, `<exMessage>Kafka send to gb-cg.q.leads.in.insert failed after 3 attempts: {1}</exMessage>`, and {1} = `meta.base.catcherrorsmessage`. It is the only shape on the TC-T catch path and it is on the TC-A try path.
- **S2:** shape29 uses `groovy.json.JsonOutput.toJson([status: "error", message: msg])`. It defaults to "" when the DDP is null, keeps the properties, and is 16 lines with one purpose. It is fed by shape25 (`outstatuscode` 500, `DDP_ERROR_MESSAGE` = Try/Catch message) and ends in shape27 Return Documents "Error".
- **BR-K and Stop "Sent":** shape30 `branch numBranches="2"`. Dragpoint 1 -> shape6 (C7) -> shape31 `<stop continue="true"/>`. Dragpoint 2 -> shape7 "Response 202" -> shape8 `'{"status":"accepted"}'` -> shape9. shape5 Try goes to shape30. C7 is not wired to shape7.
- **Facade wait/abort:** shape18 and shape24 have `wait="true" abort="true"`, `<returnpaths/>` and no dragpoints, with no extra Try/Catch.
- **C2 exactMatch:** `<overrides ... exactMatch="true" httpMethod="POST" objectName="leads" urlPath=""/>` with base `urlPath="gb-cg-leads/v1"`. D5 was re-proven (404 on `/leads/leads`, no C1 execution).
- **V3:** `dynamicdocument.outstatuscode` is now confirmed at runtime for 202 (04e4af6d) and 400 (22292eff). 500 is review only.
- **CLAUDE.md new rules:** Kafka topics are confirmed in `pipeline-state.md` before the build (`gb-cg.q.leads.in.insert`; the build log records the gate). D0 connectivity checks are recorded first in Attempts 7 and 8, with credentials shown only as SET or EMPTY. "Kafka send failures" holds by structure: 3 attempts, then the Exception, TC-A, BR-A and a 500 with the text, and no 202 path after a failed send (subject to F-1R-02).

### Checklist results

| Item | Result | Note |
|------|--------|------|
| NAM-01 | PASS | `name="[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]"` |
| NAM-02 | PASS | Publisher: Source application `Customer Portal`, Source BU `GB-CG`, no target segments |
| NAM-03 | PASS | shape1 WSS Listen. shape6 Kafka PRODUCE to `gb-cg.q.leads.in.insert` |
| NAM-04 | PASS | Equals spec row 10 character for character (platform C1 v4) |
| NAM-05 | PASS | Unchanged. All values come from the user or CLAUDE.md (spec "Required values") |
| IID-01 | PASS | `PUB-GB-CG-043` |
| IID-02 | PASS | `PUB` = Publisher |
| IID-03 | PASS | `043` from the user's design document (row 2) |
| BU-01 | PASS | Only `GB-CG` |
| FLD-01 | PASS | C1, C2, C3, C5, C6, C7 and C8 are all in folderId Rjo4ODkxNDA5 `.../GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead` (row 11; the sandbox prefix is the user's choice) |
| FLD-02 | PASS | `Enterprise Projects` |
| FLD-03 | PASS | `Customer Portal`, the user's explicit choice (follow-up A), recorded as a deviation from the CLAUDE.md hint. Unchanged since Round 1 |
| ERR-01 | PASS | shape2 TC-A, shape5 TC-T and shape14 TC-F are `shapetype="catcherrors"` |
| ERR-02 | PASS | Exactly 3 (retry 0 / 2 / 0). No fourth |
| DEP-01 | PASS | `workload="bridge"`, `allowSimultaneous="true"`. Executions report `exec_listener_bridge` (build log Attempt 8) |
| DEP-02 | N/A | No queue listener |
| SHP-01 | PASS | 0 `shapetype="notify"` in C1 v4. `test/test-report.md` is still the empty template (no temporary Notify) |
| SCR-01 | PASS | S1 (shape3) only classifies the body. S2 (shape29) only builds the 500 body |
| SCR-02 | PASS | S1 is about 25 lines and S2 about 16 lines, each with one loop and no nesting |
| TRK-01 | PASS | Row 9: `email` (user Q7), with the slots named |
| TRK-02 | PASS | C3 v1 and C7 v3: `primarykey`=`Email`, `primaryvalue`=27f55bec element 6 `email` |
| CNF-01 | PASS | shape18 and shape24 `processId="338df4f8-af86-44f9-855c-943d8d0d478f"`. C9 is v1 in folderId RjoyOTg5MzY4 (`.../01-Facade/02-Process`), checked on the platform |
| CNF-02 | PASS | shape17 -> shape18 and shape23 -> shape24 set `dynamicdocument.DDP_MED_NS_Msg` = `meta.base.catcherrorsmessage`, the first property in each step |
| EXT-01 | PASS | 9 c85b494e fields with xpath, identical to 1b208fa6, and all ids exist in C4. `consumer_group` is uncovered by an approved exception (row 20, user "2. a") |
| EXT-02 | PASS | The only Listen operation is C3 (API contract fields, no platform-generated override exists to copy). C7 is PRODUCE, which is exempt |
| EXT-03 | PASS | No host, URL or credential in C1, C3 or C7. The topic and producer settings are fixed under the CLAUDE.md exception and do not depend on the environment |
| ENV-01 | PASS | Build log Attempts 4 to 8: deployments only to 1-DEV 693e8bc2 (C1 v2 to v4, C2 v2), and "No production environment touched". The test report has no rounds |
| SPC-01 | PASS | C1, C2, C3, C5, C6 and C7 are present. C8 is present and unreferenced, as spec F4 requires. C4 and C9 are reused and not pulled, as the spec says |
| SPC-02 | PASS | Pass-through with no map (rows 1 to 10). H1/H2: shape6 `<dynamicProperties/>`. R1/R2: shape8 `'{"status":"accepted"}'`, shape20 `'{"status":"rejected","message":"'{1}'"}'`, S2 JsonOutput for 500. FI-1 to FI-15 as in mapping.md |
| SPC-03 | PASS | Attempt 8 "Deviations: None". Decisions 1 to 3 have reasons. The spec wording items are raised as F-1R-01 and F-1R-02 (minor, design) |
| R1 | PASS | shape5 `catchAll="true" retryCount="2"`, Try -> shape30 BR-K. The try path holds only shape30, shape6, shape31, shape7, shape8 and shape9. Nothing is wired from shape6 to shape7. C7 `operation_timeout`=`3000` |
| R2 | PASS | shape5 Catch -> shape28 Exception only (`stopsingledoc="true"`, exact message, {1} = Try/Catch message), with no dragpoints. No C8, 202, facade or Return Documents on this path. 0 references to be398af2 |
| R3 | PASS (structure) | shape28 is downstream of shape2's Try (shape2 -> shape5). Runtime unconfirmed (V1, F2) |
| R4 | PASS | shape2 `catchAll="true" retryCount="0"` on Decision True. Catch -> shape22 `numBranches="2"`, dragpoints 1 -> shape23 and 2 -> shape25. Its try path holds only shape5 and its subtree |
| R5 | PASS | shape23 and shape17: FI-1 then FI-2 to FI-8, with no `DDP_MED_NS_Level`. Then shape24 and shape18 call C9 with `wait="true" abort="true"`, `<returnpaths/>`, no shape added around them |
| R6 | PASS (structure) | shape25 (`outstatuscode` 500 + `DDP_ERROR_MESSAGE`) -> shape29 S2 (JsonOutput) -> shape27 "Error". No fixed-text Message "Error". Runtime unconfirmed (V6 for BR-A, F3) |
| R7 | PASS | The only Stop is shape31 on the success branch. Error paths end in Return Documents with 400 or 500 and the error text, or in the Exception that flows to TC-A. Both facade calls have `abort="true"` |
| R8 | PASS | shape1 -> shape3 -> shape4, with no Try/Catch before them. True -> shape2, False -> shape14 (not in TC-A scope). No Try/Catch encloses shape16 BR-F or shape22 BR-A. 3 Try/Catch. shape6 is the only Kafka step, inside TC-T inside TC-A |
| R9 | PASS | shape30 `shapetype="branch" numBranches="2"`, dragpoints 1 and 2 both wired. 1 -> shape6 -> shape31 `<stop continue="true"/>`. 2 -> shape7 -> shape8 -> shape9. It is the first shape after shape5's Try. No Decision, process property or script was added. The build log records V9 (documentation) and D8 (04e4af6d, 202 in 2.31 s). The failure leg is review only (F-1R-02) |

## Round 2

Reviewed 2026-10-12 against spec revision 10 (`design/spec.md`, `design/mapping.md`; third pass). Hash recomputed from the repo root with the pipeline method (`sha256sum interfaces/PUB-GB-CG-043/design/spec.md interfaces/PUB-GB-CG-043/design/mapping.md | sha256sum`): 31bb19b997598766015ae0f3b66bf761a1e6eca0692beb7083e290c30d02c293, which matches `pipeline-state.md`. Also reviewed: the XML in `build/components/`, `build/build-log.md` (last entry Attempt 8; revision 10 has no developer run, D9), `build/fix-response.md`, `test/test-report.md` Round 1 (SHP-01 and ENV-01 only), `.claude/review-checklist.md`, spec review items R1 to R10, and CLAUDE.md.

Platform cross-check, read only. `boomi-version-history.sh`: C1 135044a4 v4, C2 4c878feb v2, C3 0f214069 v1, C5 27f55bec v1, C6 f07edecd v1, C7 583b0437 v3 and C8 be398af2 v2 are the current versions on main. C4 c85b494e is still v9 and C9 338df4f8 is still v1. All seven interface components were pulled with `boomi-component-pull.sh` to a scratch path outside `interfaces/`, and `cmp` shows each is byte-identical to its file in `build/components/`. `boomi-component-search.sh` puts C9 in folderId RjoyOTg5MzY4, and `boomi-folder-list.sh` shows that folder's child as `.../01-Facade/02-Process/UnitTest`, which confirms RjoyOTg5MzY4 is `.../01-Facade/02-Process`. The deployment under review is unchanged: C1 v4, C2 v2, C3 v1, C5 v1, C6 v1, C7 v3, with C8 v2 present and unreferenced (0 occurrences of `be398af2` in C1).

### Earlier findings re-checked

| ID | Severity | Rule / spec line | Component | Evidence | Status |
|----|----------|------------------|-----------|----------|--------|
| F-1R-01 | minor | SPC-03; spec.md: "Failure-path test approach" options A and C, "Error handling" intro, header Status | `design/spec.md` (no component) | Option A now describes the current Kafka failure path ("3 failed C7 attempts ... BR-K branch 2 ("Response 202") does not run ... 500 ... never a 202; no C8 step"). The revision 5 text is marked "*History (revision 5 text, superseded ...; do not use as expectations)*". Option C says "Current behaviour (revisions 7 to 10) ... TC-T retry count **2**", and the old text is marked "*History ... Not current*". The Error handling intro says "The three Branch shapes (BR-F and BR-A ... BR-K from revision 9)". Line 5 explains that approval is recorded only in `pipeline-state.md`. Fix verified. | CLOSED |
| F-1R-02 | minor | SPC-03; CLAUDE.md SHV Energy build rules > Kafka send failures; spec.md: Follow-ups F2 | C1 BR-K `shape30` | F2 now reads "**Also open (revision 10, review F-1R-02): V9: BR-K branch 2 does not run on a failed C7 attempt.** ... The F2 run must show that "Response 202" did not run in any failed attempt and that the caller got the 500, never a 202." Option A and the Test notes "Kafka failure" row repeat the V9 expectation. Fix verified. The runtime proof itself is still open under F2, and the user accepted that (row 16). | CLOSED |

### Findings (Round 2)

| ID | Severity | Rule / spec line | Component | Evidence | Status |
|----|----------|------------------|-----------|----------|--------|
| F-2-01 | minor | SPC-03 (spec conformance); spec.md: D7 "Revision 10" sentence, "Error handling" > Definitions "Functional error" | `design/spec.md` (no component) | Two first-pass and second-pass sentences in current-rule sections contradict the final revision 10. (1) D7: "**Revision 10:** C7 v3 is not changed at all ...; only C3's tracking changes (D9)". This conflicts with D9, R10 and row 9 (C3 v1 unchanged, tracking on both). (2) Definitions: "Whether a missing or empty `email` becomes a functional error is open question 2 (row 32)". Row 32 is closed (option a), and "Open questions" says "None". The precedence notes on lines 9 and 11 ("the second pass wins", "the third pass wins") resolve both, and the build matches the final text (C3 v1 and C7 v3 identical on the platform), so no build change is needed. The risk is that the tester, who is writing cases in parallel, reads either sentence literally. **Design change (wording only):** in D7, drop "only C3's tracking changes (D9)" or replace it with "C3 is not changed either (D9)". In Definitions, replace the open-question clause with "A missing or empty `email` is not a functional error (row 32, option a)". | OPEN |

Open: 0 blocker, 0 major, 1 minor. Disputed: 0.

**Test defect D-1-01.** Closed by the user's decision (spec row 31, user: "email is mandatory. So, keep it on both"), not by a build change. As R10 requires, it is not raised as a finding.

**CLAUDE.md conformance of the accepted behaviour (row 31 and row 32).** No conflict found:

- *Kafka send failures*: an empty, whitespace-only, array or string body fails in the Start shape (C3 `primaryvalue` profile parse), before S1 and before any Kafka step. No send is attempted, so the rule's 3-attempt case does not arise. The caller gets HTTP 500, an error and never a success. The empty body (no error text) is the user's recorded decision (row 31). C1 has no path that returns 202 after a failed send: the only 202 is on BR-K branch 2 (shape30 dragpoint 2 -> shape7 -> shape8 -> shape9), and C7 (shape6) is only on dragpoint 1, inside TC-T inside TC-A.
- *Cache Notification Facade*: on the row 31 path nothing is sent and no Try/Catch message exists, so no call is due. On every designed error path the facade is still called after `DDP_MED_NS_Msg` is set (CNF-01, CNF-02).
- *Error handling*: 3 Try/Catch, unchanged. No Try/Catch can enclose a Start shape, so the row 31 failure cannot be caught without a component change, which the user declined.
- *Tracking fields*: `email` is used in the connectors C3 and C7 (TRK-02).
- *Data validation*: row 32 (no email check) agrees with requirements section 1.2.1. No script changed (S1 and S2 are the same bytes as in C1 v4).

### Checklist results

| Item | Result | Note |
|------|--------|------|
| NAM-01 | PASS | `name="[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]"` (C1 v4, platform byte-identical) |
| NAM-02 | PASS | Publisher: Source application `Customer Portal`, Source BU `GB-CG`, no target segments |
| NAM-03 | PASS | shape1 WSS Listen (C3). Kafka PRODUCE to `gb-cg.q.leads.in.insert` (shape6, C7) |
| NAM-04 | PASS | Equals spec row 10 character for character |
| NAM-05 | PASS | Unchanged in revision 10. Every value comes from the user or CLAUDE.md |
| IID-01 | PASS | `PUB-GB-CG-043` |
| IID-02 | PASS | `PUB` = Publisher |
| IID-03 | PASS | `043` from the user's design document (row 2) |
| BU-01 | PASS | Only `GB-CG` |
| FLD-01 | PASS | `folderFullPath=".../GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead"`, folderId Rjo4ODkxNDA5, equals row 11 (the sandbox prefix is the user's choice) |
| FLD-02 | PASS | `Enterprise Projects` |
| FLD-03 | PASS | `Customer Portal`, the user's explicit choice (follow-up A), recorded as a deviation from the hint. Unchanged |
| ERR-01 | PASS | 3 x `shapetype="catcherrors"` |
| ERR-02 | PASS | Exactly 3 (`retryCount` 0 / 2 / 0, all `catchAll="true"`). Revision 10 adds no shape |
| DEP-01 | PASS | `<process ... allowSimultaneous="true" ... workload="bridge">` |
| DEP-02 | N/A | No queue listener. The start shape is WSS |
| SHP-01 | PASS | 0 `shapetype="notify"` in C1 v4. Test report Round 1 "Temporary Notify shapes": none |
| SCR-01 | PASS | S1 only classifies the body, and S2 only builds the 500 body. Unchanged (row 32: no email check added) |
| SCR-02 | PASS | S1 is about 25 lines and S2 about 16 lines, with no nesting. Unchanged |
| TRK-01 | PASS | Row 9: `email` (user Q7), on C3 and C7 (user: "keep it on both") |
| TRK-02 | PASS | C3 v1 and C7 v3: `TrackedField fieldId="33185" fieldName="primarykey"` with `valueType="static"` `staticproperty="Email"`, and `fieldId="33186" fieldName="primaryvalue"` with `valueType="profile"`, profileId 27f55bec, elementId 6 `email (Root/Object/email)` |
| CNF-01 | PASS | shape18 and shape24: `processcall processId="338df4f8-af86-44f9-855c-943d8d0d478f" wait="true" abort="true"`. C9 v1 is in RjoyOTg5MzY4 `.../01-Facade/02-Process` (platform search, this round) |
| CNF-02 | PASS | shape17 and shape23 set `DDP_MED_NS_Msg` = `meta.base.catcherrorsmessage` first, then FI-2 to FI-8 |
| EXT-01 | PASS | One `ConnectionOverride id="c85b494e-..."` with 9 fields, each with `xpath`. `consumer_group` is uncovered by the approved exception (row 20) |
| EXT-02 | PASS | The only Listen operation is C3 (API contract fields, no platform-generated override to copy). C7 is PRODUCE, which is exempt. 0 `OperationOverride` |
| EXT-03 | PASS | No host, URL or credential in C1, C2, C3 or C7. Topic and producer settings are fixed under the CLAUDE.md exception |
| ENV-01 | PASS | Build log: no deployment since Attempt 8 (1-DEV only). Test report Round 1: 1-DEV (693e8bc2) only, "No production environment was touched" |
| SPC-01 | PASS | C1, C2, C3, C5, C6 and C7 are present. C8 is present and unreferenced (F4). C4 and C9 are reused, not pulled |
| SPC-02 | PASS | Pass-through with no map (rows 1 to 10). H1/H2 none. R1/R2 as in mapping.md. FI-1 to FI-15 as tabled. Mapping row 4 (Required = N, tracked on C3 and C7) matches the XML |
| SPC-03 | PASS | No deviations. The build log has no revision 10 entry, as D9 says. The spec wording item is raised as F-2-01 (minor, design wording) |
| R1 | PASS | shape5 `catchAll="true" retryCount="2"`, Try -> shape30 BR-K. Nothing wired from shape6 to shape7. C7 `operation_timeout` `3000` |
| R2 | PASS | TC-T catch -> shape28 Exception only (`stopsingledoc="true"`, message `Kafka send to gb-cg.q.leads.in.insert failed after 3 attempts: {1}`). 0 references to be398af2 |
| R3 | PASS (structure) | TC-T and its catch path sit on TC-A's try path. Runtime is unconfirmed (V1, F2) |
| R4 | PASS | TC-A `retryCount="0"` on Decision True. Catch -> BR-A `numBranches="2"`, both dragpoints wired |
| R5 | PASS | "Set facade inputs" (FI-1, then FI-2 to FI-8, no FI-9 to FI-15) -> C9 call with `wait="true" abort="true"`, no return paths, no shape around it |
| R6 | PASS (structure) | "Response 500" (500 + `DDP_ERROR_MESSAGE`) -> S2 JsonOutput -> Return Documents "Error". Runtime is unconfirmed (V6 for BR-A, F3) |
| R7 | PASS | Only one Stop (`<stop continue="true"/>`, success branch). Both facade calls `abort="true"`. Row 31 behaviour is the user's accepted exception and is not a finding |
| R8 | PASS | Start -> S1 -> Decision, outside every Try/Catch. True -> TC-A, False -> TC-F. 3 Try/Catch. C7 inside TC-T inside TC-A |
| R9 | PASS | BR-K `numBranches="2"`. 1 -> C7 -> Stop `continue="true"`. 2 -> Response 202 -> Accepted -> Return Documents "Accepted". First shape after TC-T's Try |
| R10 | PASS | C3 v1 and C7 v3 both have `primarykey` static `Email` and `primaryvalue` profile 27f55bec element 6 `email`. No component changed (all seven are byte-identical to the platform's current versions, and those versions equal the round 1 deployment C1 v4, C2 v2, C3 v1, C7 v3). No Try/Catch, script or Notify was added for D-1-01. D-1-01 is not raised. The changed rows 9, 31 and 32 are consistent with the XML and with CLAUDE.md (see above). The one wording inconsistency left is F-2-01 |

## Round 3

Reviewed 2026-10-12 (final round) against spec revision 11 (`design/spec.md`, `design/mapping.md`; wording only). Hash recomputed from the repo root with the pipeline method (`sha256sum interfaces/PUB-GB-CG-043/design/spec.md interfaces/PUB-GB-CG-043/design/mapping.md | sha256sum`): 3984711dde544ab3e30a667b4e165991366697ed64cadef2f51e46c49094d113, which matches `pipeline-state.md`. Also reviewed: the XML in `build/components/`, `build/build-log.md` (last entry still Attempt 8; revision 11 has no developer run, D9), `build/fix-response.md` (unchanged since 2026-10-12 06:50), `test/test-report.md` "## Round 2" (SHP-01, ENV-01 and the D-2-01 evidence), `.claude/review-checklist.md`, spec review items R1 to R10, and CLAUDE.md.

Platform cross-check, read only. `boomi-version-history.sh --current`: C1 135044a4 v4 (2026-10-12T06:46:45Z), C2 4c878feb v2, C3 0f214069 v1, C5 27f55bec v1, C6 f07edecd v1, C7 583b0437 v3 and C8 be398af2 v2, all current on main. C4 c85b494e is still v9 and C9 338df4f8 is still v1. All seven interface components were pulled with `boomi-component-pull.sh` to a scratch path outside `interfaces/`, and `cmp` shows each is byte-identical to its file in `build/components/`. `boomi-component-search.sh` puts C9 (v1, current) in folderId RjoyOTg5MzY4 `02-Process`, the same folder as in Rounds 1 and 2. C8 is still unreferenced (0 occurrences of `be398af2` in C1). Tool note: `boomi-env-check.sh` printed only its header and exited 1 in this session. That is a local script issue and not an auth error, because every read-only platform call afterwards succeeded. No platform state was changed.

### Earlier findings re-checked

| ID | Severity | Rule / spec line | Component | Evidence | Status |
|----|----------|------------------|-----------|----------|--------|
| F-2-01 | minor | SPC-03 (spec conformance); spec.md: D7, "Error handling" > Definitions "Functional error" | `design/spec.md` (no component) | (1) D7 now reads "**Revision 10:** C7 v3 is not changed at all, including its tracked fields ...; C3 is not changed either (D9). (Revision 11, review F-2-01: the earlier words "only C3's tracking changes" were first-pass text and are withdrawn.)", which agrees with D9, R10 and row 9. (2) Definitions "Functional error" now ends "A missing or empty `email` is not a functional error (row 32, option a)", which agrees with row 32 and "Open questions: None". "open question 2" now appears only in the revision 10 second-pass history (line 46, marked "Closed in the third pass"). Both match the build (C3 v1 and C7 v3, byte-identical to the platform). Fix verified. | CLOSED |

### Findings (Round 3)

None.

Open: 0 blocker, 0 major, 0 minor. Disputed: 0.

**Revision 11 wording compared with the build and the Round 2 test evidence.** The wording is consistent, and no finding is raised:

- **Row 31 body (D-2-01):** rows 31 and 459 ("HTTP response per outcome"), "Error reaches the caller" (line 378), process design step 1, the "Every error reaches the caller" requirement, the Definitions "Functional error" and "Unhandled by design" entries, D9, R10, the test notes "Bodies that fail at the Start shape" and "Every error returns to the caller", and `mapping.md` (revision 11 note, the revision 10 note marker and the request target note) all say "the runtime's default HTML error page (`text/html`) with the internal error reason". This matches test report Round 2: TC-08 bfbe81c5 shows `<title>Error 500 Failed tracking custom fields; Caused by: ... the document may not be well-formed json</title>`, `HTTP ERROR 500`, and "Problem accessing /ws/rest/gb-cg-leads/v1/leads. Reason:". The TC-09, TC-11 and TC-12 bodies end in `</html>`. Every other row 31 claim matches Round 2: 500, execution ERROR, S1 with 0 documents out, no facade, no TC-F/BR-F/TC-A/BR-A, no C7, never a 202. The spec says that only the TC-08 body was captured in full (line 11) and quotes the array and string texts "for example" from the process log. The test note asks for the full body to be captured at least once, which bfbe81c5 meets. That is accurate.
- **Every "empty body" left in the spec is history text with a revision 11 marker or a withdrawal note:** lines 37, 40 and 52 (revision 10 first and second pass), line 681 above the question 1 text, and line 694. Lines 11, 13 and 17 describe the change itself. No current-rule section still says "empty body".
- **Row 28 (facade failure):** the new text cites 22c61363 (revision 6 build) and says that the content on C1 v4 is "not verified". Lines 383 and 461 say the same. This is consistent with build log Attempt 4 and with Round 2 (the facade did not fail; TC-14 not run). C1 v4 still has `wait="true" abort="true"` on both facade Process Calls.
- **No component change:** D9 and the "Changes in revision 11" list state that no developer run, push or deploy is needed. The build log has no revision 11 entry, and every component is byte-identical to the platform's current version. Both agree.
- **Observations, not findings:** (a) Line 5 still says "revision 11 is not yet approved". That describes the spec file's own status line only, which is the pattern accepted under F-1R-01. Approval is recorded in `pipeline-state.md`. (b) R7 (line 635) names the facade failure as "the one accepted exception". R7 covers catch paths. The row 31 Start-shape failure is not on a catch path and is covered by R10, so there is no contradiction. (c) The exposure of internal error text and the test report's note that the row 31 decision was made on the "empty body" description are both part of the user's row 31 decision. As R10 and the orchestrator instruct, they are not raised here.

### Checklist results

| Item | Result | Note |
|------|--------|------|
| NAM-01 | PASS | `name="[Publisher]-[PUB-GB-CG-043]-[Lead]-[Customer Portal]-[GB-CG]"` (C1 v4, byte-identical to the platform) |
| NAM-02 | PASS | Publisher: Source application `Customer Portal`, Source BU `GB-CG`, no target segments |
| NAM-03 | PASS | shape1 WSS Listen (C3). Kafka PRODUCE to `gb-cg.q.leads.in.insert` (C7 `objectTypeName`) |
| NAM-04 | PASS | Equals spec row 10 character for character |
| NAM-05 | PASS | Revision 11 changes no naming value. All values come from the user or CLAUDE.md |
| IID-01 | PASS | `PUB-GB-CG-043` |
| IID-02 | PASS | `PUB` = Publisher |
| IID-03 | PASS | `043` from the user's design document (row 2) |
| BU-01 | PASS | Only `GB-CG` |
| FLD-01 | PASS | All 7 files: `folderFullPath=".../GB-CG/Enterprise Projects/Customer Portal/Publisher/PUB-GB-CG-043-Lead"` (row 11; the sandbox prefix is the user's choice) |
| FLD-02 | PASS | `Enterprise Projects` |
| FLD-03 | PASS | `Customer Portal`, the user's explicit choice (follow-up A). Unchanged |
| ERR-01 | PASS | 3 x `shapetype="catcherrors"` |
| ERR-02 | PASS | Exactly 3 (`catchAll="true"`, `retryCount` 0 / 2 / 0). No fourth |
| DEP-01 | PASS | `<process ... allowSimultaneous="true" ... workload="bridge">`. Round 2 runs report `exec_listener_bridge` |
| DEP-02 | N/A | No queue listener. The start shape is WSS |
| SHP-01 | PASS | 0 `shapetype="notify"` in C1 v4 (final pull this round). Test report Round 2 "Temporary Notify shapes": none |
| SCR-01 | PASS | S1 only classifies the body, and S2 only builds the 500 body. C1 is unchanged |
| SCR-02 | PASS | S1 is about 25 lines and S2 about 16 lines, with no nesting. Unchanged |
| TRK-01 | PASS | Row 9: `email` (user Q7), on C3 and C7 (user: "keep it on both") |
| TRK-02 | PASS | C3 v1 and C7 v3: `TrackedField fieldId="33185" fieldName="primarykey"` `staticproperty="Email"`, and `fieldId="33186" fieldName="primaryvalue"` `elementName="email (Root/Object/email)"` (C5) |
| CNF-01 | PASS | Two `processcall processId="338df4f8-af86-44f9-855c-943d8d0d478f" wait="true" abort="true"`. C9 v1 is current in folderId RjoyOTg5MzY4 `.../01-Facade/02-Process` (platform search, this round) |
| CNF-02 | PASS | Both "Set facade inputs" shapes set `DDP_MED_NS_Msg` = `meta.base.catcherrorsmessage` first. Unchanged |
| EXT-01 | PASS | One `ConnectionOverride id="c85b494e-..."` with 9 `xpath` fields. `consumer_group` is uncovered by the approved exception (row 20) |
| EXT-02 | PASS | The only Listen operation is C3 (API contract fields; no platform-generated override to copy). C7 is PRODUCE, which is exempt. 0 `OperationOverride` |
| EXT-03 | PASS | No host, URL or credential in C1, C2, C3 or C7. The topic and producer settings (`acks` all, `operation_timeout` 3000, `client_id` gb-cg.leads, `compression_type` snappy) are fixed under the CLAUDE.md exception |
| ENV-01 | PASS | Build log: no deployment since Attempt 8 (1-DEV 693e8bc2 only). Test report Round 2: 1-DEV only, "No production environment was touched", no redeploy |
| SPC-01 | PASS | C1, C2, C3, C5, C6 and C7 are present. C8 is present and unreferenced (F4). C4 and C9 are reused, not pulled |
| SPC-02 | PASS | Pass-through with no map. Revision 11 changes no mapping rule (`mapping.md` revision 11 note: "No field rule, row value or component changes"). R1/R2, H1/H2 and FI-1 to FI-15 as in Round 2 |
| SPC-03 | PASS | No deviations ("Deviations from spec: None"). Revision 11 needs no build entry (D9). F-2-01 is closed |
| R1 | PASS | TC-T `catchAll="true" retryCount="2"`. C7 `operation_timeout` `3000`. Unchanged |
| R2 | PASS | TC-T catch -> Exception "Kafka send failed" only. 0 references to be398af2 |
| R3 | PASS (structure) | TC-T sits on TC-A's try path. Runtime is unconfirmed (V1, F2; review only, row 16) |
| R4 | PASS | TC-A `retryCount="0"` on Decision True. Catch -> BR-A with both dragpoints wired |
| R5 | PASS | FI-1, then FI-2 to FI-8 -> C9 call (`wait="true" abort="true"`), with no shape around it |
| R6 | PASS (structure) | "Response 500" -> S2 -> Return Documents "Error". Runtime is unconfirmed (V6, F3) |
| R7 | PASS | No 202 after a failed send. Both facade calls have `abort="true"`. Row 31 is the user's decision and is not raised (see the observation above) |
| R8 | PASS | Start -> S1 -> Decision, outside every Try/Catch. 3 Try/Catch. C7 inside TC-T inside TC-A |
| R9 | PASS | BR-K branch 1 -> C7 -> Stop `continue="true"`. Branch 2 -> Response 202 -> Accepted -> Return Documents "Accepted". The failure leg is review only (F2) |
| R10 | PASS | C3 v1 and C7 v3 tracking as above. No component changed: all seven are byte-identical to the platform's current versions, which equal the deployment under test (C1 v4, C2 v2, C3 v1, C7 v3). No Try/Catch, script or Notify was added. The revision 11 body wording matches the Round 2 evidence. D-1-01 and the row 31 behaviour are not raised |
