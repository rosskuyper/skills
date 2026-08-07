Skills are organized into bucket folders under `skills/`:

- `engineering/` — daily code work
- `productivity/` — daily non-code workflow tools

Every skill in `engineering/` or `productivity/` must have a reference in the top-level `README.md`.

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`. Both the bucket `README.md`s and the top-level `README.md` group entries into **User-invoked** and **Model-invoked**.

Every `SKILL.md` is either user-invoked (`disable-model-invocation: true` plus `policy.allow_implicit_invocation: false` in `agents/openai.yaml`, reachable only by the human) or model-invoked (model- or user-reachable). See [.agents/invocation.md](./.agents/invocation.md).

Consumers install with `npx skills@latest add rosskuyper/skills`, which copies the skill files they pick into their own repo. That is the documented route and the only one `README.md` should describe — there is no plugin manifest and no published npm package.

`owner/repo` is GitHub shorthand that the [`skills` CLI](https://www.npmjs.com/package/skills) resolves directly against GitHub, so **this repo does not need to be listed on skills.sh** for that command to work; skills.sh is a discovery directory (`npx skills find`), not a gate. Don't add a `skills.sh/b/...` badge — for an unlisted repo it renders the text "resource not found" rather than failing visibly. The CLI honours `GITHUB_TOKEN`/`GH_TOKEN`, so the command also works while this repo is private.

For working on *this* repo, `scripts/link-skills.sh` symlinks every skill into the local harness skill directories (`~/.claude/skills`, `~/.agents/skills`) so edits take effect without reinstalling. It is a maintainer-only script; don't document it as an installer. Re-run it after adding, removing, or renaming a skill.

This repo is derived from [mattpocock/skills](https://github.com/mattpocock/skills) under the MIT license. `LICENSE` retains the upstream copyright notice alongside ours — keep it there. Don't reintroduce upstream branding (aihero.dev links, newsletter CTAs, `mattpocock/skills` install commands, or first-person claims to have authored the skills).
