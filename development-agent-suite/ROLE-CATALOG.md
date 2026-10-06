# Role catalog

Roles describe bounded responsibilities, not an autonomous organization chart. The main session coordinates and integrates; no specialist becomes the product, architecture, security, or release authority.

| Role | Primary artifact | Profile | Access |
| --- | --- | --- | --- |
| `product-owner` | Outcome brief or PRD with measurable acceptance criteria | Balanced | Read-only |
| `ux-researcher` | Research plan or evidence synthesis with provenance | Balanced | Read-only; web only when authorized |
| `product-designer` | Interaction specification, states, content, and accessibility notes | Frontier | Read-only |
| `software-architect` | ADR, dependency map, contracts, migration and rollback constraints | Frontier | Read-only |
| `project-bootstrapper` | Minimal greenfield architecture, walking skeleton, acceptance harness, and first vertical features | Frontier | Writer in assigned worktree/slice |
| `delivery-planner` | Ordered task packets with owners, dependencies, and acceptance commands | Balanced | Read-only |
| `codebase-explorer` | Concise execution-path and ownership map | Fast | Read-only |
| `bug-diagnostician` | Reproduction, root-cause evidence, and falsified alternatives | Frontier | Read-only |
| `implementation-engineer` | Minimal contract-bounded code change | Frontier | Writer in assigned worktree/slice |
| `test-engineer` | Targeted, regression, contract, or adversarial tests | Balanced | Writer in assigned worktree/slice |
| `code-reviewer` | Severity-ranked correctness and maintainability findings | Frontier | Read-only |
| `security-specialist` | Threat model and evidence-backed security findings | Frontier | Read-only |
| `documentation-engineer` | Accurate user, API, operator, or maintenance documentation | Balanced | Writer in assigned worktree/slice |
| `release-engineer` | Go/no-go evidence and unresolved release risks | Balanced | Read-only |

## Model profiles

| Profile | Codex | Claude Code | Intended work |
| --- | --- | --- | --- |
| Frontier | `gpt-6-astra` | `claude-opus-5` | Ambiguous implementation, architecture, diagnosis, adversarial review |
| Balanced | `gpt-6.1-sol` | `claude-sonnet-5` | Planning, testing, documentation, product synthesis, release review |
| Fast | `gpt-6-luna` | `claude-haiku-4-5` | Bounded read-heavy repository mapping |

OpenAI profiles checked on **2026-10-06** against the [official model guidance](https://learn.chatgpt.com/docs/models). Use GPT-6.1 Sol for routine coding in the main session; reserve the Frontier specialist profile for difficult architecture, diagnosis, and review. Saved specialist models are independent of the main session's model. Availability depends on account, client, and workspace controls; if unavailable, deliberately select an available model rather than silently falling back.

Codex starting efforts are `low` for Astra, `medium` for Sol (an explicit suite baseline, not a claim about the client's default), and `high` for Luna. Escalate only when representative checks show a quality need. Efforts do not map directly between generations. These are documentation-informed starting points, not measured performance claims. `codex_effort` in the catalog controls Codex; the existing `effort` field retains Claude settings and model pins from August 2026.

The Claude quality-first override is `claude-fable-5`; it is intentionally not a default because this suite uses balanced cost and latency profiles. Organizations may override models through their normal configuration, but they should rerun representative evaluations after doing so.

## Common task packet

Before delegating, provide:

1. Objective, user-visible outcome, and non-goals.
2. Relevant artifacts and authoritative decisions.
3. Base commit and allowed write surface.
4. Dependencies and frozen contract version.
5. Permission envelope and forbidden actions.
6. Acceptance commands and expected observations.
7. Time, token, retry, and stopping limits when material.

## Common handoff

Every role returns these headings:

- **Objective and scope**
- **Evidence** with exact files, symbols, commands, URLs, or observations
- **Artifacts or changes**
- **Checks run** and their results
- **Contract or assumption changes**
- **Unresolved risks**
- **Recommended next action**

Downstream work must validate the handoff before consuming it. A clean merge or another agent's agreement is not validation.
