---
name: bootstrap-project
description: Start an approved software product when no usable codebase exists, producing a decision record, minimal runnable foundation, acceptance harness, and first vertical features before normal feature delivery.
---

# Bootstrap project

Keep the main session accountable for product and consequential architecture decisions. Use the main session or one delegated `project-bootstrapper` as the founding write owner while architecture and implementation are still tightly coupled; this workflow is not permission for autonomous product invention or deployment.

Scale inputs and reporting to the decision and risk. Named roles describe responsibilities; they are optional delegation choices unless the user requests an independent specialist. Continue authorized work through verification and correction; pause only for material missing decisions or permission boundaries.

## Required inputs

Require an approved user-visible outcome, target users and critical journey, non-goals, measurable acceptance criteria, the exact externally visible contract for the initial boundary including field mappings when applicable, observable success and error examples, supported environments, integration constraints, quality-attribute priorities, dependency and license policy, initial vertical slice, decision owner, repository baseline, and allowed write surface. The executable acceptance oracle may be absent because creating it is a workflow output. Label unknowns. If product behavior or the problem is unresolved, route to `discover-product` before creating a writer.

## Roles and order

1. The coordinator confirms that the repository has no meaningful inherited runtime or acceptance harness and classifies choices as reversible defaults or consequential commitments.
2. One founding write owner (the main session or `project-bootstrapper`) owns the isolated repository or checkout, using a worktree once a base commit exists. It records the smallest viable architecture and alternatives, then builds and verifies one end-to-end walking skeleton before expanding the design.
3. The same bootstrapper implements approved early features sequentially as dependency-cohesive vertical slices while the foundation is still changing. Do not divide the initial scaffold by files or layers.
4. After the first executable slice, use `test-engineer`, `code-reviewer`, or `security-specialist` only when they can produce independent evidence against explicit risk criteria. Keep one integration owner.
5. Exit to `plan-feature` and `implement-feature` once the clean-start command, conventions, contracts, ownership boundaries, and acceptance harness are stable enough for another engineer to add a feature without reopening the foundation.

## Gates

- Product value and acceptance are approved before stack selection or code.
- The externally visible contract, response behavior, and error semantics needed by the slice must be supplied or approved, including field mappings when applicable. Stop rather than convert examples or assumptions into product facts.
- Reversible choices may proceed with a recorded rationale; choices that materially constrain data, security, compliance, cost, hosting, or long-term ownership return to the accountable human.
- Prefer the simplest mature option that fits supplied constraints and team ownership. Every dependency and foundational component must be justified by a present requirement, quality attribute, or verification need.
- Verify time-sensitive compatibility, maintenance, and support claims against official primary sources when browsing is available and authorized; record source dates for consequential choices.
- The walking skeleton must exercise the real entry point and at least one real boundary, not only compile generated boilerplate. Hard constraints must be enforced and covered by negative tests, not merely documented or used as defaults.
- A documented clean-start command plus build, static or type checks, focused tests, acceptance test, and runtime smoke check must pass from a clean state. Temporarily introduce or simulate one relevant implementation defect, run the exact acceptance command and capture the intended failure, restore the correct implementation, then rerun and capture the pass. Input rejection alone is not proof that the oracle detects wrong implemented behavior.
- No second writer starts until the first vertical slice is runnable and the proposed write sets and contracts are independent. Network installation, credentials, paid services, remote repository changes, infrastructure, and deployment require separate authorization.

## Output

Return the common handoff plus the selected foundation and rejected alternatives; concise decision records; project and dependency map; exact clean-start, development, and acceptance commands; implemented feature-to-test traceability; supported and unsupported boundaries; deferred complexity; current operational and security assumptions; and explicit exit criteria for normal feature delivery.

## Stop conditions

Stop when the outcome or first slice is not approved, externally visible contract details or behavior are unspecified, consequential choices lack an owner, organization or compliance constraints are missing, no credible clean acceptance oracle can be built, external credentials or mutations are required, the architecture fails against the real integration, or cleanup and contract churn outpace feature progress. Return to product discovery for unresolved value; request a human architecture decision for materially different commitments; collapse to the single bootstrapper when writers would overlap.
