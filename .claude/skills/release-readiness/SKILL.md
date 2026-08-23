---
name: release-readiness
description: Assess whether a change is ready to release using test, migration, observability, compatibility, documentation, and rollback evidence. Use before consequential deployment or publication.
---

# Release readiness

Produce a go, conditional-go, or no-go recommendation. Do not deploy, tag, publish, merge, or approve the release.

## Required inputs

Require release scope, artifact identity, target environments, acceptance and regression results, compatibility matrix, migration and rollback plans, observability, staged rollout, owners, support plan, and security disposition.

## Roles and order

1. `release-engineer` owns the evidence matrix and readiness verdict.
2. `test-engineer` evaluates missing or unreliable test evidence.
3. `documentation-engineer` checks user, operator, migration, and support documentation; it remains read-only unless a separate documentation edit is authorized.
4. `security-specialist` participates when security findings, sensitive changes, or risk acceptance require review.

Independent evidence collection may run in parallel. The coordinator resolves contradictions and keeps the human release owner accountable.

## Gates

- Artifact and source commit are unambiguous.
- Acceptance, regression, compatibility, and required non-functional checks pass.
- Migrations are ordered and recovery is tested; Git revert alone is not enough for data or external effects.
- Alerts, dashboards, ownership, rollout stages, stop thresholds, and support documentation exist.

## Output

Return the common handoff plus gate-by-gate evidence, blocking and conditional risks, explicit verdict, required approvals, rollout checkpoints, rollback trigger, and post-release verification.

## Stop conditions

Return no-go when artifact identity, recovery, observability, compatibility, accountable ownership, or required security disposition is missing. Stop before any release action.

