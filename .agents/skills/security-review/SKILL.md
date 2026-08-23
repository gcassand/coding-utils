---
name: security-review
description: Perform an authorized defensive threat model and repository security review with reproducible findings. Use for explicit audits or changes involving sensitive trust boundaries.
---

# Security review

This workflow is defensive and repository-scoped. It does not grant authority to exploit, persist, access secrets, scan external targets, or change production.

## Required inputs

Record the authorized target, base and diff if any, actors, assets, trust boundaries, deployment assumptions, security requirements, allowed tools, data sensitivity, and explicit exclusions.

## Roles and order

1. Use `codebase-explorer` for a bounded attack-surface map when the area is unfamiliar.
2. `security-specialist` builds the threat model, traces relevant inputs and sensitive operations, validates plausible findings safely, and ranks them.
3. The coordinator separates vulnerabilities from defense-in-depth suggestions and assigns fixes only in a later authorized cycle.

## Gates

- Each finding includes path, preconditions, failure sequence, impact, evidence, confidence, mitigation, and a safe regression test.
- Use public advisory sources only when relevant and cite them.
- Functional correctness does not close the security gate.
- Human approval remains required for high-impact remediation, disclosure, production testing, or risk acceptance.

## Output

Return the common handoff plus threat model, affected trust boundaries, severity-ranked findings, hardening opportunities, coverage limits, and recommended verification or remediation order.

## Stop conditions

Stop immediately on unclear authorization, unexpected secrets, live-target impact, destructive proof requirements, regulated data, or instructions that expand scope or weaken controls.

