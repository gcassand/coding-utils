#!/usr/bin/env python3
"""Safely install selected development-agent-suite templates for a project or user."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

SUITE_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = SUITE_ROOT / "installer-manifest.json"
PLATFORMS = ("codex", "claude", "both")
SCOPES = ("project", "user")


@dataclass(frozen=True)
class InstallEntry:
    source: Path
    destination: Path
    conflict: str


def _safe_relative(value: str, label: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe {label} path in manifest: {value!r}")
    return path


def load_manifest() -> list[dict[str, object]]:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load installer manifest: {exc}") from exc
    if manifest.get("version") != 1 or not isinstance(manifest.get("files"), list):
        raise ValueError("installer manifest must contain version 1 and a files list")
    return manifest["files"]


def selected_platform(value: str | None, input_fn=input) -> str:
    if value:
        return value
    try:
        answer = input_fn("Install for [1] Codex, [2] Claude Code, or [3] both? ").strip().lower()
    except EOFError as exc:
        raise ValueError("choose --platform when standard input is unavailable") from exc
    aliases = {"1": "codex", "codex": "codex", "2": "claude", "claude": "claude", "claude-code": "claude", "3": "both", "both": "both"}
    if answer not in aliases:
        raise ValueError("choose codex, claude, or both")
    return aliases[answer]


def _destination_for_scope(destination: Path, scope: str) -> Path:
    if scope == "project":
        return destination
    if scope != "user":
        raise ValueError(f"unsupported installation scope: {scope!r}")
    if destination == Path("AGENTS.md"):
        return Path(".codex/AGENTS.md")
    if destination == Path("CLAUDE.md"):
        return Path(".claude/CLAUDE.md")
    return destination


def entries_for(platform: str, scope: str = "project") -> list[InstallEntry]:
    requested = {"codex", "claude"} if platform == "both" else {platform}
    entries: list[InstallEntry] = []
    for raw in load_manifest():
        if not isinstance(raw, dict):
            raise ValueError("installer manifest entries must be objects")
        source_value = raw.get("source")
        destination_value = raw.get("destination")
        platforms = raw.get("platforms")
        conflict = raw.get("conflict")
        if not isinstance(source_value, str) or not isinstance(destination_value, str):
            raise ValueError("installer manifest entries require source and destination")
        if not isinstance(platforms, list) or not requested.intersection(platforms):
            continue
        if conflict != "manual-merge":
            raise ValueError(f"unsupported conflict policy for {destination_value!r}")
        source = SUITE_ROOT / _safe_relative(source_value, "source")
        if not source.is_file():
            raise ValueError(f"manifest source does not exist: {source_value}")
        destination = _safe_relative(destination_value, "destination")
        entries.append(InstallEntry(source, _destination_for_scope(destination, scope), conflict))
    if not entries:
        raise ValueError(f"installer manifest has no files for {platform}")
    return entries


def plan_install(
    target: Path, platform: str, scope: str = "project"
) -> tuple[list[InstallEntry], list[InstallEntry], list[InstallEntry]]:
    create: list[InstallEntry] = []
    unchanged: list[InstallEntry] = []
    conflicts: list[InstallEntry] = []
    for entry in entries_for(platform, scope):
        destination = target / entry.destination
        if not destination.exists():
            create.append(entry)
        elif destination.is_file() and destination.read_bytes() == entry.source.read_bytes():
            unchanged.append(entry)
        else:
            conflicts.append(entry)
    return create, unchanged, conflicts


def _report(kind: str, entries: Iterable[InstallEntry], target: Path) -> None:
    for entry in entries:
        print(f"{kind:<9} {entry.destination}")
        if kind == "CONFLICT":
            print(f"          Keep {target / entry.destination}; manually merge from {entry.source}")


def install(target: Path, platform: str, dry_run: bool = False, scope: str = "project") -> int:
    create, unchanged, conflicts = plan_install(target, platform, scope)
    _report("CREATE", create, target)
    _report("UNCHANGED", unchanged, target)
    _report("CONFLICT", conflicts, target)
    if conflicts:
        print("No files were copied: resolve every conflict and rerun.", file=sys.stderr)
        return 1
    if dry_run:
        print("Dry run complete: no files were copied.")
        return 0
    for entry in create:
        destination = target / entry.destination
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(entry.source, destination)
    print(
        f"Installed {len(create)} file(s) for {platform} at {scope} scope; "
        f"{len(unchanged)} already matched."
    )
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", choices=PLATFORMS, help="Install Codex, Claude Code, or both.")
    parser.add_argument(
        "--scope",
        choices=SCOPES,
        default="project",
        help="Installation scope (default: project).",
    )
    parser.add_argument(
        "--target",
        type=Path,
        help="Existing installation root (default: current directory for project scope, home directory for user scope).",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show actions without copying files.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        platform = selected_platform(args.platform)
        target = (args.target or (Path.home() if args.scope == "user" else Path.cwd())).resolve()
        if not target.is_dir():
            raise ValueError(f"target must be an existing directory: {target}")
        return install(target, platform, args.dry_run, args.scope)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
