---
name: plan-feature
description: Produce a decision-complete technical and delivery plan for an approved feature. Use before cross-module, migration, or parallel implementation when contracts and dependency order matter.
---

# Plan feature

Keep the main session as decision recorder and integration owner. Planning must remove hidden product and architecture decisions from worker task packets.

Scale inputs and reporting to the decision and risk. Named roles describe responsibilities; they are optional delegation choices unless the user requests an independent specialist. Continue authorized work through verification and correction; pause only for material missing decisions or permission boundaries.

## Required inputs

Establish the approved outcome, non-goals, acceptance criteria, repository baseline, and affected consumers. Inspect risk constraints and compatibility details where the proposed change needs them. For a localized change, a short plan and targeted oracle suffice; require complete task packets only before delegating. Resolve material product decisions before implementation; record reversible defaults without pausing for routine choices.

## Roles and order

1. For a bounded change with understood contracts, the main session inspects the affected path and records a concise plan directly.
2. Use `codebase-explorer` for an unfamiliar area, `software-architect` for consequential cross-module, compatibility, or migration decisions, and `delivery-planner` when there are multiple independently executable packets.
3. Resolve shared decisions before downstream delegation. Architecture alternatives may be explored independently, but one selected contract and acceptance oracle must precede implementation fan-out.

## Gates

- Every delegated task has inputs, outputs, base commit, allowed write set, dependency list, acceptance command, and stop condition.
- Shared contracts and central files have one owner.
- Writers are not created for blocked nodes.
- A runnable baseline and credible oracle exist before implementation.

## Output

Return the common handoff plus selected architecture and alternatives, ADR decisions, contracts, dependency graph, ordered task packets, ownership map, integration order, test gates, migration and rollback plan, and unresolved human approvals.

## Stop conditions

Stop when product scope, architecture, compatibility, data recovery, or permissions remain materially unresolved. Collapse the plan to one writer when the work is a single dependency chain or converges on one shared subsystem.
