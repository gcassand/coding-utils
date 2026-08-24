# Cross-platform development agent suite

Version **0.1.0**, with documentation checked through **24 August 2026 (Europe/Paris)**.

This is a distributable, stack-agnostic set of 13 lifecycle specialists and seven workflows for Codex and Claude Code. Its source templates remain inside this directory; use the installer to add only the platform and scope you choose.

## Install

Run the installer from a checkout of this repository. The target must already exist.

```sh
# Install Codex into the current repository
python3 development-agent-suite/tools/install_agent_suite.py --platform codex

# Install Codex for the current user, across projects
python3 development-agent-suite/tools/install_agent_suite.py \
  --platform codex --scope user

# Install Claude Code into another repository
python3 development-agent-suite/tools/install_agent_suite.py \
  --platform claude --target /path/to/project

# Install both adapters
python3 development-agent-suite/tools/install_agent_suite.py \
  --platform both --target /path/to/project

# Install both adapters for the current user
python3 development-agent-suite/tools/install_agent_suite.py \
  --platform both --scope user

# Prompt for the platform, without copying files
python3 development-agent-suite/tools/install_agent_suite.py --dry-run
```

The default scope is `project`, rooted at the current directory or `--target`. With `--scope user`, the root defaults to the current user's home directory; `--target` can override it for dotfile staging or tests. The installer uses [installer-manifest.json](installer-manifest.json) as an explicit allowlist. It creates only missing files, recognizes byte-identical files as unchanged, and makes no changes at all if any destination conflicts. Merge conflicts manually, then rerun it. It never installs credentials, deployment settings, or a permission bypass.

## Start here

1. Read the [role catalog](ROLE-CATALOG.md) and choose a [workflow](WORKFLOWS.md).
2. Follow the platform guide: [Codex](SETUP-CODEX.md) or [Claude Code](SETUP-CLAUDE-CODE.md).
3. Use the copy-pasteable [usage examples](USAGE-EXAMPLES.md), or follow the [new-project walkthrough](EXAMPLE-NEW-PROJECT.md) end to end.
4. Read the [security model](SECURITY.md) before granting network, secret, deployment, or production access.
5. Validate a source-suite edit with `python3 development-agent-suite/tools/validate_agent_suite.py`.

For iteration practices, see [authoring](AUTHORING.md) and [evaluation](EVALUATION.md). Release history is in [CHANGELOG.md](CHANGELOG.md).

## Packaged layout

| Content | Location |
| --- | --- |
| Shared Codex instructions | `templates/shared/AGENTS.md` |
| Codex adapters and workflows | `templates/codex/` |
| Claude Code adapters and workflows | `templates/claude/` |
| Safe installation and validation | `tools/` |
| Regression tests | `tests/` |

Official references: [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Claude Code skills](https://code.claude.com/docs/en/slash-commands), and [Claude Code project memory](https://code.claude.com/docs/en/memory).
