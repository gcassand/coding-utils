---
name: release-readiness
description: Assess whether a change is ready to release using test, migration, observability, compatibility, documentation, and rollback evidence. Use before consequential deployment or publication.
---

# Release readiness

Produce a go, conditional-go, or no-go recommendation. Do not deploy, tag, publish, merge, or approve the release.

Scale inputs and reporting to the decision and risk. Named roles describe responsibilities; they are optional delegation choices unless the user requests an independent specialist. Continue authorized work through verification and correction; pause only for material missing decisions or permission boundaries.

## Required inputs

Require release scope, artifact identity, target environments, acceptance and regression results, compatibility matrix, migration and rollback plans, observability, staged rollout, owners, support plan, and security disposition.

## Roles and order

1. The main session can assess a release from a complete, bounded evidence set directly. Use `release-engineer` when rollout, migration, recovery, or compatibility evidence needs substantial synthesis.
2. Use `test-engineer` for missing or unreliable test evidence, and `documentation-engineer` for uncertain user or operator documentation; both remain read-only unless an edit is authorized.
3. Use `security-specialist` when security findings, sensitive changes, or risk acceptance require independent review.

Independent evidence collection may run in parallel when useful. The coordinator resolves contradictions and keeps the human release owner accountable.

## Gates

- Artifact and source commit are unambiguous.
- Acceptance, regression, compatibility, and required non-functional checks pass.
- Migrations are ordered and recovery is tested; Git revert alone is not enough for data or external effects.
- Alerts, dashboards, ownership, rollout stages, stop thresholds, and support documentation exist.

## Output

Return the common handoff plus gate-by-gate evidence, blocking and conditional risks, explicit verdict, required approvals, rollout checkpoints, rollback trigger, and post-release verification.

## Stop conditions

Return no-go when artifact identity, recovery, observability, compatibility, accountable ownership, or required security disposition is missing. Stop before any release action.
