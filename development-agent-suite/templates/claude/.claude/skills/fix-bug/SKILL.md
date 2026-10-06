---
name: fix-bug
description: Reproduce, diagnose, minimally fix, and regression-test a defect. Use when the user asks to fix a bug and root-cause evidence or a fail-before oracle is needed.
---

# Fix bug

Use a staged diagnose–fix–verify loop. Do not assign competing writers to the same fault.

Scale inputs and reporting to the decision and risk. Named roles describe responsibilities; they are optional delegation choices unless the user requests an independent specialist. Continue authorized work through verification and correction; pause only for material missing decisions or permission boundaries.

## Required inputs

Establish observed and expected behavior, a reproduction or causal evidence, relevant environment constraints, and the allowed fix surface. Inspect logs, versions, recent changes, and risk details only as needed to distinguish causes. Ask only for missing information that materially blocks diagnosis or safe execution.

## Roles and order

1. For a localized defect with a clear owning path, the main session reproduces, diagnoses, implements the smallest fix, and verifies it directly.
2. Use a read-only `bug-diagnostician` when the cause is uncertain or alternative hypotheses need independent investigation. Validate its causal evidence before editing.
3. Delegate to one `implementation-engineer` only when a bounded fix packet makes a handoff useful. Use `test-engineer` for a missing independent regression oracle, not as a mandatory stage.
4. Use `code-reviewer` for material regression risk or requested independent review; add `security-specialist` for a security-sensitive surface.

## Gates

- Run checks that establish the changed behavior and cover affected risks. Broaden or repeat them only for new edits, failures, unresolved concerns, or repository-required gates.
- Do not edit before a reliable reproduction or sufficiently strong causal evidence exists.
- Preserve unrelated behavior and user changes.
- Run the regression test, affected-package checks, and relevant static checks.
- Report pre-existing or environment failures separately from patch regressions.

## Output

Return the common handoff plus reproduction, root cause, falsified hypotheses, minimal fix, regression oracle, exact checks, and any uncertainty about adjacent impact.

## Stop conditions

Stop when reproduction is unavailable, diagnosis remains ambiguous, fixes require unresolved architecture or product decisions, the environment is unstable, or safe diagnosis requires broader access.
