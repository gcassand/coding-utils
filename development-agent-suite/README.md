# Cross-platform development agent suite

Version **0.1.0**, with documentation checked through **23 August 2026 (Europe/Paris)**.

This directory is the implementation companion to the repository's [multi-agent software-engineering literature review](../multi-agent-software-engineering-literature-2026/). It provides the same 13 lifecycle specialists and seven workflows for Codex and Claude Code while preserving each tool's native configuration format.

## Design in one minute

- The main session is the coordinator, decision owner, and integrator.
- One agent is the default. Multiple agents are used only for independent, independently verifiable work.
- Research and review roles are read-only. Implementation, test, and documentation roles may write only inside an assigned slice and isolated worktree.
- Agents return evidence and executable results, not confidence or consensus.
- Codex and Claude adapters are hand-maintained twins checked by an offline validator.

## Start here

1. Review the [role catalog](ROLE-CATALOG.md).
2. Choose a [workflow](WORKFLOWS.md) rather than assembling a team by job title alone.
3. Follow [Codex setup](SETUP-CODEX.md) or [Claude Code setup](SETUP-CLAUDE-CODE.md).
4. Read the [security model](SECURITY.md) before granting network, secret, deployment, or production access.
5. Run `python3 scripts/validate_agent_suite.py` after any change.

For iteration practices, see [authoring](AUTHORING.md) and [evaluation](EVALUATION.md). Release history is recorded in [CHANGELOG.md](CHANGELOG.md).

## Configuration map

| Surface | Codex | Claude Code |
| --- | --- | --- |
| Repository instructions | `AGENTS.md` | `CLAUDE.md` importing `AGENTS.md` |
| Agent definitions | `.codex/agents/*.toml` | `.claude/agents/*.md` |
| Workflow skills | `.agents/skills/*/SKILL.md` | `.claude/skills/*/SKILL.md` |
| Project defaults | `.codex/config.toml` | No committed settings override |

Official references: [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Claude Code skills](https://code.claude.com/docs/en/slash-commands), and [Claude Code project memory](https://code.claude.com/docs/en/memory).

