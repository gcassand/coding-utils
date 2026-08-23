---
name: implement-feature
description: Implement an approved feature through bounded writers and executable gates. Use when requirements, contracts, write ownership, and acceptance commands are already stable.
---

# Implement feature

The main session coordinates and integrates. Start with one writer; agent count follows the ready dependency graph rather than feature size.

## Required inputs

Require the approved specification, base commit, frozen contracts, dependency graph, task packets, allowed write surfaces, setup command, acceptance oracles, risk class, and integration owner.

## Roles and order

1. Assign one ready packet to `implementation-engineer`.
2. Use `test-engineer` for an independent behavior oracle or a disjoint test slice when this adds real verification.
3. Add another writer only when its task is ready, its files and contracts do not overlap, and it runs in a separate worktree.
4. Run `code-reviewer`, and `security-specialist` only when the risk surface warrants it, before central integration.

## Gates

- Record base commit and worktree for every writer.
- Validate each handoff before downstream use.
- Run targeted checks per slice, then combined build, regression, contract, and acceptance checks in the integration worktree.
- Keep commits small and reversible. Do not deploy or merge externally without explicit authorization.

## Output

Return the common handoff plus integrated diff or commits, task-to-change traceability, commands and results, review findings and resolutions, compatibility and rollback notes, and remaining release gates.

## Stop conditions

Stop fan-out on contract churn, overlapping edits, repeated clarification, unlocalized failures, exhausted review capacity, or an empty ready queue. Consolidate the disputed dependency chain under one writer.

