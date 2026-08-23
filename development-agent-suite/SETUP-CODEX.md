# Codex setup

Install the Codex adapter into the target repository:

```sh
python3 /path/to/coding-utils/development-agent-suite/tools/install_agent_suite.py \
  --platform codex --target /path/to/target-repository
```

It creates `AGENTS.md`, `.codex/config.toml`, `.codex/agents/`, and `.agents/skills/`. It does not overwrite an existing file: inspect the reported target and template paths, merge deliberately, then rerun. Use `--dry-run` first when adopting an existing repository.

Restart Codex after installing or changing discovery files. The target repository then exposes the custom agents and workflow skills.

## Use

- Direct a bounded specialist: `Use the bug-diagnostician to reproduce issue 123 without editing files.`
- Invoke a workflow: `$fix-bug reproduce and fix issue 123.`
- Delegate independent research: `Use codebase-explorer and security-specialist in parallel, then synthesize their evidence.`
- Inspect active subagents in the CLI with `/agent` or `/subagents`.

The target `AGENTS.md` is the coordination contract. Subagents inherit the parent session’s sandbox and approvals; the adapter narrows defaults but grants no new authority. For concurrent writing, use separate Codex chats/worktrees with one writer per worktree.

## Verify and troubleshoot

```sh
python3 /path/to/coding-utils/development-agent-suite/tools/validate_agent_suite.py
codex --version
codex features list
```

The validator checks the packaged source suite, not a manually merged target repository. If an installed role is missing, check `.codex/agents/<role>.toml`; if a workflow is missing, check `.agents/skills/<workflow>/SKILL.md`. Restart the session after discovery-file changes. See [usage examples](USAGE-EXAMPLES.md) for task packets and handoffs.

Official references: [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [skills](https://learn.chatgpt.com/docs/build-skills), and [configuration](https://learn.chatgpt.com/docs/config-file/config-basic).

