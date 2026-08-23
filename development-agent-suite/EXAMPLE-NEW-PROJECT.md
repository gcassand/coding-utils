# Worked example: starting a new project

This example applies the suite to a greenfield product where research, literature, or integration material already exists but no code does. It shows the workflow order, where a human decision is mandatory, and where fan-out is premature.

Greenfield delivery is the least evidenced use of multiple agents. Treat this sequence as a disciplined default to be measured locally, not as a proven optimum. Codex invokes a workflow with `$name`; Claude Code exposes the same name as `/name`.

## When this example applies

- Evidence exists — a literature review, prior art, market or user research, integration constraints — but no running code.
- One human remains accountable for product and architecture decisions.
- If the outcome, non-goals, and acceptance criteria are already written down and stable, skip to [phase 3](#phase-3--define-contracts-for-the-first-slice).

## Why a new project changes the order

The feature workflows begin by mapping an existing system with `codebase-explorer`. A new project has nothing to map and no acceptance oracle to inherit, so two artifacts must be manufactured before any implementation can be verified: a recorded product and architecture decision, and a runnable end-to-end check.

Until both exist, additional agents add cost and agreement rather than correctness. Parallel implementation across modules is the last step in this example, not the first.

## Phase 0 — Prepare the repository and evidence

Research, architecture, and review roles are read-only and work through file reads and search. Evidence pasted into a prompt cannot be cited by path, re-read by the next role, or reviewed later. Commit it first.

```sh
mkdir -p /path/to/new-project && cd /path/to/new-project && git init
```

A workable initial layout:

```text
docs/
  evidence/      literature review, prior art, user or market research
  integration/   systems to integrate with, their contracts and constraints
  decisions/     architecture decision records (empty until phase 2)
  brief.md       product brief (empty until phase 1)
```

Install the adapter into the new repository, then restart Claude Code once so a first-time `.claude/agents/` directory is discovered:

```sh
python3 /path/to/coding-utils/development-agent-suite/tools/install_agent_suite.py \
  --platform claude --target /path/to/new-project
```

See [Codex setup](SETUP-CODEX.md) or [Claude Code setup](SETUP-CLAUDE-CODE.md) for platform details.

## Phase 1 — Scope the problem

Run [`discover-product`](WORKFLOWS.md#discover-product). The output is a decision-ready brief, not code and not product approval.

```text
/discover-product scope <product> for <audience>.

Evidence on disk: docs/evidence/ and docs/integration/. Cite these files by path.
Separate and label: what the evidence establishes, what I have assumed, what is an
untested hypothesis, and what is unknown.

Deliver problem, audience, desired outcome, non-goals, critical journey, measurable
acceptance criteria, and open decisions with an owner for each.

Do not propose an implementation, stack, or schema. Do not create write-capable
workers. Write the result to docs/brief.md.
```

`product-owner` frames outcomes, scope, and measurable acceptance. `ux-researcher` synthesizes the supplied evidence with provenance and may not invent interviews, analytics, or feedback; where your material does not support a claim, it should return a research need instead. `product-designer` explores the critical journey and state model only after the outcome is stable enough, so design work is not spent on an unsettled problem.

Existing evidence changes what these roles do: they classify and stress-test what you gathered rather than proposing new studies. Supplying the material is what keeps the research role honest.

## Phase 2 — Record the decisions

The workflow ends by handing back open decisions. Resolve them yourself and write the resolutions into `docs/brief.md`. Agents may propose alternatives; only an approved decision record becomes shared context for later roles.

This gate is not optional. Implementation task packets are only safe when the product decisions have already been removed from them.

## Phase 3 — Define contracts for the first slice

Run [`plan-feature`](WORKFLOWS.md#plan-feature) against one vertical slice that runs end to end, not the whole product.

```text
/plan-feature the first vertical slice: <thinnest end-to-end path>.

Approved outcome and acceptance criteria: docs/brief.md.
Integration constraints: docs/integration/.
Repository baseline: empty repository, no code yet — skip codebase-explorer.

From software-architect: module boundaries, versioned API and data contracts,
integration seams, failure and observability model, and what is deliberately
deferred. Record it as an ADR under docs/decisions/.

Then delivery-planner: ordered task packets with allowed write sets and one
executable acceptance command per packet.
```

`software-architect` is read-only, so this phase produces a decision record rather than a partially built framework. Scoping it to one slice keeps the contract small enough to freeze; a whole-product architecture written before anything runs will churn.

## Phase 4 — Build the walking skeleton

Run [`implement-feature`](WORKFLOWS.md#implement-feature) with a single writer. The deliverable is the acceptance oracle, not a feature.

```text
/implement-feature build the walking skeleton for docs/decisions/<adr>.md.

Goal: the thinnest end-to-end path that actually runs — real entry point, real call
to <integration>, real response — plus one acceptance test that fails today and
passes when the slice works, and a single command that runs it.

One implementation-engineer. Do not build beyond the skeleton. Stop and report if
the ADR contracts do not survive contact with the real integration.
```

Then have `test-engineer` harden the oracle independently: it must show which incorrect behavior the test rejects and that the test fails for the intended reason rather than environment noise.

This phase is what makes every later verification possible. Reviewing generated code without an executable check produces opinions; a failing-then-passing test produces evidence.

## Phase 5 — Expand under measurement

Once contracts and a runnable acceptance harness exist, a second writer becomes defensible — but only where [the concurrency and stop rules](WORKFLOWS.md#concurrency-and-stop-rules) are satisfied: the task is ready, write sets are disjoint, each slice has its own oracle, and one integrator owns the merge. Add [`review-change`](WORKFLOWS.md#review-change) before integration, and [`security-review`](WORKFLOWS.md#security-review) and [`release-readiness`](WORKFLOWS.md#release-readiness) as the surface and risk warrant.

Scale from measured queue and integration data, not from feature size.

## Sequence summary

| Phase | Workflow | Leading roles | Writes code | Exit condition |
| --- | --- | --- | --- | --- |
| 0 | none | none | Evidence committed | Material is readable by path |
| 1 | `discover-product` | `product-owner`, `ux-researcher`, `product-designer` | No | Brief with labeled evidence and open decisions |
| 2 | none | human decision owner | No | Decisions recorded in the brief |
| 3 | `plan-feature` | `software-architect`, `delivery-planner` | No | ADR, versioned contracts, task packets |
| 4 | `implement-feature` | `implementation-engineer`, `test-engineer` | Yes, one writer | End-to-end path runs; acceptance test fails before and passes after |
| 5 | `implement-feature`, `review-change` | writers plus read-only reviewers | Yes, bounded | Ready queue empty or integration becomes the constraint |

## Stop conditions for a new project

- The product problem or architecture is still being discovered.
- No runnable end-to-end harness exists yet.
- Success is primarily tacit or subjective.
- Contracts change faster than slices can be implemented against them.
- Agents produce code faster than it can be reviewed, or cleanup and rework grow.
- Broad agent permissions would be required to reach production credentials or data.

Any of these means collapse to one writer, or return to phase 2.

## Evidence basis

The ordering above reflects the sibling [multi-agent software engineering literature review](../multi-agent-software-engineering-literature-2026/), specifically its [greenfield and large-feature memo](../multi-agent-software-engineering-literature-2026/04-large-features-greenfield-products.md) and [decision framework](../multi-agent-software-engineering-literature-2026/08-synthesis-decision-framework.md).

Three findings drive the sequence. Dependency and contract planning should precede worker allocation. Ungrounded second-agent review did not improve implementation quality in full-lifecycle evaluation, while execution feedback did, which is why phase 4 precedes any fan-out. Project-level autonomous delivery shows low measured success rates, so this example keeps a human decision owner and one accountable integrator throughout.

Evidence quality for greenfield multi-agent delivery is low. Run the [evaluation guide](EVALUATION.md) against a matched single-agent baseline before standardizing this sequence.
