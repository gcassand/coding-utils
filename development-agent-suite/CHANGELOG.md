# Changelog

## Unreleased

## 0.3.0 - 2026-10-06

- Updated Codex Frontier/Balanced/Fast profiles to GPT-6 Astra, GPT-6.1 Sol, and GPT-6 Luna; retained Claude model and effort pins.
- Separated Codex reasoning effort from Claude effort, starting at low/medium/high by profile.
- Made specialist routing conditional; localized work can remain in the main session with proportionate checks.
- Clarified continued execution within authorized scope and scaled inputs, handoffs, and testing to risk.
- Added migration evaluation guidance; model performance comparisons remain to be measured on representative tasks.

## 0.2.0 - 2026-08-24

- Added paired `project-bootstrapper` agents for the empty-repository foundation phase.
- Added the paired `bootstrap-project` workflow and a greenfield walking-skeleton evaluation fixture.
- Bumped the suite catalog to 0.2.0 with 14 agents, eight workflows, and eight behavioral fixtures.
- Added `--scope user` installation for Codex and Claude Code, while keeping project scope as the default.
- Repackaged all installable adapters and tools inside `development-agent-suite/`.
- Added a manifest-driven, non-destructive installer for Codex, Claude Code, or both.
- Added installation, direct-role, workflow, worktree, and handoff examples.
- Added a greenfield new-project walkthrough covering workflow order, decision gates, and the acceptance-oracle phase.

## 0.1.0 - 2026-08-23

- Added 13 paired Codex and Claude Code development specialists.
- Added seven paired lifecycle workflow skills.
- Added least-privilege, worktree, handoff, validation, setup, and evaluation guidance.
- Pinned balanced August 2026 model profiles for both platforms.
