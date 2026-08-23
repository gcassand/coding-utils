@AGENTS.md

## Claude Code

- Use project agents from `.claude/agents/` and workflows from `.claude/skills/`.
- Keep experimental agent teams disabled unless the user explicitly asks for a communicating team. Ordinary subagents are the default delegation surface.
- Writer agents use worktree isolation. Record whether the worktree starts from the remote default branch or local `HEAD`; this repository does not impose a `worktree.baseRef` setting.
- After creating `.claude/agents/` for the first time, restart Claude Code. For later edits, verify discovery with `/agents`, `/skills`, and `/doctor`.

