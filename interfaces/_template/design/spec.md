# Design spec: <ID>

Status: DRAFT - OPEN QUESTIONS

## Requirements

<The user's requirements, as given.>

## Required values

| # | Value | Answer | Source |
|---|-------|--------|--------|
| 1 | Interface type | | OPEN |
| 2 | Integration ID sequence number (YYY) | | OPEN |
| 3 | Integration ID | | OPEN |
| 4 | Main atomic object | | OPEN |
| 5a | Source application | | OPEN |
| 5b | Source BU | | OPEN |
| 6a | Target application | | OPEN |
| 6b | Target BU | | OPEN |
| 7 | Project type | | OPEN |
| 8 | Application name | | OPEN |
| 9 | Tracking field(s) | | OPEN |
| 10 | Full process name | | OPEN |
| 11 | Full folder path | | OPEN |

Source is one of: `user: "<answer>"`, `CLAUDE.md: <section>`, or `OPEN`.
Mark a value "not required for this interface type" when the type does not require it.

## Process design

- Start shape:
- Main steps:
- Target (Kafka topic / ASB / application):
- Deployment mode (workload):

## Error handling

| Try/Catch | Wraps | Catch path |
|-----------|-------|------------|

## Cache Notification Facade

- Where `DDP_MED_NS_Msg` is set to the Try/Catch message:
- Where `[MED] (sub) CACHE Notification Facade` is called:

## Connectors

| Connection / operation | Purpose | Extensible settings | Tracking field |
|------------------------|---------|---------------------|----------------|

## Scripts

| Script | Single purpose |
|--------|----------------|

## Test notes

| Requirement | Observable behaviour to check |
|-------------|-------------------------------|

## Open questions

1.
