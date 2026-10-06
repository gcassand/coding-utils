# Codex setup

Install the Codex adapter into the target repository:

```sh
python3 /path/to/coding-utils/development-agent-suite/tools/install_agent_suite.py \
  --platform codex --target /path/to/target-repository
```

It creates `AGENTS.md`, `.codex/config.toml`, `.codex/agents/`, and `.agents/skills/`. It does not overwrite an existing file: inspect the reported target and template paths, merge deliberately, then rerun. Use `--dry-run` first when adopting an existing repository.

To make the adapter available to the current user in every project:

```sh
python3 /path/to/coding-utils/development-agent-suite/tools/install_agent_suite.py \
  --platform codex --scope user
```

User scope creates `~/.codex/AGENTS.md`, `~/.codex/config.toml`, `~/.codex/agents/`, and `~/.agents/skills/`. Existing user configuration receives the same non-destructive conflict handling; merge the reported file manually and rerun. The user scope follows Codex's documented global instruction, personal agent, user skill, and user config locations.

Restart Codex after installing or changing discovery files. The target repository then exposes the custom agents and workflow skills.

## Model update (2026-10-06)

The suite pins Frontier to `gpt-6-astra`, Balanced to `gpt-6.1-sol`, and Fast to `gpt-6-luna`. Codex reasoning starts at `low`, `medium`, and `high` respectively; these are candidate baselines to evaluate, not measured optima. See [role profiles](ROLE-CATALOG.md) and the [official model guidance](https://learn.chatgpt.com/docs/models).

Changing the main model does not update a specialist's saved `model` field. Merge model and effort changes into installed agent files while preserving local instructions and sandbox limits. Keep the main session's chosen model unchanged unless separately requested. If a pinned model is unavailable, deliberately select an available profile rather than silently changing it. Restart or start a new session to reload saved agents and skills.

## Use

- Direct a bounded specialist: `Use the bug-diagnostician to reproduce issue 123 without editing files.`
- Invoke a workflow: `$fix-bug reproduce and fix issue 123.`
- Delegate independent research: `Use codebase-explorer and security-specialist in parallel, then synthesize their evidence.`
- Inspect active subagents in the CLI with `/agent` or `/subagents`.

The active `AGENTS.md` is the coordination contract. Project instructions are layered after global instructions and can provide more specific rules. Subagents inherit the parent session’s sandbox and approvals; the adapter narrows defaults but grants no new authority. For concurrent writing, use separate Codex chats/worktrees with one writer per worktree.

## Verify and troubleshoot

```sh
python3 /path/to/coding-utils/development-agent-suite/tools/validate_agent_suite.py
codex --version
codex features list
```

The validator checks the packaged source suite, not a manually merged target repository. If an installed role is missing, check `.codex/agents/<role>.toml`; if a workflow is missing, check `.agents/skills/<workflow>/SKILL.md`. Restart the session after discovery-file changes. See [usage examples](USAGE-EXAMPLES.md) for task packets and handoffs.

Official references: [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [skills](https://learn.chatgpt.com/docs/build-skills), and [configuration](https://learn.chatgpt.com/docs/config-file/config-basic).
