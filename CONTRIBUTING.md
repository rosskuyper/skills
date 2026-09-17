# Maintainer validation

Use [uv](https://docs.astral.sh/uv/getting-started/installation/) to run the repository-owned validator. If you use mise, `mise install` selects the uv version pinned in `mise.toml` (trust this checkout with `mise trust` if prompted).

```bash
# Validate every skill.
uv run --locked scripts/validate_skills.py

# Validate one skill.
uv run --locked scripts/validate_skills.py skills/engineering/implement
```

uv creates and caches an isolated environment automatically. Python requirements and PyYAML are declared in the script using PEP 723 metadata; `scripts/validate_skills.py.lock` locks resolved dependencies. No environment activation or manual pip install is needed.

The validator checks frontmatter, names, descriptions, non-empty instructions, and agreement between Claude and Codex invocation policies. It does not evaluate skill behavior or model costs.

After deliberately changing script dependencies, regenerate the lockfile and include it with the change:

```bash
uv lock --script scripts/validate_skills.py
```
