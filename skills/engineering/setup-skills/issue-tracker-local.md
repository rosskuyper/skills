# Issue tracker: Local Markdown

Issues and specs for this repo live as markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The spec is `.scratch/<feature-slug>/spec.md`
- Implementation issues are one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` — never a single combined tickets file
- Triage state is recorded as a `Status:` line near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/` (creating the directory if needed).

## When a skill says "publish a spec"

Write the whole spec to `.scratch/<feature-slug>/spec.md`, every section a heading in the one file. There is no project-shaped container here, so the spec is not split across files — the tickets `/to-tickets` produces sit alongside it under `.scratch/<feature-slug>/issues/`.

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## When a skill says "resolve the work list"

Turn a reference into the ordered list of issues to actually work:

- **A `.scratch/<feature-slug>/` directory** → every file under its `issues/`, in number order. The directory and its `spec.md` are containers, never units of work.
- **A single issue file** → that file alone.
- **A `spec.md` with no `issues/` beside it** → nothing; it hasn't been broken down yet.

An issue is on the **frontier** when its own `Status:` is not `done` and every ticket in its `Blocked by:` line is `done`.

## When a skill says "start a ticket"

Set the file's `Status:` line to `in-progress` and save before the first edit; set it to `done` once the work is reviewed and committed. These two sit alongside the triage roles in `triage-labels.md` rather than replacing them — a ticket carries whichever describes it now.

## When a skill says "fetch the spec"

Read `.scratch/<feature-slug>/spec.md`, or the path the user passed.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a file with one **child** file per ticket.

- **Map**: `.scratch/<effort>/map.md` — the Notes / Decisions-so-far / Fog body.
- **Child ticket**: `.scratch/<effort>/issues/NN-<slug>.md`, numbered from `01`, with the question in the body. A `Type:` line records the ticket type (`research`/`prototype`/`grilling`/`task`); a `Status:` line records `claimed`/`resolved`.
- **Blocking**: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- **Frontier**: scan `.scratch/<effort>/issues/` for files that are open, unblocked, and unclaimed; first by number wins.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, then append a context pointer (gist + link) to the map's Decisions-so-far in `map.md`.
