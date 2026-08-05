#!/usr/bin/env python3
"""Contract tests for Codex-native metadata and debranding boundaries."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_skill", ROOT / "scripts" / "validate_skill.py")
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("unable to load validate_skill.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class CodexContractTest(unittest.TestCase):
    def test_openai_yaml_matches_skill_name(self) -> None:
        frontmatter = VALIDATOR.parse_frontmatter((ROOT / "SKILL.md").read_text(encoding="utf-8"))
        openai = VALIDATOR.load_yaml(ROOT / "agents" / "openai.yaml")
        self.assertIn(f"${frontmatter['name']}", openai["interface"]["default_prompt"])
        self.assertNotIn("compatibility", openai)

    def test_no_legacy_interface_contract(self) -> None:
        self.assertFalse((ROOT / "agents" / "interface.yaml").exists())
        runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md")), *sorted((ROOT / "scripts").glob("*.py"))]
        )
        self.assertNotIn("agents/interface.yaml", runtime_text)

    def test_zhuque_identity_and_adaptation_are_explicit(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        manifest = VALIDATOR.load_json(ROOT / "manifest.json")
        self.assertIn("## 朱雀 AI Adaptation", skill)
        self.assertIn("keep`, `adapt`, `remove`, or `add", skill)
        self.assertIn("用 AI 享受工作，降低内耗，快乐生活", skill)
        self.assertEqual(manifest["owner"], "朱雀 AI")
        self.assertIn("价值层", readme)

    def test_retired_project_identity_is_absent(self) -> None:
        retired = "".join(chr(codepoint) for codepoint in (114, 101, 100, 98, 105, 114, 100))
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
                continue
            if path.suffix.lower() not in {".md", ".py", ".json", ".yaml", ".yml"}:
                continue
            self.assertNotIn(retired, path.read_text(encoding="utf-8").lower(), str(path))

    def test_personal_brand_tokens_are_confined_to_legal_notices(self) -> None:
        allowed = {Path("LICENSE"), Path("THIRD_PARTY_NOTICES.md")}
        forbidden = tuple(
            "".join(chr(codepoint) for codepoint in sequence)
            for sequence in (
                (21521, 38451, 20052, 26408),
                (20052, 21521, 38451),
                (118, 105, 115, 116, 97, 56),
                (113, 105, 97, 111, 109, 117, 46, 97, 105),
                (113, 105, 97, 111, 109, 117, 45, 112, 114, 111, 102, 105, 108, 101),
                (113, 105, 97, 111, 109, 117, 95, 114, 101, 119, 97, 114, 100, 95, 113, 114),
                (113, 105, 97, 111, 109, 117, 95, 119, 101, 99, 104, 97, 116),
                (106, 111, 101, 115, 101, 101, 115, 117, 110),
            )
        )
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.relative_to(ROOT) in allowed or ".git" in path.parts or "__pycache__" in path.parts:
                continue
            if path.suffix.lower() not in {".md", ".py", ".json", ".yaml", ".yml"}:
                continue
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text, f"{path.relative_to(ROOT)} contains personal brand token {token}")


if __name__ == "__main__":
    unittest.main()
