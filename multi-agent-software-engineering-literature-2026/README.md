# Multi-agent software engineering literature review (2026)

## Research cutoff

This evidence-led review was searched and validated through **23 August 2026 (Europe/Paris)**. The requested cutoff was **31 August 2026**, which was still eight days in the future when the research ran. The review therefore does not claim coverage of sources published from 24–31 August 2026; a follow-up search after 31 August is required for a literal end-of-month cutoff.

## Executive recommendation

Use multiple coding agents only when the task exposes at least two **independently executable and independently verifiable** work queues, with stable contracts, isolated write surfaces, an accountable integrator, and enough review/testing capacity to absorb the outputs. Agent count should follow the ready dependency graph—not project size or the desire for more parallelism.

The default is one strong, well-tooled agent:

- **Small fixes and features:** one agent; optionally add a read-only diagnostician, test author, or risk reviewer. Avoid multiple overlapping writers.
- **Medium features:** begin with one; use two or three total only behind frozen API/UI or module boundaries and executable acceptance tests.
- **Large or cross-cutting features:** begin with one accountable lead plus two or three contract-bounded workers/verifiers in isolated branches or worktrees. Plan dependencies before fan-out and integrate centrally.
- **Greenfield products:** retain human product and architecture ownership. After specifications, contracts, and a vertical acceptance harness exist, use a small lead-and-workers topology; scale only from measured queue, integration, cost, and quality data.

Across all scopes, prefer executable evidence—tests, compilers, static/security analysis, traces, and clean integration runs—over agent consensus. Stop parallelism when interface churn, overlapping edits, repeated clarification, merge/review queues, regressions, or marginal cost dominate. Current Codex and Claude Code documentation establishes useful multi-agent controls, but not a universal productivity advantage; evaluate proposed topologies against a matched single-agent baseline on representative private tasks.

The full recommendation, scope matrix, Codex and Claude Code operating models, evidence grading, contradictions, limitations, and research gaps are in the [synthesis and decision framework](08-synthesis-decision-framework.md).

## Deliverables

1. [Research plan and protocol](00-research-plan.md)
2. [Foundations and theory](01-foundations-and-theory.md)
3. [Empirical software-engineering evidence](02-empirical-software-engineering.md)
4. [Small and medium feature practice](03-small-medium-features.md)
5. [Large features and greenfield products](04-large-features-greenfield-products.md)
6. [Tooling and platform landscape](05-tooling-and-platform-landscape.md)
7. [Critical review and red-team limitations](06-red-team-limitations.md)
8. [Normalized evidence register](07-evidence-register.md)
9. [Synthesis and decision framework](08-synthesis-decision-framework.md)

## Evidence base

Six independent research agents produced 95 annotated bibliography entries. The coordinator deduplicated them into **76 normalized source entries** with authorship, date, absolute URL, source type, evidence quality, and supported scopes. Primary sources were required for material claims; preprints, inaccessible or unverified material, vendor sponsorship, and indirect evidence are explicitly flagged in the individual memos. Official documentation is treated as strong evidence for product capability but weak evidence for comparative effectiveness.

## How to use this review

Start with the [decision matrix](08-synthesis-decision-framework.md#literature-backed-decision-matrix), then consult the relevant scope memo for claim-level findings and the [evidence register](07-evidence-register.md) for normalized source traceability. The [red-team memo](06-red-team-limitations.md) should be read before granting multiple agents broader permissions or adopting an autonomous workflow.
