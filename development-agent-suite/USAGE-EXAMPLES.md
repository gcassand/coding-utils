# Using the agents: practical examples

Use one capable agent for small or tightly coupled work. Delegate only when each task has a stable boundary, separate write ownership, and an independent acceptance check.

## Direct specialists

```text
Use the product-owner to turn this request into a one-page PRD.
State outcomes, non-goals, measurable acceptance criteria, assumptions, and open decisions.
Do not propose implementation.
```

```text
Use the codebase-explorer to map the request-validation path for POST /orders.
Do not edit files. Cite exact files and symbols, identify tests and conventions,
then return the common handoff.
```

```text
Use the bug-diagnostician to reproduce “CSV import drops the last row”.
Do not edit files. Give a minimal reproduction, the failing command or trace,
the evidence-backed root cause, and the smallest likely fix surface.
```

## Workflows

Codex accepts the skill name with `$`; Claude Code exposes the same name as a slash command.

```text
$discover-product help define the onboarding problem for first-time team admins.
Separate supplied evidence, assumptions, unknowns, and research needed before design.
```

```text
/fix-bug investigate and fix issue 123: token refresh fails after a browser sleep.
Start with a reproduction and diagnosis. Keep the fix local, add a regression test,
and stop if the contract needs to change.
```

```text
$review-change review the current diff for correctness, regressions, security risks,
and missing tests. Do not edit. Rank findings by impact and cite exact evidence.
```

## Writer task packet

Give a writer a bounded contract before it can edit:

```text
Use implementation-engineer.

Objective: add an optional `timezone` field to the account profile response.
Base commit: abc1234.
Allowed files: api/profile.py, api/profile_test.py.
Contract: omit the field when no timezone is stored; preserve all existing fields.
Non-goals: schema migration, frontend work, dependency upgrades.
Acceptance: pytest api/profile_test.py; existing profile contract test.
Stop: any API-versioning decision, migration, or edit outside the allowed files.
Return the standard handoff with exact commands and results.
```

For parallel writers, freeze the contract first, assign disjoint files, name an integrator, and ensure each slice has its own executable oracle. Otherwise use one writer.

## Expected handoff

Every specialist returns:

```text
Objective and completed scope:
Evidence: exact files, symbols, traces, or user-provided facts.
Artifacts or changes:
Checks run: exact commands and outcomes.
Contract or assumption changes:
Unresolved risks:
Recommended next action:
```

A confident answer or agreement between agents is not verification. Prefer executable tests, type checks, traces, screenshots, and reproducible commands.
