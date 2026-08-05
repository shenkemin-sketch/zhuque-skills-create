#!/usr/bin/env python3
"""Validate a Codex-native skill package and optional distribution evidence."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


REQUIRED_FRONTMATTER = ("name", "description")
ALLOWED_FRONTMATTER = {"name", "description", "license", "allowed-tools", "metadata"}
REQUIRED_OPENAI_FIELDS = ("display_name", "short_description")
REQUIRED_MANIFEST_FIELDS = ("name", "version", "owner", "updated_at", "status", "maturity_tier")
IGNORED_DISCOVERY_DIRS = {".git", "dist", "node_modules", "__pycache__"}
EVIDENCE_TIERS = {"production", "library", "governed"}
MAX_PRODUCTION_SKILL_BYTES = 14_000
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected JSON object")
    return payload


def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        return {}
    try:
        payload = yaml.safe_load(read_text(path)) or {}
    except Exception as exc:
        raise ValueError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return payload


def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    lines = text.splitlines()
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}
    payload = "\n".join(lines[1:end])
    if yaml is not None:
        loaded = yaml.safe_load(payload) or {}
        return loaded if isinstance(loaded, dict) else {}
    data: dict[str, Any] = {}
    for line in payload.splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip("'\"|")
    return data


def markdown_links(text: str) -> list[str]:
    return re.findall(r"\]\(([^)]+\.md)\)", text)


def discover_skill_entrypoints(root: Path) -> list[Path]:
    """Return exact SKILL.md entrypoints an installer could expose recursively."""
    entries: list[Path] = []
    for path in root.rglob("SKILL.md"):
        relative = path.relative_to(root)
        if any(part in IGNORED_DISCOVERY_DIRS for part in relative.parts):
            continue
        entries.append(relative)
    return sorted(entries)


def validate_evidence_reports(
    root: Path,
    manifest: dict[str, Any],
    failures: list[str],
    warnings: list[str],
) -> None:
    tier = str(manifest.get("maturity_tier", "")).lower()
    if tier not in EVIDENCE_TIERS:
        return
    for relative in (
        "reports/skill-ir.json",
        "reports/trigger-eval.json",
        "reports/prior-art-research.md",
        "reports/creation-handoff.md",
    ):
        if not (root / relative).is_file():
            failures.append(f"{tier} distribution project missing evidence artifact: {relative}")

    ir_path = root / "reports/skill-ir.json"
    if ir_path.is_file():
        try:
            package = load_json(ir_path).get("package", {})
        except ValueError as exc:
            failures.append(str(exc))
            package = {}
        if package.get("name") != manifest.get("name"):
            failures.append("reports/skill-ir.json package.name does not match manifest.json")
        if package.get("version") != manifest.get("version"):
            failures.append("reports/skill-ir.json package.version does not match manifest.json")

    trigger_path = root / "reports/trigger-eval.json"
    if trigger_path.is_file():
        try:
            trigger = load_json(trigger_path)
        except ValueError as exc:
            failures.append(str(exc))
            trigger = {}
        summary = trigger.get("summary", {})
        total = summary.get("total") if isinstance(summary, dict) else None
        passed = summary.get("passed") if isinstance(summary, dict) else None
        if trigger.get("ok") is not True or not isinstance(total, int) or total <= 0 or passed != total:
            failures.append("reports/trigger-eval.json is incomplete or failing")

    handoff_path = root / "reports/creation-handoff.md"
    if handoff_path.is_file() and str(manifest.get("version")) not in read_text(handoff_path):
        warnings.append("reports/creation-handoff.md may not mention the current manifest version")


def validate(root: Path) -> dict[str, Any]:
    root = root.expanduser().resolve()
    failures: list[str] = []
    warnings: list[str] = []
    manifest: dict[str, Any] = {}
    frontmatter: dict[str, Any] = {}
    skill_bytes = 0

    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        failures.append("missing required file: SKILL.md")

    entrypoints = discover_skill_entrypoints(root)
    nested = [path for path in entrypoints if path != Path("SKILL.md")]
    if nested:
        failures.append(
            "nested discoverable skill entrypoints found: "
            + ", ".join(map(str, nested))
            + "; rename examples to SKILL.example.md and fixtures to SKILL.fixture.md"
        )

    if skill_path.is_file():
        skill_text = read_text(skill_path)
        skill_bytes = len(skill_text.encode("utf-8"))
        frontmatter = parse_frontmatter(skill_text)
        for field in REQUIRED_FRONTMATTER:
            if not frontmatter.get(field):
                failures.append(f"SKILL.md missing frontmatter field: {field}")
        unknown = sorted(set(frontmatter) - ALLOWED_FRONTMATTER)
        if unknown:
            failures.append("SKILL.md contains unsupported frontmatter fields: " + ", ".join(unknown))
        name = str(frontmatter.get("name", ""))
        description = str(frontmatter.get("description", ""))
        if name and (len(name) > 64 or not NAME_PATTERN.fullmatch(name)):
            failures.append("SKILL.md name must be lowercase hyphen-case and no longer than 64 characters")
        if description and len(description) > 1024:
            failures.append("SKILL.md description exceeds 1024 characters")
        if "<" in description or ">" in description:
            failures.append("SKILL.md description may not contain angle brackets")
        for relative in markdown_links(skill_text):
            if not (root / relative).exists():
                failures.append(f"SKILL.md links to missing reference: {relative}")

    openai_path = root / "agents" / "openai.yaml"
    if openai_path.is_file():
        try:
            openai = load_yaml(openai_path)
        except ValueError as exc:
            failures.append(str(exc))
            openai = {}
        interface = openai.get("interface", {}) if isinstance(openai, dict) else {}
        for field in REQUIRED_OPENAI_FIELDS:
            if not isinstance(interface, dict) or not str(interface.get(field, "")).strip():
                failures.append(f"agents/openai.yaml missing interface.{field}")
        short = str(interface.get("short_description", "")) if isinstance(interface, dict) else ""
        if short and not 25 <= len(short) <= 64:
            failures.append("agents/openai.yaml interface.short_description must be 25-64 characters")
        prompt = str(interface.get("default_prompt", "")) if isinstance(interface, dict) else ""
        name = str(frontmatter.get("name", ""))
        if prompt and name and f"${name}" not in prompt:
            failures.append("agents/openai.yaml interface.default_prompt must mention the skill as $<skill-name>")
    else:
        warnings.append("agents/openai.yaml missing; recommended for Codex UI metadata")

    manifest_path = root / "manifest.json"
    if manifest_path.is_file():
        try:
            manifest = load_json(manifest_path)
        except ValueError as exc:
            failures.append(str(exc))
            manifest = {}
        for field in REQUIRED_MANIFEST_FIELDS:
            if not manifest.get(field):
                failures.append(f"manifest.json missing field: {field}")
        if manifest.get("name") and manifest.get("name") != frontmatter.get("name"):
            failures.append("manifest.json name does not match SKILL.md")
        if manifest.get("version") and not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest["version"])):
            failures.append("manifest.json version must be semantic X.Y.Z")
        if manifest.get("context_budget_tier") == "production" and skill_bytes > MAX_PRODUCTION_SKILL_BYTES:
            warnings.append(
                f"SKILL.md exceeds production context budget: {skill_bytes} > {MAX_PRODUCTION_SKILL_BYTES} bytes"
            )

    validate_evidence_reports(root, manifest, failures, warnings)

    cases_path = root / "evals" / "trigger_cases.json"
    if cases_path.is_file():
        try:
            cases = load_json(cases_path)
        except ValueError as exc:
            failures.append(str(exc))
            cases = {}
        for bucket in ("should_trigger", "should_not_trigger", "near_neighbor"):
            if not cases.get(bucket):
                warnings.append(f"evals/trigger_cases.json has no {bucket} cases")
    elif manifest.get("maturity_tier") in EVIDENCE_TIERS:
        warnings.append("evals/trigger_cases.json missing for a production-or-higher distribution project")

    scripts_dir = root / "scripts"
    if scripts_dir.is_dir():
        for script in sorted(scripts_dir.glob("*.py")):
            text = read_text(script)
            if "argparse" not in text and "sys.argv" not in text and 'SCRIPT_INTERFACE = "internal-module"' not in text:
                warnings.append(f"script has no argparse help or internal-module marker: {script.name}")

    return {"ok": not failures, "root": str(root), "failures": failures, "warnings": warnings}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Codex-native skill package.")
    parser.add_argument("skill_dir", nargs="?", default=".", help="Skill directory to validate.")
    args = parser.parse_args()
    result = validate(Path(args.skill_dir))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
