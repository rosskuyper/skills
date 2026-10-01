# Issue tracker: Local Markdown

Specs and tickets for this repo live as markdown files under `docs/specs/`. They are committed repo history, like ADRs: never throwaway, never moved once written.

## Conventions

- One feature per directory: `docs/specs/<YYYY-MM-DD>-<feature-slug>/`. The date is the day the folder is created, ISO format. There is no global counter, because parallel branches would collide silently. If the same date and slug already exist, pick a more specific slug.
- The spec is `docs/specs/<YYYY-MM-DD>-<feature-slug>/spec.md`, every section in the one file
- Tickets are one file each at `docs/specs/<YYYY-MM-DD>-<feature-slug>/tickets/<NN>-<slug>.md`, numbered per feature from `01` — never a single combined tickets file
- **References are always by path**: `docs/specs/2026-10-01-billing-webhooks/tickets/02-retry-queue.md`. In prose the short form `2026-10-01-billing-webhooks/02` is fine. Never a bare number.
- Finished features stay where they are. The `Status:` line is the lifecycle; there is no archive or move step.
- Comments and conversation history append to the bottom of the file under a `## Comments` heading
- Ticket-file edits commit with the ticket's code. The `in-progress` flip is included in the ticket's commit; `done` and ticked checkboxes go in the same commit as the reviewed code, or a trailing commit on the same branch if the code commit was already made.
- `.scratch/` is gitignored and holds only throwaway state, such as `/implement`'s run ledger at `.scratch/implement/<feature-slug>.md`. Nothing committed lives there.

### Status vocabulary

Every ticket file carries one `Status:` line: a triage role from `triage-labels.md` (default `ready-for-agent`), then `in-progress`, then `done`. The last two sit alongside the triage roles rather than replacing them — a ticket carries whichever describes it now.

`spec.md` carries its own `Status:` line under the title: `ready` (published, not started), `in-progress` (first ticket started), `done` (all tickets done).

### Ticket header

In this order: title, `Status:`, `Wave:`, `Blocked by:`, and for wayfinder tickets `Type:`. `Blocked by:` lists ticket numbers within the same feature and cross-feature blockers by path; omit it or write `none` when unblocked. Then a blank line and the body.

```md
# 02 — Retry queue

Status: ready-for-agent
Wave: 1
Blocked by: 01, docs/specs/2026-09-14-event-bus/tickets/03-outbox.md

## What to build

...

## Acceptance criteria

- [ ] ...
```

## When a skill says "publish to the issue tracker"

Create a new file under `docs/specs/<YYYY-MM-DD>-<feature-slug>/tickets/` (creating the directories if needed), numbered after the highest existing ticket.

## When a skill says "publish a spec"

Write the whole spec to `docs/specs/<YYYY-MM-DD>-<feature-slug>/spec.md`, `# <Title>` then `Status: ready`, every section a heading in the one file. There is no project-shaped container here, so the spec is not split across files.

- **Multi-slice** → `spec.md` only. `/to-tickets` adds `tickets/` beside it.
- **Single slice** → `spec.md` plus `tickets/01-<slug>.md`, whose What to build says "Implement `spec.md`" and whose Acceptance criteria are the spec's criteria as checkboxes. `/implement` always has a ticket to work.

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or its short form.

## When a skill says "resolve the work list"

Turn a reference into the ordered list of tickets to actually work:

- **A `docs/specs/<YYYY-MM-DD>-<feature-slug>/` directory** → every file under its `tickets/`, in `Wave:` then number order. The directory and its `spec.md` are containers, never units of work.
- **A single ticket file** → that file alone.
- **A `spec.md` with no `tickets/` beside it** → nothing; it hasn't been broken down yet.

A ticket is on the **frontier** when its own `Status:` is not `done` and every ticket in its `Blocked by:` line is `done`.

## When a skill says "start a ticket"

Set the file's `Status:` line to `in-progress` and save before the first edit; set it to `done` and tick its acceptance criteria once the work is reviewed. Both changes commit with the ticket's code.

## When a skill says "begin the spec"

Set `spec.md`'s `Status:` line to `in-progress`.

## When a skill says "finish the spec"

Set `spec.md`'s `Status:` line to `done`.

## When a skill says "fetch the spec"

Read `docs/specs/<YYYY-MM-DD>-<feature-slug>/spec.md`, or the path the user passed.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a file with one **child** file per ticket, in the same tree as specs.

- **Map**: `docs/specs/<YYYY-MM-DD>-<effort-slug>/map.md` — the Notes / Decisions-so-far / Fog body.
- **Child ticket**: `docs/specs/<YYYY-MM-DD>-<effort-slug>/tickets/NN-<slug>.md`, numbered from `01`, with the question in the body. Header order as above, with a `Type:` line recording the ticket type (`research`/`prototype`/`grilling`/`task`).
- **Blocking**: a `Blocked by: NN, NN` line in the header. A ticket is unblocked when every ticket it lists is `done`.
- **Frontier**: scan the effort's `tickets/` for files that are neither `in-progress` nor `done` and are unblocked; first by number wins.
- **Claim**: set `Status: in-progress` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: done`, then append a context pointer (gist + path) to the map's Decisions-so-far in `map.md`.
