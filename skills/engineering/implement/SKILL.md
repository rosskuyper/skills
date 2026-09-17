---
name: implement
description: Orchestrate a spec, project, or ticket through implementation, independent verification, review, and per-ticket commits, delegating execution to appropriately sized subagents.
disable-model-invocation: true
---

# Implement

Build the work while keeping the coordinator's context small enough to last the whole run. The coordinator owns ordering, decisions, acceptance gates, and user communication. Workers own investigation, implementation, tests, validation, review, fixes, git operations, and tracker updates. **Delegate execution even for a single ticket.** Do not inspect full diffs, consume raw test logs, or repeat a worker's checks in the coordinator; request missing evidence or assign a focused investigation instead.

If `docs/agents/issue-tracker.md` is missing, ask the user to run `/setup-skills`.

## Model and delegation policy

Before dispatching work, use the session's model identity and available model controls; do not guess from your writing style. Prefer Astra, Fable, or an equivalent high-capability model for coordination. If the current model is outside that tier or its identity is unknown, ask once whether to continue with it or switch, explaining that this skill recommends the stronger tier for cross-ticket decisions. Wait for the answer; respect an earlier explicit choice and do not ask again. A skill cannot switch its own model unless the harness supports it.

Use these routing preferences, resolving names to models actually available in the harness:

| Work | Preferred model |
| --- | --- |
| Coordination, difficult cross-ticket decisions | Astra, Fable, or equivalent |
| Implementation, debugging, semantic acceptance checks, code review | Sol or Opus |
| Bounded searches, known test/typecheck/lint commands, mechanical git/tracker operations | Luna or Sonnet |

Choose an available equivalent when a named model is absent. Select worker model and effort explicitly where supported: low effort for mechanical work, medium for ordinary implementation/review, higher only for demonstrated difficulty. Do not silently inherit the coordinator's model and maximum effort for every worker. If model overrides are unavailable, disclose that delegation still isolates context but cannot guarantee cheaper execution. If subagents are unavailable, agree an inline or split-session fallback with the user before building.

- Give each ticket fresh worker context. Disable conversation inheritance where supported (for example, `fork_turns="none"`); pass a bounded brief with source paths and relevant excerpts. Do not fork the whole run or make every worker rediscover the project.
- Batch related mechanical operations into one assignment rather than spawning an agent per command. Reuse a ticket's worker for fixes, then release it; do not accumulate the entire run in a long-lived worker.
- Keep implementation and independent verification separate. Routine command execution can use a smaller model; deciding whether behavior satisfies the spec needs an implementation/review-capable model.
- Escalate a difficult task to a stronger worker with the failed approach and evidence. Do not take over execution in the coordinator or retry the same approach indefinitely.
- Keep logs and detailed findings in local artifacts outside the committed change. Worker replies should normally stay under 300 words: status, changed paths, evidence, unresolved findings, and artifact pointers. Never omit a blocker to meet the word budget.

## Process

### 1. Resolve the work list

Delegate retrieval of the supplied project, issue, spec, URL, or agreed conversation scope. Have the worker follow the "resolve the work list" convention in `docs/agents/issue-tracker.md` and return a compact **ordered list of tickets**, states, dependencies, and source pointers. Cache fetched ticket/spec content locally for subsequent workers.

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

A one-ticket work list follows the same delegated loop; keep its brief and bookkeeping proportional to the work.

### 2. Agree the run, once

Report the work list, blockers, execution order, and selected worker models. Explain that the run will work through every ticket, commit after each, and stop only under section 4. Get one approval unless the user has already authorized that scope.

Do not seek per-ticket confirmation. Keep progress updates brief and communicate decisions or blockers without forwarding worker transcripts.

Read the spec's Implementation and Testing Decisions and agreed seams once. Retain a compact decision summary and source pointers for briefs. Delegate branch and working-tree checks: start from the spec's branch where one exists, and stop if the initial tree contains uncommitted work. Have a worker establish the baseline checks before building; record the commands for later validators.

