---
name: security-review
description: Perform an authorized defensive threat model and repository security review with reproducible findings. Use for explicit audits or changes involving sensitive trust boundaries.
---

# Security review

This workflow is defensive and repository-scoped. It does not grant authority to exploit, persist, access secrets, scan external targets, or change production.

Scale inputs and reporting to the decision and risk. Named roles describe responsibilities; they are optional delegation choices unless the user requests an independent specialist. Continue authorized work through verification and correction; pause only for material missing decisions or permission boundaries.

## Required inputs

Record the authorized target, base and diff if any, actors, assets, trust boundaries, deployment assumptions, security requirements, allowed tools, data sensitivity, and explicit exclusions.

## Roles and order

1. The main session can inspect a narrow, authorized surface directly. Use `codebase-explorer` for an unfamiliar attack surface only when needed.
2. Use `security-specialist` for substantial threat modeling, uncertain exploitability, or requested independent security analysis. Trace relevant inputs and sensitive operations, validate plausible findings safely, and rank them.
3. Separate vulnerabilities from defense-in-depth suggestions and assign fixes only within an authorized remediation scope.

## Gates

- Each finding includes path, preconditions, failure sequence, impact, evidence, confidence, mitigation, and a safe regression test.
- Use public advisory sources only when relevant and cite them.
- Functional correctness does not close the security gate.
- Human approval remains required for high-impact remediation, disclosure, production testing, or risk acceptance.

## Output

Return the common handoff plus threat model, affected trust boundaries, severity-ranked findings, hardening opportunities, coverage limits, and recommended verification or remediation order.

## Stop conditions

Stop immediately on unclear authorization, unexpected secrets, live-target impact, destructive proof requirements, regulated data, or instructions that expand scope or weaken controls.
