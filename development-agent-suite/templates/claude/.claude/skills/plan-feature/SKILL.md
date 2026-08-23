---
name: plan-feature
description: Produce a decision-complete technical and delivery plan for an approved feature. Use before cross-module, migration, or parallel implementation when contracts and dependency order matter.
---

# Plan feature

Keep the main session as decision recorder and integration owner. Planning must remove hidden product and architecture decisions from worker task packets.

## Required inputs

Require an approved outcome, non-goals, acceptance criteria, repository baseline, risk constraints, and known consumers. If these are unstable, route back to product discovery.

## Roles and order

1. `codebase-explorer` maps current execution paths, conventions, dependencies, tests, and commands.
2. `software-architect` defines boundaries, versioned interfaces, invariants, migration, observability, failure, compatibility, and rollback behavior.
3. After the architecture is selected, `delivery-planner` creates the dependency graph and task packets.

Architecture alternatives may be explored independently, but one approved decision must be recorded before implementation tasks fan out.

## Gates

- Every task has inputs, outputs, base commit, allowed write set, dependency list, acceptance command, and stop condition.
- Shared contracts and central files have one owner.
- Writers are not created for blocked nodes.
- A runnable baseline and credible oracle exist before implementation.

## Output

Return the common handoff plus selected architecture and alternatives, ADR decisions, contracts, dependency graph, ordered task packets, ownership map, integration order, test gates, migration and rollback plan, and unresolved human approvals.

## Stop conditions

Stop when product scope, architecture, compatibility, data recovery, or permissions remain materially unresolved. Collapse the plan to one writer when the work is a single dependency chain or converges on one shared subsystem.
