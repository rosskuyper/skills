---
name: implement
description: Build the work described by a spec, a project, or a ticket — resolve whatever you were given into an ordered work list, then build the frontier ticket with /tdd at the pre-agreed seams and /code-review before committing.
disable-model-invocation: true
---

# Implement

Build the work. The first job is not writing code — it is working out **what the unit of work is**. Pointing this skill at a container and letting it implement the container is how a fifteen-slice project ends up built in one exhausted context.

The issue tracker should have been provided to you — run `/setup-skills` if not.

## Process

### 1. Resolve the work list

Take whatever the user gave you — a project, an issue identifier, a spec file, a URL, or nothing at all — and resolve it into an **ordered list of tickets**, following the "resolve the work list" convention in `docs/agents/issue-tracker.md`.

| What you were given | The work list |
| --- | --- |
| A project (a project-shaped spec) | Its issues, in wave order, then dependency order within each wave |
| An issue that has children | Its children — never the parent |
| An issue with no children | That issue alone, even when it belongs to a project |
| A local `.scratch/<feature>/` directory | The files under its `issues/`, in number order |
| A spec with no breakdown yet | Nothing — see below |
| Nothing | Whatever the conversation has already agreed |

**A container is never a unit of work.** If what you were handed has been broken down, the breakdown is the work and the container is context. This is the failure the step exists to prevent: implementing a spec whose tickets already exist means building the whole feature in one pass and leaving every ticket open behind you.

**If the target is a spec with no breakdown**, stop and say so, and offer `/to-tickets` first. Build it directly only if the user hears that and still asks you to — a spec small enough to land in a single pass is possible, just rare enough to be worth confirming.

### 2. Agree the scope

Report the resolved work list: each ticket, its state, and which are on the **frontier** — the tickets whose blockers are all complete. Name the one you propose to take, which is the first frontier ticket in list order.

**Default to one ticket per run.** `/to-tickets` sizes each slice to fit a single fresh context window, and taking several at once spends that budget before the last one starts. Offer a whole wave, or the lot, only if the user asks — and say plainly that a long run degrades.

If nothing is on the frontier, say which blockers are open rather than picking a blocked ticket anyway.

### 3. Load the ticket's context

Read both halves before editing anything:

- **The ticket** — what to build, and its acceptance criteria.
- **The spec it was cut from** — the Implementation and Testing Decisions, and the seams agreed in `/to-spec`. Fetch it via the "fetch the spec" convention. A ticket's acceptance criteria are not the spec; they assume it.

Also read the repo's domain glossary and any ADRs covering the area you're touching.

### 4. Build it

Move the ticket to the tracker's in-progress state before the first edit, so a parallel session doesn't take the same slice.

Use `/tdd` where possible, at the pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

### 5. Close it out

Use `/code-review` to review the work, and act on what it finds before going further.

Commit your work to the current branch, referencing the ticket in the commit message so the tracker links the two.

Then close the ticket: move it to the tracker's completed state and tick off its acceptance criteria.

### 6. Take stock

Report what landed and what the work list looks like now — the next frontier ticket, and anything the completed ticket has just unblocked. Ask before taking it; a fresh context is the point.

When the list is empty and every ticket is complete, offer to move the container to its completed state. Nothing else closes the project `/to-spec` opened.
