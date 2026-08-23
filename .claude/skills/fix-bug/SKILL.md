---
name: fix-bug
description: Reproduce, diagnose, minimally fix, and regression-test a defect. Use when the user asks to fix a bug and root-cause evidence or a fail-before oracle is needed.
---

# Fix bug

Use a staged diagnose–fix–verify loop. Do not assign competing writers to the same fault.

## Required inputs

Collect observed and expected behavior, environment and version, reproduction information, safe diagnostic commands, relevant logs, recent changes, risk class, and allowed files.

## Roles and order

1. `bug-diagnostician` reproduces, minimizes, localizes, and falsifies alternative causes without editing.
2. The coordinator validates the diagnosis and assigns the smallest fix surface to one `implementation-engineer`.
3. `test-engineer` adds or validates a fail-before/pass-after regression oracle when useful and independently checkable.
4. `code-reviewer` checks the patch; add `security-specialist` only for a security-sensitive surface.

## Gates

- Do not edit before a reliable reproduction or sufficiently strong causal evidence exists.
- Preserve unrelated behavior and user changes.
- Run the regression test, affected-package checks, and relevant static checks.
- Report pre-existing or environment failures separately from patch regressions.

## Output

Return the common handoff plus reproduction, root cause, falsified hypotheses, minimal fix, regression oracle, exact checks, and any uncertainty about adjacent impact.

## Stop conditions

Stop when reproduction is unavailable, diagnosis remains ambiguous, fixes require unresolved architecture or product decisions, the environment is unstable, or safe diagnosis requires broader access.

