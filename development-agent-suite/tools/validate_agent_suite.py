#!/usr/bin/env python3
"""Validate the repository's hand-maintained Codex and Claude agent suite."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any


SUITE_ROOT = Path(__file__).resolve().parents[1]
AGENT_REQUIRED_FIELDS = ("name", "description")
CLAUDE_REQUIRED_FIELDS = ("model", "effort", "permissionMode")
WORKFLOW_SECTIONS = (
    "Required inputs",
    "Roles and order",
    "Gates",
    "Output",
    "Stop conditions",
)
UNSAFE_PATH_PATTERNS = (
    re.compile(r"/Users/[^\s`\"']+"),
    re.compile(r"/home/[^\s`\"']+"),
    re.compile(r"[A-Za-z]:\\\\Users\\\\[^\s`\"']+"),
)


class FrontmatterError(ValueError):
    """Raised when a Markdown file has unsupported or malformed frontmatter."""


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    """Parse the simple scalar frontmatter used by this repository."""

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("missing opening frontmatter delimiter")

    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise FrontmatterError("missing closing frontmatter delimiter") from exc

    metadata: dict[str, str] = {}
    for line_number, raw_line in enumerate(lines[1:end], start=2):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line[:1].isspace() or ":" not in raw_line:
            raise FrontmatterError(
                f"unsupported frontmatter at line {line_number}: {raw_line!r}"
            )
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key or not value:
            raise FrontmatterError(f"empty key or value at line {line_number}")
        if key in metadata:
            raise FrontmatterError(f"duplicate frontmatter key {key!r}")
        metadata[key] = value

    return metadata, "\n".join(lines[end + 1 :]).strip()


def load_catalog(root: Path) -> dict[str, Any]:
    path = root / "catalog.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _check_sections(
    errors: list[str], label: str, body: str, required_sections: list[str]
) -> None:
    for section in required_sections:
        if not re.search(rf"^#{{1,2}}\s+{re.escape(section)}\s*$", body, re.MULTILINE):
            errors.append(f"{label}: missing required section {section!r}")


def _check_unsafe_paths(errors: list[str], label: str, text: str) -> None:
    for pattern in UNSAFE_PATH_PATTERNS:
        match = pattern.search(text)
        if match:
            errors.append(f"{label}: contains unsafe user-specific path {match.group(0)!r}")


def _validate_catalog(errors: list[str], catalog: dict[str, Any]) -> None:
    if catalog.get("version") != "0.2.0":
        errors.append("catalog: expected suite version 0.2.0")
    if catalog.get("documentation_baseline") != "2026-08-24":
        errors.append("catalog: documentation baseline must be 2026-08-24")

    profiles = catalog.get("profiles", {})
    if set(profiles) != {"frontier", "balanced", "fast"}:
        errors.append("catalog: profiles must be frontier, balanced, and fast")

    agent_ids = [entry.get("id") for entry in catalog.get("agents", [])]
    workflow_ids = catalog.get("workflows", [])
    fixture_ids = catalog.get("evaluation_fixtures", [])
    if len(agent_ids) != 14 or len(set(agent_ids)) != 14:
        errors.append("catalog: expected 14 unique agents")
    if len(workflow_ids) != 8 or len(set(workflow_ids)) != 8:
        errors.append("catalog: expected eight unique workflows")
    if len(fixture_ids) != 8 or len(set(fixture_ids)) != 8:
        errors.append("catalog: expected eight unique evaluation fixtures")


def _validate_installer_manifest(
    errors: list[str], root: Path, expected_agents: set[str], expected_workflows: set[str]
) -> None:
    """Ensure the installer has an explicit, complete, safe allowlist."""

    path = root / "installer-manifest.json"
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"installer manifest: cannot parse: {exc}")
        return
    if manifest.get("version") != 1 or not isinstance(manifest.get("files"), list):
        errors.append("installer manifest: expected version 1 and files list")
        return

    expected: set[tuple[str, str, tuple[str, ...]]] = {
        ("templates/shared/AGENTS.md", "AGENTS.md", ("codex",)),
        ("templates/codex/.codex/config.toml", ".codex/config.toml", ("codex",)),
        ("templates/claude/CLAUDE.md", "CLAUDE.md", ("claude",)),
    }
    expected.update(
        (
            f"templates/codex/.codex/agents/{agent}.toml",
            f".codex/agents/{agent}.toml",
            ("codex",),
        )
        for agent in expected_agents
    )
    expected.update(
        (
            f"templates/claude/.claude/agents/{agent}.md",
            f".claude/agents/{agent}.md",
            ("claude",),
        )
        for agent in expected_agents
    )
    expected.update(
        (
            f"templates/codex/.agents/skills/{workflow}/SKILL.md",
            f".agents/skills/{workflow}/SKILL.md",
            ("codex",),
        )
        for workflow in expected_workflows
    )
    expected.update(
        (
            f"templates/claude/.claude/skills/{workflow}/SKILL.md",
            f".claude/skills/{workflow}/SKILL.md",
            ("claude",),
        )
        for workflow in expected_workflows
    )

    actual: set[tuple[str, str, tuple[str, ...]]] = set()
    destinations: set[str] = set()
    for entry in manifest["files"]:
        if not isinstance(entry, dict):
            errors.append("installer manifest: entry must be an object")
            continue
        source, destination, platforms, conflict = (
            entry.get("source"),
            entry.get("destination"),
            entry.get("platforms"),
            entry.get("conflict"),
        )
        if not isinstance(source, str) or not isinstance(destination, str) or not isinstance(platforms, list):
            errors.append("installer manifest: entry requires source, destination, and platforms")
            continue
        if Path(source).is_absolute() or ".." in Path(source).parts or Path(destination).is_absolute() or ".." in Path(destination).parts:
            errors.append(f"installer manifest: unsafe path for {destination!r}")
            continue
        if destination in destinations:
            errors.append(f"installer manifest: duplicate destination {destination!r}")
        destinations.add(destination)
        if conflict != "manual-merge":
            errors.append(f"installer manifest: unsafe conflict policy for {destination!r}")
        actual.add((source, destination, tuple(sorted(platforms))))

    if actual != expected:
        errors.append("installer manifest: allowlist does not match packaged templates")


def validate_suite(root: Path = SUITE_ROOT) -> list[str]:
    errors: list[str] = []
    try:
        catalog = load_catalog(root)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"catalog: cannot load catalog.json: {exc}"]

    _validate_catalog(errors, catalog)
    profiles = catalog.get("profiles", {})
    required_sections = catalog.get("required_prompt_sections", [])
    expected_agents = {entry["id"] for entry in catalog.get("agents", []) if "id" in entry}
    expected_workflows = set(catalog.get("workflows", []))
    _validate_installer_manifest(errors, root, expected_agents, expected_workflows)

    config_path = root / "templates" / "codex" / ".codex" / "config.toml"
    try:
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
        agents_config = config.get("agents", {})
        if agents_config.get("enabled") is not True:
            errors.append("templates/codex/.codex/config.toml: agents.enabled must be true")
        cap = agents_config.get("max_concurrent_threads_per_session")
        if not isinstance(cap, int) or not 1 <= cap <= 4:
            errors.append("templates/codex/.codex/config.toml: concurrency cap must be between 1 and 4")
    except (OSError, tomllib.TOMLDecodeError) as exc:
        errors.append(f"templates/codex/.codex/config.toml: cannot parse: {exc}")

    codex_dir = root / "templates" / "codex" / ".codex" / "agents"
    claude_dir = root / "templates" / "claude" / ".claude" / "agents"
    actual_codex = {path.stem for path in codex_dir.glob("*.toml")}
    actual_claude = {path.stem for path in claude_dir.glob("*.md")}
    if actual_codex != expected_agents:
        errors.append(
            f"Codex agent inventory mismatch: expected {sorted(expected_agents)}, got {sorted(actual_codex)}"
        )
    if actual_claude != expected_agents:
        errors.append(
            f"Claude agent inventory mismatch: expected {sorted(expected_agents)}, got {sorted(actual_claude)}"
        )

    for entry in catalog.get("agents", []):
        agent_id = entry["id"]
        profile = profiles.get(entry.get("profile"), {})
        access = entry.get("access")
        codex_path = codex_dir / f"{agent_id}.toml"
        claude_path = claude_dir / f"{agent_id}.md"
        codex_description: str | None = None
        claude_description: str | None = None

        if codex_path.exists():
            try:
                codex = tomllib.loads(codex_path.read_text(encoding="utf-8"))
            except tomllib.TOMLDecodeError as exc:
                errors.append(f"{codex_path.relative_to(root)}: invalid TOML: {exc}")
                codex = {}
            for field in (*AGENT_REQUIRED_FIELDS, "developer_instructions", "model", "model_reasoning_effort", "sandbox_mode"):
                if not codex.get(field):
                    errors.append(f"{codex_path.relative_to(root)}: missing field {field!r}")
            if codex.get("name") != agent_id:
                errors.append(f"{codex_path.relative_to(root)}: mismatched role name")
            codex_description = codex.get("description")
            if codex.get("model") != profile.get("codex_model"):
                errors.append(f"{codex_path.relative_to(root)}: stale or incorrect Codex model")
            if codex.get("model_reasoning_effort") != entry.get("effort"):
                errors.append(f"{codex_path.relative_to(root)}: incorrect reasoning effort")
            expected_sandbox = "workspace-write" if access == "writer" else "read-only"
            if codex.get("sandbox_mode") != expected_sandbox:
                errors.append(f"{codex_path.relative_to(root)}: unsafe or incorrect sandbox mode")
            instructions = str(codex.get("developer_instructions", ""))
            _check_sections(errors, str(codex_path.relative_to(root)), instructions, required_sections)
            _check_unsafe_paths(errors, str(codex_path.relative_to(root)), codex_path.read_text(encoding="utf-8"))

        if claude_path.exists():
            try:
                metadata, body = parse_frontmatter(claude_path)
            except FrontmatterError as exc:
                errors.append(f"{claude_path.relative_to(root)}: {exc}")
                metadata, body = {}, ""
            for field in (*AGENT_REQUIRED_FIELDS, *CLAUDE_REQUIRED_FIELDS, "tools"):
                if not metadata.get(field):
                    errors.append(f"{claude_path.relative_to(root)}: missing field {field!r}")
            if metadata.get("name") != agent_id:
                errors.append(f"{claude_path.relative_to(root)}: mismatched role name")
            claude_description = metadata.get("description")
            if metadata.get("model") != profile.get("claude_model"):
                errors.append(f"{claude_path.relative_to(root)}: stale or incorrect Claude model")
            if metadata.get("effort") != entry.get("effort"):
                errors.append(f"{claude_path.relative_to(root)}: incorrect effort")
            tools = {tool.strip() for tool in metadata.get("tools", "").split(",") if tool.strip()}
            if access == "writer":
                if not {"Edit", "Write"}.issubset(tools):
                    errors.append(f"{claude_path.relative_to(root)}: writer lacks Edit and Write")
                if metadata.get("isolation") != "worktree":
                    errors.append(f"{claude_path.relative_to(root)}: writer must use worktree isolation")
                if metadata.get("permissionMode") == "bypassPermissions":
                    errors.append(f"{claude_path.relative_to(root)}: permission bypass is forbidden")
            else:
                if {"Edit", "Write"} & tools:
                    errors.append(f"{claude_path.relative_to(root)}: read-only agent has write tools")
                if metadata.get("permissionMode") != "plan":
                    errors.append(f"{claude_path.relative_to(root)}: read-only agent must use plan mode")
            _check_sections(errors, str(claude_path.relative_to(root)), body, required_sections)
            _check_unsafe_paths(errors, str(claude_path.relative_to(root)), claude_path.read_text(encoding="utf-8"))

        if codex_description and claude_description and codex_description != claude_description:
            errors.append(f"agent {agent_id!r}: descriptions differ between platforms")

    codex_skills_dir = root / "templates" / "codex" / ".agents" / "skills"
    claude_skills_dir = root / "templates" / "claude" / ".claude" / "skills"
    actual_codex_skills = {path.parent.name for path in codex_skills_dir.glob("*/SKILL.md")}
    actual_claude_skills = {path.parent.name for path in claude_skills_dir.glob("*/SKILL.md")}
    if actual_codex_skills != expected_workflows:
        errors.append("Codex workflow inventory mismatch")
    if actual_claude_skills != expected_workflows:
        errors.append("Claude workflow inventory mismatch")

    for workflow in sorted(expected_workflows):
        pairs: list[tuple[str, dict[str, str], str]] = []
        for platform, path in (
            ("Codex", codex_skills_dir / workflow / "SKILL.md"),
            ("Claude", claude_skills_dir / workflow / "SKILL.md"),
        ):
            if not path.exists():
                errors.append(f"{platform} workflow {workflow!r}: missing SKILL.md")
                continue
            try:
                metadata, body = parse_frontmatter(path)
            except FrontmatterError as exc:
                errors.append(f"{path.relative_to(root)}: {exc}")
                continue
            if metadata.get("name") != workflow:
                errors.append(f"{path.relative_to(root)}: workflow name mismatch")
            if not metadata.get("description"):
                errors.append(f"{path.relative_to(root)}: missing workflow description")
            _check_sections(errors, str(path.relative_to(root)), body, list(WORKFLOW_SECTIONS))
            _check_unsafe_paths(errors, str(path.relative_to(root)), path.read_text(encoding="utf-8"))
            pairs.append((platform, metadata, body))
        if len(pairs) == 2 and pairs[0][1].get("description") != pairs[1][1].get("description"):
            errors.append(f"workflow {workflow!r}: descriptions differ between platforms")
        if len(pairs) == 2 and pairs[0][2] != pairs[1][2]:
            errors.append(f"workflow {workflow!r}: instructions differ between platforms")

    eval_dir = root / "evals"
    actual_fixtures = {path.stem for path in eval_dir.glob("*.json")}
    expected_fixtures = set(catalog.get("evaluation_fixtures", []))
    if actual_fixtures != expected_fixtures:
        errors.append(
            f"evaluation fixture inventory mismatch: expected {sorted(expected_fixtures)}, got {sorted(actual_fixtures)}"
        )
    for fixture_id in sorted(expected_fixtures & actual_fixtures):
        path = eval_dir / f"{fixture_id}.json"
        try:
            fixture = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(root)}: invalid JSON: {exc}")
            continue
        for field in ("id", "workflow", "prompt", "expected_orchestration", "acceptance_checks", "failure_signals"):
            if not fixture.get(field):
                errors.append(f"{path.relative_to(root)}: missing fixture field {field!r}")
        if fixture.get("id") != fixture_id:
            errors.append(f"{path.relative_to(root)}: fixture id mismatch")
        if fixture.get("workflow") not in expected_workflows:
            errors.append(f"{path.relative_to(root)}: unknown workflow")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=SUITE_ROOT, help="Suite directory to validate")
    args = parser.parse_args(argv)
    errors = validate_suite(args.root.resolve())
    if errors:
        print(f"Agent suite validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    catalog = load_catalog(args.root.resolve())
    print(
        "Agent suite valid: "
        f"{len(catalog['agents'])} paired agents, "
        f"{len(catalog['workflows'])} paired workflows, "
        f"{len(catalog['evaluation_fixtures'])} evaluation fixtures."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
