#!/usr/bin/env python3
"""Ensure prior-art research and publishing remain self-contained."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_DOCS = (
    ROOT / "SKILL.md",
    ROOT / "README.md",
    ROOT / "references" / "prior-art-research.md",
    ROOT / "references" / "skill-engineering-method.md",
    ROOT / "agents" / "openai.yaml",
)
FORBIDDEN = (
    ".agents/skills/find-skills/SKILL.md",
    "npx skills add https://github.com/vercel-labs/skills --skill find-skills",
)


class BuiltInCapabilitiesTest(unittest.TestCase):
    def test_no_external_discovery_skill_dependency(self) -> None:
        for path in ACTIVE_DOCS:
            text = path.read_text(encoding="utf-8").replace("$HOME/", "").replace("~/", "")
            for forbidden in FORBIDDEN:
                self.assertNotIn(forbidden, text, f"{path} contains {forbidden}")

    def test_prior_art_research_is_bundled(self) -> None:
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("scripts/research_prior_art.py", skill_text)
        self.assertIn("skills.sh", skill_text)
        self.assertIn("SkillsMP", skill_text)
        self.assertTrue((ROOT / "scripts" / "search_skillsmp.py").is_file())

    def test_publishing_is_bundled_but_explicit(self) -> None:
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("scripts/publish_skill.py", skill_text)
        self.assertIn("explicit", skill_text)
        self.assertTrue((ROOT / "scripts" / "publish_skill.py").is_file())


if __name__ == "__main__":
    unittest.main()