Maintain a small local run ledger outside the committed change: branch, decisions, ticket dependencies/states, base and landed commits, validation/review evidence pointers, blockers, and next action. Update it at ticket boundaries. After compaction or resumption, recover from this ledger and reconcile live git/tracker state through a worker instead of replaying the conversation.

### 3. Run the loop

Take the first **frontier** ticket whose blockers are complete. Keep a single writer in a shared working tree; finish edits before validators or reviewers inspect it.

**a. Start and brief.** Delegate the in-progress tracker update and capture the ticket's base commit. Give a fresh implementation worker:

- ticket ID, scope, acceptance criteria, and relevant spec decisions/testing seams
- source paths for cached ticket/spec content, domain glossary, and relevant ADRs
- a sentence or two on preceding tickets and any interfaces they established
- branch/worktree, base commit, allowed scope, known check commands, and instruction to use `/tdd` at the agreed seams
- the report contract below; no commits or tracker closure until the coordinator accepts the gates

**b. Build.** The implementation worker writes code and tests, runs the focused TDD cycle, and reports the result. It leaves full logs and detailed notes in artifacts. The coordinator reads the summary only.

**c. Verify independently.** Assign a different worker to run typechecking and the required test suite on the finished tree. Batch other required mechanical checks into this assignment. Require executed commands, exit codes, test counts where available, skipped checks, log paths, and the checked revision/tree identity. A bare “tests passed” is insufficient. The coordinator evaluates this evidence without rerunning commands.

**d. Review independently.** Delegate `/code-review` using the ticket base and the actual candidate change. Its Standards and Spec reviewers must inspect the candidate independently of the implementer, confirm the diff is non-empty and in scope, and map each acceptance criterion to code/test evidence. For uncommitted changes, explicitly cover staged, unstaged, and new files; a `base...HEAD` diff alone misses them. If nesting or available agent slots cannot accommodate this, dispatch the two review roles directly at the coordinator level, sequentially if necessary. Return compact findings with file/line pointers and separate verdicts for each axis.

Send actionable failures to the implementation worker for one bounded repair pass, escalating its model if needed. Revalidate affected checks and re-review affected criteria after edits; evidence for an earlier tree cannot approve a later one. Reuse successful checks only while their inputs remain unchanged. Unresolved failures follow section 4.

**e. Accept and land.** Only after independent validation and both review axes pass, delegate one commit referencing the ticket, then the completed tracker update and acceptance-criteria ticks. The worker must confirm the committed content matches the verified tree and return the commit ID and tracker outcome. Include only ticket files, keeping run artifacts out. The coordinator owns this gate; an implementer's success report alone cannot close a ticket.

**f. Record and advance.** Update the ledger, release finished workers, and recompute the frontier. Do not reread completed tickets or their diffs. Use this compact report contract across assignments, omitting irrelevant fields:

> Ticket / role / status; base and candidate identity; changed paths and behavior; commands + exit codes + test counts; acceptance evidence and Standards/Spec verdicts; unresolved blockers; commit/tracker outcome; artifact paths.

### 4. When a ticket goes wrong

Stop working *that ticket* when any of these hold:

- required checks are still failing or cannot run after the bounded repair pass
- `/code-review` raises something the subagent couldn't resolve
- the subagent reports a decision the spec doesn't settle
- the diff strays outside the ticket's scope

Delegate parking the failed ticket's changes and restoring the last verified state without discarding unrelated work. Leave the ticket in progress with a comment explaining the blocker, and **skip it along with everything blocked by it**. Confirm the tree is restored before continuing.

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

Only when the user asks, and only for tickets you can see are disjoint, run a wave concurrently — each subagent in its own git worktree, merged back one at a time with a validation worker running the test suite and checking integration after each merge. Treat the merge cost as part of the decision, and say so before starting.
