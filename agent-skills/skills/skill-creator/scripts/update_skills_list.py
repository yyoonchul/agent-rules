#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate and refresh skills list markdown."
    )
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=None,
        help="Skills root directory (default: inferred from script location)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output markdown path (default: <skills-root>/SKILLS.md)",
    )
    return parser.parse_args()


def infer_skills_root() -> Path:
    return Path(__file__).resolve().parents[2]


def extract_frontmatter(text: str) -> str | None:
    match = re.search(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return None
    return match.group(1)


def extract_field(frontmatter: str, key: str) -> str:
    lines = frontmatter.splitlines()
    pattern = re.compile(rf"^{re.escape(key)}\s*:\s*(.*)$")

    for index, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue

        value = match.group(1).strip()
        if value in {"|", ">", "|-", ">-", "|+", ">+"}:
            block_lines: list[str] = []
            for next_line in lines[index + 1 :]:
                if next_line.startswith("  ") or next_line == "":
                    block_lines.append(next_line[2:] if next_line.startswith("  ") else "")
                else:
                    break
            return " ".join(part.strip() for part in block_lines if part.strip()).strip()

        return value.strip().strip('"').strip("'")

    return ""


def summarize(description: str, max_len: int = 180) -> str:
    condensed = " ".join(description.split())
    if len(condensed) <= max_len:
        return condensed
    return condensed[: max_len - 1].rstrip() + "…"


def collect_skills(skills_root: Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []

    for child in sorted(skills_root.iterdir(), key=lambda path: path.name):
        if not child.is_dir() or child.name.startswith("."):
            continue

        skill_md = child / "SKILL.md"
        if not skill_md.exists():
            continue

        text = skill_md.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(text)
        if frontmatter is None:
            continue

        name = extract_field(frontmatter, "name") or child.name
        description = extract_field(frontmatter, "description")

        entries.append(
            {
                "name": name,
                "summary": summarize(description) if description else "(description 없음)",
                "path": f"agent-skills/skills/{child.name}/SKILL.md",
            }
        )

    return entries


def render_markdown(entries: list[dict[str, str]]) -> str:
    lines: list[str] = []
    lines.append("# 통합 스킬 목록")
    lines.append("")
    lines.append("이 문서는 `agent-skills/skills` 기준 스킬 목록입니다.")
    lines.append("`skill-creator/scripts/update_skills_list.py`로 자동 생성/갱신됩니다.")
    lines.append("")
    lines.append("| 스킬 이름 | 역할 요약 | 경로 |")
    lines.append("| --- | --- | --- |")

    for entry in entries:
        name = f"`{entry['name']}`"
        summary = entry["summary"].replace("|", "\\|")
        path = f"`{entry['path']}`"
        lines.append(f"| {name} | {summary} | {path} |")

    lines.append("")
    lines.append("## 갱신 명령")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 agent-skills/skills/skill-creator/scripts/update_skills_list.py")
    lines.append("```")

    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    skills_root = (args.skills_root or infer_skills_root()).resolve()
    output = (args.output or (skills_root / "SKILLS.md")).resolve()

    if not skills_root.exists() or not skills_root.is_dir():
        print(f"ERROR: skills root not found: {skills_root}")
        return 2

    entries = collect_skills(skills_root)
    markdown = render_markdown(entries)
    output.write_text(markdown, encoding="utf-8")

    print(f"Updated: {output}")
    print(f"Skills: {len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
