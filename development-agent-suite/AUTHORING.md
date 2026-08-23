# Authoring and versioning

The Codex and Claude files are hand-maintained twins. The machine-readable catalog defines inventory, profile, effort, and access expectations, but it is not a prompt generator.

## Change a role

1. Edit both `.codex/agents/<role>.toml` and `.claude/agents/<role>.md`.
2. Preserve the common required sections and handoff contract.
3. Keep the role narrow; move a repeated multi-role procedure into a workflow skill.
4. Update `catalog.json` when profile, effort, access, or inventory changes.
5. Update the role catalog and changelog for user-visible changes.
6. Run validation and behavioral fixtures before committing.

## Change a workflow

1. Edit both `.agents/skills/<workflow>/SKILL.md` and `.claude/skills/<workflow>/SKILL.md`.
2. Keep descriptions discriminating so unrelated tasks do not trigger the skill.
3. State required inputs, participating roles, dependency order, gates, concurrency, stop conditions, and final output.
4. Avoid copying setup manuals into skills; link to maintained documentation when users need platform details.
5. Add or update an evaluation fixture for any changed decision rule.

## Change models

Review the current official [OpenAI model guidance](https://developers.openai.com/api/docs/guides/latest-model) and [Anthropic model overview](https://platform.claude.com/docs/en/about-claude/models/overview). Update `catalog.json`, every affected adapter, the role catalog, the documentation baseline, and the changelog together. Do not silently replace a user-requested or pinned model. Re-run matched behavioral evaluations because a newer model does not guarantee better task-specific results.

## Version policy

- Patch: wording, documentation, or validation corrections without changed role behavior.
- Minor: new role/workflow or material behavior, permission, or profile change.
- Major: incompatible file layout, invocation, or handoff-contract change.

Record the model IDs, suite version, repository commit, and tool versions with evaluation results. Hosted execution is auditable but not necessarily deterministic.

