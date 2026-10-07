# Interfaces

Each SHV Boomi interface built through the role pipeline (`/build-interface <ID>`) gets
its own folder here, named after its Integration ID (for example `MA-IT-LG-001`).
`_template/` holds empty versions of every file. The orchestrator copies it when it starts a new interface.

## Layout

```
interfaces/<ID>/
├── pipeline-state.md        # orchestrator only: step, round, spec approval and hash, rulings
├── design/                  # designer only
│   ├── spec.md              # required values, process design, open questions
│   └── mapping.md           # field mapping, one row per target field
├── build/                   # developer only
│   ├── components/          # pulled XML: components/<component-type>/<name>.xml
│   ├── build-log.md         # components, decisions, deviations, deployments, temporary Notify
│   └── fix-response.md      # per round: each finding FIXED or DISPUTED, with a reason
├── review/                  # reviewer only
│   └── findings.md          # per round: findings table and checklist results
└── test/                    # tester only
    ├── test-cases.md        # derived from design/ only
    ├── payloads/            # input payload per test case (no credentials)
    └── test-report.md       # per round: results, execution IDs, defects, temporary Notify
```

Each role writes only to its own folder. Hooks in `.claude/agents/*.md` enforce this.
`_template/` is read-only for all roles.

## Spec approval

The designer sets `Status: READY FOR APPROVAL` only when no required value is `OPEN`.
Approval comes from the user and is recorded by the orchestrator in `pipeline-state.md`,
together with a hash of `spec.md` and `mapping.md`. The developer refuses to build if the
spec is unapproved or its hash has changed.

## Findings format (`review/findings.md`)

The reviewer appends one `## Round N` section per review. Each finding is one row:

| Column | Content |
|--------|---------|
| ID | `F-<round>-<nn>`. The ID is kept when the finding is re-checked in later rounds. |
| Severity | `blocker`, `major` or `minor`. The default comes from `.claude/review-checklist.md`. |
| Rule / spec line | Checklist ID and CLAUDE.md section (e.g. `DEP-01 / SHV Energy build rules > Deployment mode`), or `spec.md: <section>` |
| Component | Component name, and the file under `build/components/` |
| Evidence | XML element or attribute with the shape name, or quoted spec text |
| Status | `OPEN`, `CLOSED` (fix verified) or `DISPUTED` (sent to the user) |

Each round ends with `Open: <n> blocker, <n> major, <n> minor. Disputed: <n>.` followed by
a "Checklist results" table (item, PASS/FAIL/N/A, note).

Example row:

| ID | Severity | Rule / spec line | Component | Evidence | Status |
|----|----------|------------------|-----------|----------|--------|
| F-1-02 | blocker | DEP-01 / SHV Energy build rules > Deployment mode | [Mediation API]-[MA-IT-LG-001]-... (`build/components/process/...xml`) | `<process ... workload="general">`; the start shape is a Web Services Server | OPEN |

The developer answers each blocker, major and test defect in `build/fix-response.md` as
`FIXED` (component, new version, change) or `DISPUTED` (reason and evidence).
Any dispute stops the pipeline and goes to the user.

## Test report format (`test/test-report.md`)

The tester appends one `## Round N` section per execution, containing:

- **Environment** (name and classification; never production) and the **Deployment ID**.
- **Results table**: case, payload file, execution ID, expected, actual, `PASS`/`FAIL`, defect ID.
- `Passed: <n> / <total>`.
- **Defects**: `D-<round>-<nn>`, case, observed, expected, severity.
- **Temporary Notify shapes**: process, shape, reason, added, removed. CLAUDE.md bans Notify
  shapes. One may be added only when a test cannot be verified any other way, and it must be
  removed (pushed and redeployed) before the tester hands back.

## Round limit

Review, fix and test run for at most three rounds. After that, or on any disputed finding,
the orchestrator stops and escalates to the user.
