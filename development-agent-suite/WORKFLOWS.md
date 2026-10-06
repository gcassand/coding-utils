# Lifecycle workflows

The paired source skills under `templates/codex/.agents/skills/` and `templates/claude/.claude/skills/` expose the workflows below. Install the selected adapter, then invoke them for their decision criteria and verification gates; Named roles are optional unless independent specialist work is requested; the main session can complete bounded tasks directly. Individual roles may also be called directly for bounded work. See [usage examples](USAGE-EXAMPLES.md).

## `discover-product`

Use when the problem, audience, or experience remains uncertain. The coordinator may ask `product-owner`, `ux-researcher`, and `product-designer` for independent evidence. The output is a decision-ready product brief, not code. Research gaps stay labeled as hypotheses; no agent may invent interviews, analytics, or user feedback.

## `bootstrap-project`

Use after the desired outcome is approved but the repository has no meaningful codebase or acceptance harness. One `project-bootstrapper` records low-regret foundation choices, builds the first runnable vertical slice, and implements the approved seed features while architecture and implementation remain tightly coupled. Consequential product, data, security, compliance, cost, hosting, and ownership choices stay with the accountable human. Exit to `plan-feature` and `implement-feature` once another engineer can add a feature without reopening the foundation.

## `plan-feature`

Use after the desired outcome is stable but before implementation. The main session can plan a bounded change directly. Use `codebase-explorer` for unfamiliar paths, `software-architect` for consequential contracts and risks, and `delivery-planner` for multiple ready packets. Implementation waits until the coordinator or human records the chosen design and acceptance oracle.

## `implement-feature`

Use for an approved feature with stable contracts. Start in the main session or with one delegated `implementation-engineer`. Add a second writer or `test-engineer` only when write sets are disjoint, both tasks are ready, and each has an executable oracle. Integrate centrally and run combined tests.

## `fix-bug`

Use for a reported defect. The main session handles localized faults directly. Use `bug-diagnostician` when the cause is uncertain; delegate one `implementation-engineer` for a useful bounded handoff and `test-engineer` for a missing independent regression oracle. Run review or security checks according to risk. Do not run competing writers over the same fault.

## `review-change`

Use for a branch or diff. Keep reviewers read-only and independent on their first pass. `code-reviewer` checks correctness and regressions; `security-specialist` participates only when the changed surface warrants it; `test-engineer` evaluates test gaps. Findings require exact evidence and severity.

## `security-review`

Use for an authorized defensive assessment. `security-specialist` defines the threat boundary, traces attack surfaces, and reports reproducible findings. A `codebase-explorer` may map unfamiliar paths. The workflow does not authorize exploitation, secret access, external scanning, persistence, or production changes.

## `release-readiness`

Use before deployment or release. `release-engineer` owns the checklist; `test-engineer`, `documentation-engineer`, and `security-specialist` contribute only relevant evidence. Missing rollback, migration, observability, compatibility, or acceptance evidence produces a conditional or no-go result, not optimistic completion.

## Concurrency and stop rules

- Default: one capable main session; add a specialist only when it contributes distinct, independently verifiable work.
- Initial cap for a genuinely decomposable feature: coordinator plus at most three specialists.
- Only independent read-heavy work should fan out freely within the configured cap.
- Stop spawning when no ready queue remains.
- Collapse overlapping or sequential work to one owner.
- Stop retrying when repeated attempts produce no new evidence or exceed the stated budget.
