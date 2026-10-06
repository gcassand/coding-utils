from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path
import sys

SUITE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SUITE_ROOT / "tools"))

from install_agent_suite import install, main, selected_platform
from validate_agent_suite import validate_suite


class AgentSuiteValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.suite = Path(self.temp_dir.name) / "suite"
        shutil.copytree(SUITE_ROOT, self.suite, ignore=shutil.ignore_patterns("__pycache__"))
        self.target = Path(self.temp_dir.name) / "target"
        self.target.mkdir()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _replace(self, relative: str, old: str, new: str) -> None:
        path = self.suite / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, f"test mutation target not found in {relative}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def test_packaged_suite_is_valid(self) -> None:
        self.assertEqual(validate_suite(self.suite), [])

    def test_missing_required_field_is_rejected(self) -> None:
        self._replace(
            "templates/codex/.codex/agents/product-owner.toml",
            'description = "Turns a product problem into a decision-ready outcome brief or PRD; use before design or implementation when scope and acceptance are not yet stable."\n',
            "",
        )
        self.assertTrue(any("missing field 'description'" in error for error in validate_suite(self.suite)))

    def test_mismatched_role_is_rejected(self) -> None:
        self._replace(
            "templates/claude/.claude/agents/product-owner.md",
            "name: product-owner",
            "name: product-owner-mismatch",
        )
        self.assertTrue(any("mismatched role name" in error for error in validate_suite(self.suite)))

    def test_unsafe_writer_permission_is_rejected(self) -> None:
        self._replace(
            "templates/codex/.codex/agents/product-owner.toml",
            'sandbox_mode = "read-only"',
            'sandbox_mode = "workspace-write"',
        )
        self.assertTrue(any("unsafe or incorrect sandbox mode" in error for error in validate_suite(self.suite)))

    def test_stale_model_mapping_is_rejected(self) -> None:
        self._replace(
            "templates/claude/.claude/agents/security-specialist.md",
            "model: claude-opus-5",
            "model: claude-sonnet-5",
        )
        self.assertTrue(any("stale or incorrect Claude model" in error for error in validate_suite(self.suite)))

    def test_stale_codex_model_mapping_is_rejected(self) -> None:
        self._replace(
            "templates/codex/.codex/agents/codebase-explorer.toml",
            'model = "gpt-6-luna"',
            'model = "gpt-5.6-luna"',
        )
        self.assertTrue(any("stale or incorrect Codex model" in error for error in validate_suite(self.suite)))

    def test_codex_effort_is_independent_of_claude_effort(self) -> None:
        # Changing the Codex adapter must not alter the retained Claude effort pin.
        self._replace(
            "templates/codex/.codex/agents/software-architect.toml",
            'model_reasoning_effort = "low"',
            'model_reasoning_effort = "xhigh"',
        )
        errors = validate_suite(self.suite)
        self.assertTrue(any("incorrect reasoning effort" in error for error in errors))
        self.assertFalse(any("incorrect effort" in error for error in errors))

    def test_absent_workflow_counterpart_is_rejected(self) -> None:
        (self.suite / "templates/claude/.claude/skills/fix-bug/SKILL.md").unlink()
        errors = validate_suite(self.suite)
        self.assertTrue(any("Claude workflow inventory mismatch" in error for error in errors))
        self.assertTrue(any("missing SKILL.md" in error for error in errors))

    def test_manifest_drift_is_rejected(self) -> None:
        self._replace(
            "installer-manifest.json",
            '"destination": "AGENTS.md"',
            '"destination": "unexpected.md"',
        )
        self.assertTrue(any("allowlist does not match" in error for error in validate_suite(self.suite)))

    def test_codex_install_creates_only_codex_files(self) -> None:
        self.assertEqual(install(self.target, "codex"), 0)
        self.assertTrue((self.target / "AGENTS.md").is_file())
        self.assertTrue((self.target / ".codex/agents/product-owner.toml").is_file())
        self.assertTrue((self.target / ".codex/agents/project-bootstrapper.toml").is_file())
        self.assertTrue((self.target / ".agents/skills/bootstrap-project/SKILL.md").is_file())
        self.assertTrue((self.target / ".agents/skills/fix-bug/SKILL.md").is_file())
        self.assertFalse((self.target / "CLAUDE.md").exists())
        self.assertFalse((self.target / ".claude").exists())

    def test_claude_install_creates_only_claude_files(self) -> None:
        self.assertEqual(install(self.target, "claude"), 0)
        self.assertTrue((self.target / "CLAUDE.md").is_file())
        self.assertTrue((self.target / ".claude/agents/product-owner.md").is_file())
        self.assertTrue((self.target / ".claude/agents/project-bootstrapper.md").is_file())
        self.assertTrue((self.target / ".claude/skills/bootstrap-project/SKILL.md").is_file())
        self.assertTrue((self.target / ".claude/skills/fix-bug/SKILL.md").is_file())
        self.assertFalse((self.target / "AGENTS.md").exists())
        self.assertFalse((self.target / ".codex").exists())

    def test_both_install_and_rerun_are_safe(self) -> None:
        self.assertEqual(install(self.target, "both"), 0)
        self.assertTrue((self.target / "AGENTS.md").is_file())
        self.assertTrue((self.target / "CLAUDE.md").is_file())
        self.assertEqual(install(self.target, "both"), 0)

    def test_user_install_uses_platform_user_directories(self) -> None:
        self.assertEqual(install(self.target, "both", scope="user"), 0)
        self.assertTrue((self.target / ".codex/AGENTS.md").is_file())
        self.assertTrue((self.target / ".codex/config.toml").is_file())
        self.assertTrue((self.target / ".codex/agents/product-owner.toml").is_file())
        self.assertTrue((self.target / ".codex/agents/project-bootstrapper.toml").is_file())
        self.assertTrue((self.target / ".agents/skills/bootstrap-project/SKILL.md").is_file())
        self.assertTrue((self.target / ".agents/skills/fix-bug/SKILL.md").is_file())
        self.assertTrue((self.target / ".claude/CLAUDE.md").is_file())
        self.assertTrue((self.target / ".claude/agents/product-owner.md").is_file())
        self.assertTrue((self.target / ".claude/agents/project-bootstrapper.md").is_file())
        self.assertTrue((self.target / ".claude/skills/bootstrap-project/SKILL.md").is_file())
        self.assertTrue((self.target / ".claude/skills/fix-bug/SKILL.md").is_file())
        self.assertFalse((self.target / "AGENTS.md").exists())
        self.assertFalse((self.target / "CLAUDE.md").exists())

    def test_user_scope_cli_accepts_an_alternate_home(self) -> None:
        self.assertEqual(
            main(["--platform", "codex", "--scope", "user", "--target", str(self.target)]),
            0,
        )
        self.assertTrue((self.target / ".codex/AGENTS.md").is_file())

    def test_user_scope_conflict_blocks_every_copy(self) -> None:
        (self.target / ".codex").mkdir()
        (self.target / ".codex/AGENTS.md").write_text("user-owned instructions\n", encoding="utf-8")
        self.assertEqual(install(self.target, "codex", scope="user"), 1)
        self.assertFalse((self.target / ".codex/agents").exists())
        self.assertFalse((self.target / ".agents").exists())

    def test_dry_run_does_not_mutate_target(self) -> None:
        self.assertEqual(install(self.target, "codex", dry_run=True), 0)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_conflict_blocks_every_copy(self) -> None:
        (self.target / "AGENTS.md").write_text("user-owned instructions\n", encoding="utf-8")
        self.assertEqual(install(self.target, "codex"), 1)
        self.assertFalse((self.target / ".codex").exists())

    def test_interactive_platform_selection(self) -> None:
        self.assertEqual(selected_platform(None, lambda _: "2"), "claude")
        self.assertEqual(selected_platform(None, lambda _: "both"), "both")

    def test_missing_target_is_rejected(self) -> None:
        self.assertEqual(main(["--platform", "codex", "--target", str(self.target / "missing")]), 2)

    def test_invalid_platform_is_rejected_by_parser(self) -> None:
        with self.assertRaises(SystemExit):
            main(["--platform", "invalid"])


if __name__ == "__main__":
    unittest.main()
