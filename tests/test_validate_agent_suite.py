from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_agent_suite import REPO_ROOT, validate_suite


class AgentSuiteValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for relative in (
            ".agents",
            ".claude",
            ".codex",
            "development-agent-suite",
        ):
            source = REPO_ROOT / relative
            destination = self.root / relative
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _replace(self, relative: str, old: str, new: str) -> None:
        path = self.root / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, f"test mutation target not found in {relative}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def test_repository_suite_is_valid(self) -> None:
        self.assertEqual(validate_suite(self.root), [])

    def test_missing_required_field_is_rejected(self) -> None:
        self._replace(
            ".codex/agents/product-owner.toml",
            'description = "Turns a product problem into a decision-ready outcome brief or PRD; use before design or implementation when scope and acceptance are not yet stable."\n',
            "",
        )
        self.assertTrue(any("missing field 'description'" in error for error in validate_suite(self.root)))

    def test_mismatched_role_is_rejected(self) -> None:
        self._replace(
            ".claude/agents/product-owner.md",
            "name: product-owner",
            "name: product-owner-mismatch",
        )
        self.assertTrue(any("mismatched role name" in error for error in validate_suite(self.root)))

    def test_unsafe_writer_permission_is_rejected(self) -> None:
        self._replace(
            ".codex/agents/product-owner.toml",
            'sandbox_mode = "read-only"',
            'sandbox_mode = "workspace-write"',
        )
        self.assertTrue(any("unsafe or incorrect sandbox mode" in error for error in validate_suite(self.root)))

    def test_stale_model_mapping_is_rejected(self) -> None:
        self._replace(
            ".claude/agents/security-specialist.md",
            "model: claude-opus-5",
            "model: claude-sonnet-5",
        )
        self.assertTrue(any("stale or incorrect Claude model" in error for error in validate_suite(self.root)))

    def test_absent_workflow_counterpart_is_rejected(self) -> None:
        (self.root / ".claude/skills/fix-bug/SKILL.md").unlink()
        errors = validate_suite(self.root)
        self.assertTrue(any("Claude workflow inventory mismatch" in error for error in errors))
        self.assertTrue(any("missing SKILL.md" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

