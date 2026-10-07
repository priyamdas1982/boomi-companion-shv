---
name: build-interface
description: Run the SHV Boomi role pipeline (designer, developer, reviewer, tester) for one interface ID, with user approval of the spec and at most three review/fix/test rounds.
argument-hint: <interface-id e.g. MA-IT-LG-001>
arguments: [interface-id]
disable-model-invocation: true
---

# /build-interface $0

You are the **orchestrator** for interface `$0`. You run in the main conversation and delegate
each role to its subagent with the Agent tool (`subagent_type`: `designer`, `developer`,
`reviewer` or `tester`).

You do not design, build, review or test yourself. You are the only one who talks to the user,
and the only writer of `interfaces/$0/pipeline-state.md`. CLAUDE.md, including its "Role pipeline"
section, applies throughout.

Every prompt you send to a subagent starts with: the interface ID `$0`, the folder `interfaces/$0/`,
the current round number, and exactly what you want back. Subagents cannot ask the user; you can.

## 0. Set up

1. Check that `$0` matches `^(PUB|SUB|MA|SC|LI)-<BU-SHORT>-[0-9]+$`, where `<BU-SHORT>` is one of the
   codes in CLAUDE.md "BU-SHORT codes". If no ID was given, or it doesn't match, ask the user for the
   ID and explain the format with the examples from CLAUDE.md. Never construct the sequence number yourself.
2. If `interfaces/$0/` does not exist, copy `interfaces/_template/` to it. If it exists, read
   `pipeline-state.md` and resume from the recorded step. Tell the user which step you are resuming from.
3. Record in `pipeline-state.md`: step, round = 0, spec approved = no.
4. Ask the user for the requirements, unless they already gave them. Pass the user's words through unchanged.

## 1. Design, then STOP for approval

1. Run **designer** with the requirements and all of the user's answers so far.
2. If the spec status is `DRAFT - OPEN QUESTIONS`, put the open questions to the user exactly as
   numbered by the designer, wait for the answers, and run **designer** again with them.
   Repeat until the status is `READY FOR APPROVAL`.
3. Show the user:
   - the Required values table from `design/spec.md`, including the full process name and folder path,
   - a short outline of the design and the tracking field,
   - the paths to `design/spec.md` and `design/mapping.md`.
4. **STOP.** Ask the user to approve the spec, or request changes. Do not continue until they explicitly approve.
   On a change request, go back to step 1.1.
5. On approval, compute
   `sha256sum interfaces/$0/design/spec.md interfaces/$0/design/mapping.md | sha256sum`
   and record in `pipeline-state.md`: `Spec approved: yes`, the approval date, and `Spec hash: <hash>`.

Under the "Role pipeline" section of CLAUDE.md, this approval is the user's answer and confirmation for
naming, folder path, sequence number and tracking field. You do not ask for them again in later steps.

## 2. Build

Run **developer** in build mode.

If it returns `BLOCKED`, handle it under "Missing values" below. Otherwise record the component IDs
in `pipeline-state.md` and set round = 1.

## Rounds: steps 3 to 5, at most three rounds

### 3. Review and test design, in parallel

In **one message**, launch both agents so they run in parallel:

- **reviewer** for round N.
- **tester** in `write-cases` mode. Do this in round 1, and in later rounds only if the spec has changed.
  Otherwise launch only the reviewer.

### Disputes

If any finding has status `DISPUTED`, or the developer's fix response disputes any finding, **stop the loop**.
Show the user each disputed finding: ID, rule, evidence, the developer's reason and the reviewer's response.
Ask them to rule on each one. Record the rulings in `pipeline-state.md`. Continue only on their instruction:
"fix" means the developer must fix it; "accept" means the finding is closed by the user's decision.

### 4. Fix

If there are open **blocker** or **major** findings, or test defects from the previous round's step 5,
run **developer** in fix mode with the list of finding and defect IDs. Then check its fix response for
`DISPUTED` answers (see Disputes above). Minor findings are not sent for fixing; they stay open for the summary.

If there is nothing to fix, skip to step 5.

### 5. Execute tests

Run **tester** in `execute` mode for round N.

### Loop control

- **Done** when the latest review has no open blockers or majors, every test case passed, no finding is
  disputed, and the tester reports no temporary Notify shapes left in place. Go to Finish.
- Otherwise, if N < 3, set N = N + 1 and go back to step 3. The reviewer re-checks the fixes and
  the developer then fixes any new findings and test defects.
- If round 3 ends without being Done, **stop and escalate** to the user. List what is still open,
  and do not start a fourth round unless the user explicitly tells you to.

Update `pipeline-state.md` after every step: step, round, open counts, disputed IDs, last test result.

## Missing values

When any role returns `BLOCKED: missing value` or reports an `OPEN` item:

1. Ask the user a direct question for each specific missing value, with hints from CLAUDE.md. Do not investigate the platform to avoid asking.
2. Run **designer** to add the answer to the spec.
3. The spec has changed, so return to step 1.3 for re-approval and a new hash before any further building.

`BLOCKED: environment` means the test environment could not be confirmed. Stop and ask the user;
never point a role at production.

## Finish

1. **Final Notify check.** Pull each process in the spec with the read-only `boomi-component-pull.sh`
   and confirm that no XML contains `shapetype="notify"`. If any does, the pipeline is not done:
   send it to the developer to remove it as a blocker, and report it.
2. Summarise for the user:
   - **Process names**, exactly as built.
   - **Folder path.**
   - **Rounds used**, out of 3.
   - **Open findings**: ID, severity, rule, one line each, including minors and any the user accepted.
   - **Test results**: passed and failed counts per round, execution IDs from the last round,
     open defects, and the environment used.
   - **Temporary Notify shapes**: confirmation that none remain.
   - **Files**: `interfaces/$0/design/`, `build/`, `review/findings.md`, `test/test-report.md`.
3. Remind the user that promotion to production goes through SHV's normal release process, not this pipeline.
