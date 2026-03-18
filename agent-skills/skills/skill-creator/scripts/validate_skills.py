#!/usr/bin/env python3

from __future__ import annotations

import argparse
import importlib
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SkillResult:
    path: Path
    errors: list[str]
    warnings: list[str]


@dataclass
class ValidatorBackend:
    module: object | None
    cli_available: bool
    mode: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate skills with a single command."
    )
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=None,
        help="Skills root directory (default: inferred from script location)",
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Skill name or skill path (repeatable)",
    )
    parser.add_argument(
        "--strict-lines",
        action="store_true",
        help="Treat SKILL.md > 500 lines as an error instead of a warning",
    )
    return parser.parse_args()


def infer_skills_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_targets(skills_root: Path, skill_args: list[str]) -> list[Path]:
    if not skill_args:
        targets: list[Path] = []
        for child in sorted(skills_root.iterdir()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            if (child / "SKILL.md").exists():
                targets.append(child)
        return targets

    resolved: list[Path] = []
    for raw in skill_args:
        raw_path = Path(raw)
        if raw_path.exists():
            resolved.append(raw_path.resolve())
            continue

        maybe = skills_root / raw
        if maybe.exists():
            resolved.append(maybe.resolve())
            continue

        resolved.append(maybe.resolve())
    return resolved


def load_validator_backend() -> ValidatorBackend:
    try:
        module = importlib.import_module("skills_ref.validator")
        return ValidatorBackend(module=module, cli_available=False, mode="skills_ref_module")
    except Exception:
        pass

    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[4]
    local_src = repo_root / "agentskills" / "skills-ref" / "src"
    if local_src.exists():
        sys.path.insert(0, str(local_src))
        try:
            module = importlib.import_module("skills_ref.validator")
            return ValidatorBackend(module=module, cli_available=False, mode="skills_ref_module")
        except Exception:
            pass

    if shutil.which("skills-ref"):
        return ValidatorBackend(module=None, cli_available=True, mode="skills_ref_cli")

    return ValidatorBackend(module=None, cli_available=False, mode="builtin")


def parse_frontmatter_basic(content: str) -> tuple[dict[str, object], str | None]:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "Missing opening frontmatter delimiter '---'"

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break

    if end_index is None:
        return {}, "Missing closing frontmatter delimiter '---'"

    frontmatter = lines[1:end_index]
    metadata: dict[str, object] = {}

    idx = 0
    while idx < len(frontmatter):
        raw = frontmatter[idx]
        if not raw.strip():
            idx += 1
            continue

        if raw.startswith(" "):
            return {}, f"Invalid frontmatter indentation at line: {raw}"

        match = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", raw)
        if not match:
            return {}, f"Invalid frontmatter line: {raw}"

        key = match.group(1)
        value = match.group(2)

        if value in {"|", ">", "|-", ">-", "|+", ">+"}:
            block_lines: list[str] = []
            idx += 1
            while idx < len(frontmatter):
                candidate = frontmatter[idx]
                if candidate.startswith("  ") or not candidate.strip():
                    block_lines.append(candidate[2:] if candidate.startswith("  ") else "")
                    idx += 1
                    continue
                break
            metadata[key] = "\n".join(block_lines).strip()
            continue

        if value == "":
            nested: dict[str, str] = {}
            idx += 1
            while idx < len(frontmatter):
                candidate = frontmatter[idx]
                if not candidate.strip():
                    idx += 1
                    continue
                if not candidate.startswith("  "):
                    break
                nested_match = re.match(r"^\s{2}([A-Za-z0-9_.-]+)\s*:\s*(.*)$", candidate)
                if not nested_match:
                    return {}, f"Invalid nested frontmatter line: {candidate}"
                nested_key = nested_match.group(1)
                nested_value = nested_match.group(2).strip().strip('"').strip("'")
                nested[nested_key] = nested_value
                idx += 1
            metadata[key] = nested
            continue

        metadata[key] = value.strip().strip('"').strip("'")
        idx += 1

    return metadata, None


def builtin_validate(skill_path: Path) -> list[str]:
    allowed_fields = {
        "name",
        "description",
        "license",
        "allowed-tools",
        "metadata",
        "compatibility",
    }

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return ["Missing required file: SKILL.md"]

    content = skill_md.read_text(encoding="utf-8")
    metadata, parse_error = parse_frontmatter_basic(content)
    if parse_error:
        return [parse_error]

    errors: list[str] = []

    extra_fields = set(metadata.keys()) - allowed_fields
    if extra_fields:
        errors.append(
            f"Unexpected fields in frontmatter: {', '.join(sorted(extra_fields))}."
        )

    name = metadata.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("Field 'name' must be a non-empty string")
    else:
        normalized = name.strip()
        if len(normalized) > 64:
            errors.append(f"Skill name '{normalized}' exceeds 64 character limit")
        if normalized != normalized.lower():
            errors.append(f"Skill name '{normalized}' must be lowercase")
        if normalized.startswith("-") or normalized.endswith("-"):
            errors.append("Skill name cannot start or end with a hyphen")
        if "--" in normalized:
            errors.append("Skill name cannot contain consecutive hyphens")
        if not all(char.isalnum() or char == "-" for char in normalized):
            errors.append(
                f"Skill name '{normalized}' contains invalid characters."
            )
        if skill_path.name != normalized:
            errors.append(
                f"Directory name '{skill_path.name}' must match skill name '{normalized}'"
            )

    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("Field 'description' must be a non-empty string")
    else:
        if len(description) > 1024:
            errors.append(
                f"Description exceeds 1024 character limit ({len(description)} chars)"
            )

    compatibility = metadata.get("compatibility")
    if compatibility is not None:
        if not isinstance(compatibility, str):
            errors.append("Field 'compatibility' must be a string")
        elif len(compatibility) > 500:
            errors.append(
                f"Compatibility exceeds 500 character limit ({len(compatibility)} chars)"
            )

    return errors


def run_validator(
    skill_path: Path,
    backend: ValidatorBackend,
) -> list[str]:
    if backend.module is not None:
        validate_func = getattr(backend.module, "validate")
        return list(validate_func(skill_path))

    if backend.cli_available:
        process = subprocess.run(
            ["skills-ref", "validate", str(skill_path)],
            capture_output=True,
            text=True,
        )
        if process.returncode == 0:
            return []

        stderr_lines = [line.strip() for line in process.stderr.splitlines() if line.strip()]
        if not stderr_lines:
            return [f"validation failed for {skill_path}"]

        cleaned: list[str] = []
        for line in stderr_lines:
            if line.startswith("Validation failed for"):
                continue
            cleaned.append(line.removeprefix("- ").removeprefix("• ").strip())
        return cleaned or stderr_lines

    return builtin_validate(skill_path)


def line_count_warning(skill_path: Path, strict_lines: bool) -> tuple[list[str], list[str]]:
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return ["Missing required file: SKILL.md"], []

    line_count = skill_md.read_text(encoding="utf-8").count("\n") + 1
    if line_count <= 500:
        return [], []

    message = f"SKILL.md has {line_count} lines (recommended <= 500)."
    if strict_lines:
        return [message], []
    return [], [message]


def main() -> int:
    args = parse_args()
    skills_root = (args.skills_root or infer_skills_root()).resolve()

    if not skills_root.exists() or not skills_root.is_dir():
        print(f"ERROR: skills root not found: {skills_root}")
        return 2

    targets = resolve_targets(skills_root, args.skill)
    if not targets:
        print(f"No skills found under: {skills_root}")
        return 0

    backend = load_validator_backend()
    print(f"Validator backend: {backend.mode}")

    results: list[SkillResult] = []
    for skill in targets:
        errors: list[str] = []
        warnings: list[str] = []

        if not skill.exists() or not skill.is_dir():
            errors.append("Skill directory not found")
            results.append(SkillResult(path=skill, errors=errors, warnings=warnings))
            continue

        errors.extend(run_validator(skill, backend))
        extra_errors, extra_warnings = line_count_warning(skill, args.strict_lines)
        errors.extend(extra_errors)
        warnings.extend(extra_warnings)

        results.append(SkillResult(path=skill, errors=errors, warnings=warnings))

    fail_count = 0
    warn_count = 0

    print(f"Skills root: {skills_root}")
    for result in results:
        relative = result.path.relative_to(skills_root) if result.path.is_relative_to(skills_root) else result.path
        if result.errors:
            fail_count += 1
            print(f"[FAIL] {relative}")
            for error in result.errors:
                print(f"  - {error}")
        else:
            print(f"[PASS] {relative}")

        if result.warnings:
            warn_count += 1
            for warning in result.warnings:
                print(f"  - WARN: {warning}")

    print()
    print(f"Summary: total={len(results)} fail={fail_count} warn={warn_count}")

    return 1 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())
