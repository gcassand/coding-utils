# Claude Code setup

The checked-in configuration is active when Claude Code starts from this repository. `CLAUDE.md` imports the shared `AGENTS.md`; project agents live in `.claude/agents/`, and skills live in `.claude/skills/`.

## Adopt the suite in another repository

Copy these paths while preserving their relative locations:

```text
AGENTS.md
CLAUDE.md
.claude/agents/
.claude/skills/
development-agent-suite/
scripts/validate_agent_suite.py
```

If the target already has `CLAUDE.md`, add `@AGENTS.md` and merge the Claude-specific rules instead of overwriting it. Merge existing agent and skill directories file by file. After creating a repository's first `.claude/agents/` directory, restart Claude Code; edits in an already-watched directory are normally detected within seconds.

## Use

- Inspect discovery with `/agents`, `/skills`, and `/doctor`.
- Ask directly for a role or `@`-mention it where supported.
- Invoke a workflow with `/fix-bug`, `/plan-feature`, or another checked-in skill.
- Use ordinary subagents for focused work that returns a result to the lead.

Writer agents declare `isolation: worktree`. Claude Code normally creates worktrees from the remote default branch (`fresh`). If the agent needs unpushed or feature-branch state, set `worktree.baseRef` to `head` in the appropriate user, local, or project settings before delegation. This suite intentionally commits no choice. Record the actual base commit in every writer task packet.

## Agent teams

Agent teams are experimental and disabled by default. Do not enable them for ordinary role delegation. Use them only when the user explicitly requests a communicating team and peers genuinely need shared task state or direct messages.

To opt in for a controlled session, set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` outside the repository or in an intentionally reviewed settings file. Enabling it can turn named delegation into teammates, raises token use, and changes coordination behavior. It does not replace worktree isolation or a single integration owner.

## Model substitution and permissions

Agent definitions pin current full model IDs. An organization model allowlist or `CLAUDE_CODE_SUBAGENT_MODEL` may substitute another model; Claude Code reports substitution in interactive sessions. Re-evaluate representative tasks after a model change.

Read-only agents use tool allowlists without `Edit` or `Write`. Writer agents use default approval handling and worktree isolation; none uses `bypassPermissions`, embeds credentials, or grants deployment authority.

Official references: [project memory](https://code.claude.com/docs/en/memory), [subagents](https://code.claude.com/docs/en/sub-agents), [skills](https://code.claude.com/docs/en/slash-commands), [worktrees](https://code.claude.com/docs/en/worktrees), and [agent teams](https://code.claude.com/docs/en/agent-teams).

