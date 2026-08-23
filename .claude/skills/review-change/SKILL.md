---
name: review-change
description: Review a branch or diff through independent correctness, test, and risk evidence. Use after implementation or when the user explicitly requests a code review.
---

# Review change

Keep all reviewers read-only and preserve independent first-pass judgment. Agent agreement is not a correctness oracle.

## Required inputs

Require the base and target diff, intended behavior, contracts, acceptance criteria, known test results, risk class, and repository conventions.

## Roles and order

1. `codebase-explorer` maps unfamiliar affected paths only when needed.
2. Run `code-reviewer` for correctness, regressions, maintainability, and missing tests.
3. Ask `test-engineer` to evaluate oracle adequacy without editing unless a separate test-writing cycle is authorized.
4. Add `security-specialist` only for explicit security review or security-sensitive code.

Independent review lanes may run in parallel. Do not share the author's rationale before a reviewer records its first-pass findings unless it is required context.

## Gates

- Every finding has severity, exact location, trigger, impact, and actionable remediation.
- Omit style-only comments without material consequence.
- Validate claims with code paths, tests, static analysis, or reproducible commands.
- Do not edit, merge, post comments, or update external review systems.

## Output

Return findings first in severity order, then open questions, test gaps, and a concise verdict. If there are no findings, state the reviewed surface and remaining verification limits.

## Stop conditions

Stop when the base, requirements, or generated-source provenance is unavailable; request the missing artifact instead of manufacturing findings.

