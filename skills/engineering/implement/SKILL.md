---
name: implement
description: Build the work described by a spec, a project, or a ticket — resolve whatever you were given into an ordered work list, then orchestrate it ticket by ticket, dispatching each slice to a fresh subagent that drives /tdd at the pre-agreed seams, verifying its work, and committing per ticket.
disable-model-invocation: true
---

# Implement

Build the work. Two jobs, in order: work out **what the unit of work is**, then **orchestrate the units** — you hold the spec, the work list and the running state; the subagents hold the code.

**You are the orchestrator, not the builder.** Do not write the implementation yourself when the work list holds more than one ticket. `/to-tickets` sizes each slice to a single fresh context window, so building them all in your own context spends that budget before the last slice starts, and the run degrades exactly when it should be sharpest. Your context is the one thing that has to last the whole run.

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

**A container is never a unit of work.** If what you were handed has been broken down, the breakdown is the work and the container is context. Implementing a spec whose tickets already exist means building the whole feature in one pass and leaving every ticket open behind you.

**If the target is a spec with no breakdown**, stop and say so, and offer `/to-tickets` first. Build it directly only if the user hears that and still asks you to — a spec small enough to land in a single pass is possible, just rare enough to be worth confirming.

The exception is a **single-slice spec**: an issue that `/to-spec` sized as one vertical slice and published whole, carrying its own Acceptance Criteria section. That is a unit of work, not a container missing its breakdown — build it, and don't offer `/to-tickets` against it.

**A one-ticket work list is not a run.** Build it yourself, in this context, following the per-ticket steps in section 3 without the dispatch. The orchestration below is what a *container* resolves to.

### 2. Agree the run, once

Report the work list — each ticket, its state, its blockers — and the order you'll take it in. Then say plainly what the run will do: work unattended through every ticket, commit after each, and stop only on the conditions in section 4. Get one approval.

**Then don't ask again.** Per-ticket confirmation is the thing this design exists to remove. The next time you address the user is the final report, or a stop condition.

Read the spec once, now, before the first dispatch: the Implementation and Testing Decisions, and the seams agreed in `/to-spec`. Every brief you write is cut from it, and re-reading it per ticket wastes the context you are trying to protect.

### 3. Run the loop

Until the work list is empty, take the next **frontier** ticket — first in list order whose blockers are all complete — and:

**a. Start it.** Move it to the tracker's in-progress state, per the "start a ticket" convention.

**b. Brief a subagent.** It has none of your conversation, so anything you leave out is lost. Give it, in full:

- the ticket: what to build, and its acceptance criteria
- the slice of the spec that governs it — the relevant Implementation and Testing Decisions, and the seams to test at
- what the preceding tickets already landed, in a sentence or two, so it builds on them rather than around them
- pointers to the repo's domain glossary and any ADRs covering the area
- the instruction to use `/tdd` at those seams, and to report back: what changed, what tests it added, and anything it could not resolve

Dispatch it as a subagent so it gets a fresh context window. If your harness has no subagents, do the work inline but tell the user the run will degrade over a long list, and offer to split it.

**c. Verify, don't trust.** Take the report as a claim and check it yourself before believing it:

- the diff is non-empty and stays inside the ticket's scope
- typechecking passes
- the test suite passes — you run it, not the subagent
- each acceptance criterion is actually met by what changed

A subagent reporting success on work that doesn't compile is the failure mode this step exists for.

**d. Review it.** Use `/code-review` on the slice. Apply what it finds, dispatching a follow-up subagent if the fix is substantial.

**e. Commit it.** One commit per ticket, referencing the ticket, so a bad slice can be reverted without unpicking the run.

**f. Close it.** Move the ticket to completed and tick off its acceptance criteria.

**g. Re-resolve the frontier.** Closing a ticket may unblock several. Recompute rather than walking the list you printed in step 2.

Keep a short running log as you go — ticket, outcome, commit — so the final report doesn't depend on recalling twelve slices.

### 4. When a ticket goes wrong

Stop working *that ticket* when any of these hold:

- typechecking or the test suite is still red after the subagent's attempt
- `/code-review` raises something the subagent couldn't resolve
- the subagent reports a decision the spec doesn't settle
- the diff strays outside the ticket's scope

Then: revert or park that ticket's changes so the tree stays green, leave the ticket in its in-progress state with a comment saying what blocked it, and **skip it along with everything blocked by it**. Carry on with the rest of the list.

Do not halt the whole run. Stopping at ticket 3 of 12 because one slice was ambiguous wastes the unattended window that the rest of the list would have used. The exception is a failure that isn't ticket-shaped — a broken build on the base commit, a tracker you can't write to, the same failure on three consecutive tickets — where continuing just multiplies the damage. Stop there and say why.

### 5. Report

When the list is exhausted, report once:

- what landed, ticket by ticket, with its commit
- what was skipped, and the specific thing that blocked each one
- what remains blocked behind the skips

Then stop. Do not re-plan the skipped work — what to do about an ambiguous slice is the user's call, and `/grill-with-docs` or `/to-tickets` is usually the answer.

If everything completed and the container is a project, offer to move it to its completed state. Nothing else closes the project `/to-spec` opened.

## Running slices in parallel

Serial is the default and usually correct: tracer-bullet slices in the same wave tend to touch the same seams, and concurrent builds against one working tree collide.

Only when the user asks, and only for tickets you can see are disjoint, run a wave concurrently — each subagent in its own git worktree, merged back one at a time with the test suite run after each merge. Treat the merge cost as part of the decision, and say so before starting.
