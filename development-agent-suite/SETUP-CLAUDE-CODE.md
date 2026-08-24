# Claude Code setup

Install the Claude Code adapter into the target repository:

```sh
python3 /path/to/coding-utils/development-agent-suite/tools/install_agent_suite.py \
  --platform claude --target /path/to/target-repository
```

It creates `CLAUDE.md`, `.claude/agents/`, and `.claude/skills/`. The Claude-only install is self-contained. The installer never overwrites existing files: resolve every reported conflict manually and rerun; use `--dry-run` to inspect first.

To make the adapter available to the current user in every project:

```sh
python3 /path/to/coding-utils/development-agent-suite/tools/install_agent_suite.py \
  --platform claude --scope user
```

User scope creates `~/.claude/CLAUDE.md`, `~/.claude/agents/`, and `~/.claude/skills/`. Existing user configuration receives the same non-destructive conflict handling; merge the reported file manually and rerun.

After creating a repository’s first `.claude/agents/` directory, restart Claude Code. Later edits in an already-watched directory are normally detected quickly.

## Use

- Inspect discovery with `/agents`, `/skills`, and `/doctor`.
- Ask directly for a named role where supported.
- Invoke `/fix-bug`, `/plan-feature`, or another installed workflow.
- Use ordinary subagents for focused work that returns a result to the lead.

Writer agents declare `isolation: worktree`. Claude Code normally uses the remote default branch (`fresh`). When work must include unpushed or feature-branch state, set `worktree.baseRef` to `head` in an appropriate settings surface and record the chosen base commit in the task packet. This suite intentionally commits no default.

## Agent teams and troubleshooting

Agent teams are experimental and disabled by default. Enable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` only on explicit user request when peers truly need shared task state or direct messages. It increases cost and changes delegation behavior; ordinary subagents are preferable for isolated roles.

An organization model allowlist or `CLAUDE_CODE_SUBAGENT_MODEL` can substitute a model. Re-run representative evaluations after any substitution. Read-only agents exclude `Edit` and `Write`; writers use default approval handling and worktree isolation. See [usage examples](USAGE-EXAMPLES.md) for direct prompts, writer packets, and expected handoffs.

Official references: [project memory](https://code.claude.com/docs/en/memory), [subagents](https://code.claude.com/docs/en/sub-agents), [skills](https://code.claude.com/docs/en/slash-commands), [worktrees](https://code.claude.com/docs/en/worktrees), and [agent teams](https://code.claude.com/docs/en/agent-teams).
