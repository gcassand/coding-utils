---
name: review-change
description: Review a branch or diff through independent correctness, test, and risk evidence. Use after implementation or when the user explicitly requests a code review.
---

# Review change

Keep all reviewers read-only and preserve independent first-pass judgment. Agent agreement is not a correctness oracle.

Scale inputs and reporting to the decision and risk. Named roles describe responsibilities; they are optional delegation choices unless the user requests an independent specialist. Continue authorized work through verification and correction; pause only for material missing decisions or permission boundaries.

## Required inputs

Require the base and target diff, intended behavior, contracts, acceptance criteria, known test results, risk class, and repository conventions.

## Roles and order

1. The main session can review a small, understood diff directly. Use `codebase-explorer` for unfamiliar affected paths only when needed.
2. Use `code-reviewer` when an independent pass is requested or the change has material correctness, compatibility, or regression risk.
3. Ask `test-engineer` to evaluate oracle adequacy when the test evidence is uncertain; keep it read-only unless a separate test-writing cycle is authorized.
4. Add `security-specialist` only for explicit security review or security-sensitive code.

Independent review lanes may run in parallel when each adds distinct evidence. Do not share the author's rationale before a reviewer records its first-pass findings unless it is required context.

## Gates

- Every finding has severity, exact location, trigger, impact, and actionable remediation.
- Omit style-only comments without material consequence.
- Validate claims with code paths, tests, static analysis, or reproducible commands.
- Do not edit, merge, post comments, or update external review systems.

## Output

Return findings first in severity order, then open questions, test gaps, and a concise verdict. If there are no findings, state the reviewed surface and remaining verification limits.

## Stop conditions

Stop when the base, requirements, or generated-source provenance is unavailable; request the missing artifact instead of manufacturing findings.
