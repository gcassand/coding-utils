---
name: implement-feature
description: Implement an approved feature through bounded writers and executable gates. Use when requirements, contracts, write ownership, and acceptance commands are already stable.
---

# Implement feature

The main session coordinates and integrates. Start with one writer; agent count follows the ready dependency graph rather than feature size.

Scale inputs and reporting to the decision and risk. Named roles describe responsibilities; they are optional delegation choices unless the user requests an independent specialist. Continue authorized work through verification and correction; pause only for material missing decisions or permission boundaries.

## Required inputs

Establish the approved behavior, affected boundary, allowed write surface, and acceptance command. For a localized change, collect these in the main session without a separate dependency graph or specification document. Before delegation, provide the base commit, stable contracts, ready dependencies, explicit ownership, permissions, and acceptance oracle for each packet. Resolve consequential missing decisions before dependent work.

## Roles and order

1. For a bounded approved change, the main session implements and verifies it directly. When delegation adds value, assign one ready packet to `implementation-engineer`.
2. Use `test-engineer` for an independent behavior oracle or a disjoint test slice when this adds real verification.
3. Add another writer only when its task is ready, its files and contracts do not overlap, and it runs in a separate worktree.
4. Use `code-reviewer` before integration for material regression risk or requested independent review, and `security-specialist` when the trust boundary warrants it. For small changes, the main session reviews its diff and targeted check results.

## Gates

- Run checks that establish the changed behavior and cover affected risks. Broaden or repeat them only for new edits, failures, unresolved concerns, or repository-required gates.
- Record base commit and worktree for every writer.
- Validate each handoff before downstream use.
- Run targeted checks per slice, then combined build, regression, contract, and acceptance checks in the integration worktree.
- Keep commits small and reversible. Do not deploy or merge externally without explicit authorization.

## Output

Return the common handoff plus integrated diff or commits, task-to-change traceability, commands and results, review findings and resolutions, compatibility and rollback notes, and remaining release gates.

## Stop conditions

Stop fan-out on contract churn, overlapping edits, repeated clarification, unlocalized failures, exhausted review capacity, or an empty ready queue. Consolidate the disputed dependency chain under one writer.
