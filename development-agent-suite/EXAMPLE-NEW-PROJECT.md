# Worked example: starting a new project

This example applies the suite to a greenfield product where research, literature, or integration material already exists but no code does. It shows the workflow order, where a human decision is mandatory, and where fan-out is premature.

Greenfield delivery is the least evidenced use of multiple agents. Treat this sequence as a disciplined default to be measured locally, not as a proven optimum. Codex invokes a workflow with `$name`; Claude Code exposes the same name as `/name`.

## When this example applies

- Evidence exists — a literature review, prior art, market or user research, integration constraints — but no running code.
- One human remains accountable for product and architecture decisions.
- If the outcome, non-goals, and acceptance criteria are already written down and stable, skip to [phase 3](#phase-3--bootstrap-the-architecture-in-code).

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

## Phase 3 — Bootstrap the architecture in code

Run [`bootstrap-project`](WORKFLOWS.md#bootstrap-project) against one vertical slice that runs end to end, not the whole product. `project-bootstrapper` is the single founding writer: it may make and record reversible, low-regret engineering choices, while consequential commitments return to the human owner.

```text
/bootstrap-project start the product in this empty repository.

Approved outcome and acceptance criteria: docs/brief.md.
Evidence and integration constraints: docs/evidence/ and docs/integration/.
Supported environments, dependency policy, and quality priorities: <paths or facts>.
First vertical slice: <thinnest real entry-to-output path>.
Approved seed features: <small ordered list>.

Compare only viable foundations. Choose the simplest mature option that fits the
constraints, record the selected decision and rejected alternatives under
docs/decisions/, then build the walking skeleton before expanding it.

The skeleton must exercise the real entry point and integration boundary. Provide
one documented clean-start command, an acceptance test that rejects relevant wrong
behavior, and build, static/type, test, and runtime smoke evidence. Implement the
seed features sequentially as vertical slices. Do not add speculative services,
layers, persistence, queues, caches, hosting, or deployment machinery.

Stop for any consequential product, data, security, compliance, cost, hosting, or
maintenance-ownership decision, or if the chosen contract fails against reality.
```

Keeping architecture and implementation under one founding writer avoids a false handoff: before the first code runs, contracts are hypotheses and every proposed slice still converges on the same files and decisions. The bootstrapper earns abstractions through the first real path, keeps the decision record aligned with the code, and ends its ownership once another engineer can add a feature without reopening the foundation.

After the skeleton runs, `test-engineer`, `code-reviewer`, or `security-specialist` may produce independent evidence against explicit risk criteria. A reviewer must show which incorrect behavior or risk its oracle detects; agreement with the bootstrapper is not a gate.

## Phase 4 — Transfer to normal feature delivery

Use [`plan-feature`](WORKFLOWS.md#plan-feature) and [`implement-feature`](WORKFLOWS.md#implement-feature) for later features only after the bootstrap handoff includes stable clean-start and acceptance commands, module and contract boundaries, dependency conventions, deferred complexity, and explicit write ownership.

At that point a second writer becomes defensible only where [the concurrency and stop rules](WORKFLOWS.md#concurrency-and-stop-rules) are satisfied: the task is ready, write sets are disjoint, each slice has its own oracle, and one integrator owns the merge. Add [`review-change`](WORKFLOWS.md#review-change) before integration, and [`security-review`](WORKFLOWS.md#security-review) and [`release-readiness`](WORKFLOWS.md#release-readiness) as the surface and risk warrant.

Scale from measured queue and integration data, not from feature size.

## Sequence summary

| Phase | Workflow | Leading roles | Writes code | Exit condition |
| --- | --- | --- | --- | --- |
| 0 | none | none | Evidence committed | Material is readable by path |
| 1 | `discover-product` | `product-owner`, `ux-researcher`, `product-designer` | No | Brief with labeled evidence and open decisions |
| 2 | none | human decision owner | No | Decisions recorded in the brief |
| 3 | `bootstrap-project` | `project-bootstrapper`; optional independent verifiers after the skeleton runs | Yes, one founding writer | Decisions recorded; clean end-to-end path and seed features pass acceptance |
| 4 | `plan-feature`, `implement-feature`, `review-change` | bounded writers plus read-only reviewers | Yes, bounded | Normal feature work proceeds without reopening the foundation |

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

Three findings drive the sequence. Dependency and contract planning should precede worker allocation. Ungrounded second-agent review did not improve implementation quality in full-lifecycle evaluation, while execution feedback did, which is why the phase 3 walking skeleton precedes any fan-out. Project-level autonomous delivery shows low measured success rates, so this example keeps a human decision owner and one accountable integrator throughout.

Evidence quality for greenfield multi-agent delivery is low. Run the [evaluation guide](EVALUATION.md) against a matched single-agent baseline before standardizing this sequence.
