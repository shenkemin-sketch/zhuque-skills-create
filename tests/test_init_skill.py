#!/usr/bin/env python3
"""Smoke-test the bundled official Codex initializer end to end."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InitSkillSmokeTest(unittest.TestCase):
    def test_initializer_creates_codex_metadata_and_validates_after_authoring(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            initialized = subprocess.run(
                [
                    "python3", str(ROOT / "scripts" / "init_skill.py"), "demo-workflow",
                    "--path", str(destination),
                    "--resources", "scripts,references",
                    "--interface", "display_name=Demo Workflow",
                    "--interface", "short_description=Create validated demo workflow skills",
                    "--interface", "default_prompt=Use $demo-workflow to package this repeated task.",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(initialized.returncode, 0, initialized.stderr or initialized.stdout)
            skill = destination / "demo-workflow"
            self.assertTrue((skill / "agents" / "openai.yaml").is_file())
            (skill / "SKILL.md").write_text(
                "---\n"
                "name: demo-workflow\n"
                "description: Create a reusable Codex skill from a repeated demo workflow. Use when the same demo task should be packaged and validated.\n"
                "---\n\n"
                "# Demo Workflow\n\nFollow the repeated workflow and verify its output.\n",
                encoding="utf-8",
            )
            quick = subprocess.run(
                ["python3", str(ROOT / "scripts" / "quick_validate.py"), str(skill)],
                capture_output=True,
                text=True,
                check=False,
            )
            extended = subprocess.run(
                ["python3", str(ROOT / "scripts" / "validate_skill.py"), str(skill)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(quick.returncode, 0, quick.stdout + quick.stderr)
            self.assertEqual(extended.returncode, 0, extended.stdout + extended.stderr)


if __name__ == "__main__":
    unittest.main()
