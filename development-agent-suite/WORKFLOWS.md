# Lifecycle workflows

The paired skills under `.agents/skills/` and `.claude/skills/` expose the workflows below. Invoke them explicitly when you want the full orchestration; individual roles may also be called directly for bounded work.

## `discover-product`

Use when the problem, audience, or experience remains uncertain. The coordinator may ask `product-owner`, `ux-researcher`, and `product-designer` for independent evidence. The output is a decision-ready product brief, not code. Research gaps stay labeled as hypotheses; no agent may invent interviews, analytics, or user feedback.

## `plan-feature`

Use after the desired outcome is stable but before implementation. `codebase-explorer` maps the existing system; `software-architect` defines contracts and risks; `delivery-planner` creates ordered task packets. Implementation waits until the coordinator or human records the chosen design and acceptance oracle.

## `implement-feature`

Use for an approved feature with stable contracts. Start with one `implementation-engineer`. Add a second writer or `test-engineer` only when write sets are disjoint, both tasks are ready, and each has an executable oracle. Integrate centrally and run combined tests.

## `fix-bug`

Use for a reported defect. `bug-diagnostician` reproduces and localizes without editing. One `implementation-engineer` owns the minimal fix; `test-engineer` adds a regression oracle when needed. Run review or security checks according to risk. Do not run competing writers over the same fault.

## `review-change`

Use for a branch or diff. Keep reviewers read-only and independent on their first pass. `code-reviewer` checks correctness and regressions; `security-specialist` participates only when the changed surface warrants it; `test-engineer` evaluates test gaps. Findings require exact evidence and severity.

## `security-review`

Use for an authorized defensive assessment. `security-specialist` defines the threat boundary, traces attack surfaces, and reports reproducible findings. A `codebase-explorer` may map unfamiliar paths. The workflow does not authorize exploitation, secret access, external scanning, persistence, or production changes.

## `release-readiness`

Use before deployment or release. `release-engineer` owns the checklist; `test-engineer`, `documentation-engineer`, and `security-specialist` contribute only relevant evidence. Missing rollback, migration, observability, compatibility, or acceptance evidence produces a conditional or no-go result, not optimistic completion.

## Concurrency and stop rules

- Default: coordinator plus one active specialist.
- Initial cap for a genuinely decomposable feature: coordinator plus at most three specialists.
- Only independent read-heavy work should fan out freely within the configured cap.
- Stop spawning when no ready queue remains.
- Collapse overlapping or sequential work to one owner.
- Stop retrying when repeated attempts produce no new evidence or exceed the stated budget.

