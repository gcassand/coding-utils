# Codex setup

The checked-in configuration is active when Codex starts from this repository. Codex reads `AGENTS.md`, project custom agents under `.codex/agents/`, project configuration from `.codex/config.toml`, and repository skills under `.agents/skills/`.

## Adopt the suite in another repository

Copy these paths while preserving their relative locations:

```text
AGENTS.md
.codex/config.toml
.codex/agents/
.agents/skills/
development-agent-suite/
scripts/validate_agent_suite.py
```

Do not overwrite an existing `AGENTS.md` or `.codex/config.toml`. Merge durable repository conventions into `AGENTS.md`, and merge the `[agents]` table into the existing project config. Existing, more-specific nested `AGENTS.md` files continue to apply within their subtrees.

Start a new Codex session after copying or changing project instructions. Run the validator before use.

## Use

- Ask directly for a role: `Use the bug-diagnostician to reproduce issue 123 without editing files.`
- Invoke a workflow skill by name: `$fix-bug reproduce and fix issue 123.`
- Ask for parallel work only when the work packets are independent: `Use codebase-explorer and security-specialist in parallel, wait for both, then synthesize their evidence.`
- In the CLI, use `/agent` or `/subagents` to inspect spawned threads.

Subagents inherit the parent turn's live sandbox and approval choices. The custom files narrow defaults, but they do not grant new authority. For concurrent write-heavy work, prefer separate Codex chats/worktrees with one writer per worktree rather than multiple writers in one shared checkout.

## Project defaults

`.codex/config.toml` enables subagents and caps open spawned threads at four. It does not broaden the parent sandbox, configure credentials, or enable external services. Model and reasoning settings are pinned per role so they can be reviewed independently.

## Verify and troubleshoot

```sh
python3 scripts/validate_agent_suite.py
codex --version
codex features list
```

If a role is missing, confirm the file is a readable TOML file under `.codex/agents/` and contains `name`, `description`, and `developer_instructions`. If a skill is missing, confirm it is under `.agents/skills/<name>/SKILL.md` with matching `name` and `description` frontmatter. Restart the session after changing discovery files.

Official references: [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [skills](https://learn.chatgpt.com/docs/build-skills), and [configuration](https://learn.chatgpt.com/docs/config-file/config-basic).

