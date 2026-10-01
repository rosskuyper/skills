---
name: to-spec
description: Turn the current conversation into a spec and publish it to the configured tracker — by default a `docs/specs/` folder (plus one ticket when the work is a single vertical slice); on a hosted tracker a single issue, or a project with spec documents where the tracker has projects and the work is several slices. Commits the design docs (glossary, ADRs, spec folder) on a branch named for the feature. No interview, just synthesis of what you've already discussed.
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user — just synthesize what you already know.

The issue tracker and triage label vocabulary should have been provided to you — run `/setup-skills` if not.

## Process

### 1. Explore

Explore the repo to understand the current state of the codebase, if you haven't already. Use the codebase's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching. Prior specs in `docs/specs/` are the spec archive: consult them through `/recall`, never read them directly.

### 2. Agree the seams

Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

Check with the user that these seams match their expectations.

### 3. Size it

Decide whether the work is **one vertical slice** or several. You have just agreed the seams, so you already know. One slice means: it cuts a complete path through every layer, it is demoable on its own, it fits in a single fresh context window, and `/to-tickets` would have nothing to break it into. Adding an OAuth provider to an app that already has sessions is usually one slice; adding auth to an app that has none is not.

A **wide refactor** is never one slice, however mechanical it looks — its blast radius fans across the codebase and it has to be sequenced expand–contract.

State the call and why, in a sentence, and let the user correct it. **When you can't tell, call it multi-slice.** A project wrapped around one ticket is a container you ignore; a multi-slice feature built as one ticket degrades halfway through and you re-do it.

### 4. Write the spec

Write the whole spec using the template below before publishing anything. The template's sections are the unit of publication in step 5, so write them as sections that stand on their own.

Scale the spec to the call you just made. A one-slice spec fills the same headings, but proportionately — a handful of user stories, not a long list — and it adds the **Acceptance Criteria** section, because no `/to-tickets` pass is coming to write them and `/implement` verifies against them. A multi-slice spec omits that section; criteria belong to the tickets.

### 5. Publish it

Follow the "publish a spec" convention in `docs/agents/issue-tracker.md`. The shape follows from the size call and the tracker:

- **Local markdown (the default), any size** → write `docs/specs/<YYYY-MM-DD>-<feature-slug>/spec.md`, dated today: `# <Title>`, then `Status: ready`, then every template heading in the one file. For **one vertical slice**, also write `tickets/01-<slug>.md` beside it, in the ticket header order (`# 01 — <Title>`, `Status: ready-for-agent`, `Wave: 1`, blank line, `## What to build`, `## Acceptance criteria`), whose What to build says "Implement `spec.md`" and whose Acceptance criteria are the spec's criteria as checkboxes. For **several slices**, `spec.md` only — `/to-tickets` adds `tickets/` beside it.
- **One vertical slice, hosted tracker** → a single issue carrying the entire spec as its body, under the template's headings, including Acceptance Criteria. Apply the `ready-for-agent` triage label. Do **not** open a project for it, even on a tracker that has them — the issue is the unit of work, and a container around one ticket just hides it.
- **Several slices, on a tracker with projects (Linear)** → a **project**, moved straight to its in-progress status, whose overview holds Problem Statement / Solution / Out of Scope / Further Notes and links onward to one **document** per remaining section: User Stories, Implementation Decisions, Testing Decisions. Don't apply a triage label — the project isn't a unit of work, the tickets inside it are. The tracker config carries the exact tool names and the overview shape.
- **Several slices, on a hosted tracker without projects (GitHub, GitLab)** → a single issue carrying the entire spec as its body, under the template's headings. Apply the `ready-for-agent` triage label — no need for additional triage.

### 6. Commit the design artifacts

The session that led here usually leaves design artifacts in the working tree — glossary updates (`CONTEXT.md`), ADRs, and on a local tracker the `docs/specs/<YYYY-MM-DD>-<feature-slug>/` folder. Committed nowhere, they dangle through the breakdown and into the build, where they get lost or swept into some ticket's diff. Commit them now, on the feature's branch, so they ride ahead of every ticket commit:

- If the tree holds no design artifacts (possible only on a hosted tracker), skip this step entirely.
- Cut a branch named `<feature-slug>` — the spec folder's slug, without the date — and leave it checked out. `/to-tickets` and `/implement` continue on it, so the docs become the first commit of the feature's eventual PR.
- Commit **only the design artifacts**, referencing the spec in the message by path (local) or URL (hosted tracker). Anything else sitting in the tree is not yours to commit — leave it and mention it in the hand-off.
- Do not push or open a PR — that belongs to the implementation run.

### 7. Hand off

Report where the spec landed — its `spec.md` path on a local tracker, its URL on a hosted one — and the branch now carrying the design artifacts. Then the next step follows the size call, not the shape:

- **One vertical slice** → name `/implement` against the ticket as the next step — `tickets/01-<slug>.md` locally, the issue on a hosted tracker. It resolves to that ticket alone and builds it in one pass; there is nothing for `/to-tickets` to slice. Do not run it yourself — building is a decision the user drives.
- **Several slices** → invite the user to type `/to-tickets` now, in this session, where the full design context still lives — the breakdown continues warm instead of re-fetching the spec cold. You cannot fire it yourself; it is user-invoked. Exception: if the spec came out of a long conversation and context is already deep, recommend running `/to-tickets` in a fresh session against the published spec instead — the spec exists precisely so the breakdown can start cold.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## Acceptance Criteria

**Single-slice specs only** — omit this section entirely when the work is several slices, where criteria belong to the tickets `/to-tickets` writes.

A checklist of the observable behaviours that make this done. Each one is verifiable by running the software, not by reading the diff.

- [ ] Criterion 1
- [ ] Criterion 2

## User Stories

A numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

For a multi-slice spec this list should be extremely extensive and cover all aspects of the feature. For a single slice, a handful is right — the Acceptance Criteria above carry the detail, and padding the list invents scope the user never asked for.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
