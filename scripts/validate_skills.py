# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6,<7"]
# ///
"""Validate skill metadata and invocation policy using this repository's conventions."""

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_mapping(text):
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("expected a YAML mapping")
    return data


def validate_skill(path):
    errors = []
    try:
        content = (path / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
        if not match:
            return ["SKILL.md must start with YAML frontmatter"]
        metadata = load_mapping(match[1])
        name = metadata.get("name")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append("name must use lowercase letters, numbers, and single hyphens")
        elif len(name) > 64 or name != path.name:
            errors.append("name must match its directory and be at most 64 characters")
        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append("description must be a non-empty string")
        elif len(description) > 1024:
            errors.append("description must be at most 1024 characters")
        if not content[match.end():].strip():
            errors.append("skill instructions must not be empty")
        explicit = metadata.get("disable-model-invocation", False)
        if type(explicit) is not bool:
            errors.append("disable-model-invocation must be a boolean")
        config = load_mapping((path / "agents/openai.yaml").read_text(encoding="utf-8"))
        policy = config.get("policy", {})
        if not isinstance(policy, dict):
            errors.append("agents/openai.yaml policy must be a mapping")
        else:
            implicit = policy.get("allow_implicit_invocation", True)
            if type(implicit) is not bool or implicit is not (not explicit):
                errors.append("invocation policy must agree between SKILL.md and agents/openai.yaml")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(str(exc))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="*", type=Path, help="Skill directories; defaults to all repository skills")
    args = parser.parse_args()
    paths = args.skills or sorted(
        path.parent for bucket in ("engineering", "productivity")
        for path in (ROOT / "skills" / bucket).glob("*/SKILL.md")
    )
    if not paths:
        parser.error("no skills found")
    failed = 0
    for path in paths:
        errors = validate_skill(path)
        if errors:
            failed += 1
            for error in errors:
                print(f"FAIL {path}: {error}")
    print(f"Validated {len(paths)} skill(s): {len(paths) - failed} passed, {failed} failed.")
    return bool(failed)


if __name__ == "__main__":
    raise SystemExit(main())
