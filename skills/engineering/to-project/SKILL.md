---
name: to-project
description: Turn the current conversation into a published spec and complete ticket breakdown, then review the result. Chooses seams, slices, waves, and dependencies, publishes to the configured tracker, and commits design artifacts without intermediate confirmation.
disable-model-invocation: true
---

# To Project

Complete the planning work from the current conversation and design docs: publish a spec and, when the work needs several slices, its tickets. Invocation authorizes this planning and publication flow, including the design-artifact commits below. Make routine decisions and finish before asking whether the user wants changes. Do not start implementation.

This workflow is self-contained; do not invoke `/to-spec` or `/to-tickets`, or require them to be installed.

## 1. Gather context and choose the seams

Synthesize what is already known; do not restart the interview. Read any supplied spec reference in full, including comments. For a project-shaped spec, follow the "fetch the spec" convention in `docs/agents/issue-tracker.md`: read the overview, attached documents, and existing issues. Reuse context already available in this session.

Explore the codebase if needed. Use its domain glossary vocabulary and respect existing ADRs. Choose the highest practical testing seams, preferring existing seams and as few as possible; ideally one.

Read the configured issue tracker and triage vocabulary. If configuration is missing, ask for the missing destination or configuration; the user can run `/setup-skills`. Resolve only information that prevents completion. For routine uncertainty about seams, sizing, or breakdown, make a reasonable choice within the discussed scope, record the assumption, and continue without confirmation.

## 2. Size and draft the spec

Decide whether the work is one vertical slice or several. One slice is a complete path through the relevant layers, independently demoable or verifiable, sized for a single fresh context window, with nothing useful to break down further. When uncertain, choose several slices. A wide refactor is always several slices.

State the size call and rationale briefly, then continue. Write the whole spec before publishing, with these headings:

- **Problem Statement** — the problem from the user's perspective.
- **Solution** — the solution from the user's perspective.
- **Acceptance Criteria** — only for a single slice: a checklist of observable, verifiable behaviours. Omit for several slices; criteria belong in their tickets.
- **User Stories** — numbered “As an <actor>, I want <feature>, so that <benefit>” stories. Cover the discussed feature comprehensively for several slices; a handful suffices for one. Do not invent scope.
- **Implementation Decisions** — modules, interfaces, architecture, schemas, API contracts, and technical decisions.
- **Testing Decisions** — external behaviour to test, modules and seams, and relevant prior art; avoid testing implementation details.
- **Out of Scope** — explicit boundaries.
- **Further Notes** — remaining context and assumptions.

Make sections stand on their own because they may be published separately. Avoid specific file paths and code snippets in specs and tickets; they go stale. A prototype snippet may be included when it expresses a decision better than prose: trim to the decision and identify its prototype origin.

## 3. Publish the spec

Follow the "publish a spec" convention in `docs/agents/issue-tracker.md`, using its exact tool names and overview shape:

- **One slice, any tracker:** create a single issue with the entire spec, including Acceptance Criteria, and apply `ready-for-agent`. Do not create a project or a duplicate implementation ticket. Skip ticket breakdown and proceed to the artifact commit and final review.
- **Several slices, tracker with projects (Linear):** create an in-progress project. Its overview holds Problem Statement, Solution, Out of Scope, and Further Notes, with links to a document per remaining section: User Stories, Implementation Decisions, Testing Decisions. Do not apply a triage label to the project.
- **Several slices, tracker without projects (GitHub, GitLab, local markdown):** create one issue containing the entire spec and apply `ready-for-agent`.

Record the container identifier for ticket publication. If continuing a partially completed run or working from an already published spec, inspect and reuse the existing artifacts instead of creating duplicates. After an uncertain write result, check the tracker before retrying. Report any publication failure and the artifacts already created; do not claim completion while required writes are missing.

## 4. Commit the design artifacts

If the session left design artifacts (`CONTEXT.md`, ADRs, or local `.scratch/` spec files), commit them on a branch named for the spec. Use the issue's generated branch name where available, otherwise the feature slug. Leave it checked out so implementation can continue there. Reuse the feature branch on a resumed run.

Commit only the session's design artifacts, referencing the spec URL (or local path) in the message. Leave unrelated changes untouched and mention them in the final review. If there are no design artifacts, skip this step. Do not push or open a PR.

## 5. Draft the tickets and waves

For several slices, break the work into tracer-bullet tickets. Each cuts a narrow, complete path through the relevant layers (schema, API, UI, tests), is independently demoable or verifiable, and fits a single fresh context window. Put useful prefactoring first.

Declare each ticket's blockers: only tickets that genuinely must complete before it can start. Group tickets into ordered, named delivery waves, each a coherent checkpoint. Two or three waves is common; one is fine for a small breakdown. No ticket may depend on a later wave; dependencies must be acyclic.

**Wide refactors use expand–contract instead of forced vertical slices.** Add the new form alongside the old, migrate callers in batches sized by blast radius, then remove the old form. Every migration depends on the expansion; contraction depends on every migration. Keep CI green between batches. If batches cannot stay green independently, use a shared integration branch and a final integrate-and-verify ticket blocked by all batches; green is promised only there.

Check that the tickets cover the spec, have observable acceptance criteria, and do not add scope. Decide granularity, blockers, merges, splits, and waves yourself; do not pause for approval.

## 6. Publish the tickets

Publish in dependency order, blockers first, keeping waves contiguous where possible.

- **Local files:** write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`. Include the number and title, **What to build**, **Blocked by** (numbers/titles, or “None — can start immediately”), **Wave**, **Status: ready-for-agent**, and acceptance-criteria checkboxes. Commit these files on the spec's branch. If none was needed earlier, create the feature branch now and commit the ticket files there without an additional confirmation.
- **A real tracker:** create one issue per ticket and apply `ready-for-agent` unless instructed otherwise. Include **Parent** (reference the source issue; omit for a project-shaped spec), **What to build**, **Acceptance criteria** (checkboxes), and **Blocked by** (real issue references or “None — can start immediately”). Use native blocking/sub-issue relationships where supported; otherwise record blockers in the body. Describe end-to-end behaviour, not layer-by-layer implementation tasks.
- **Inside a project-shaped spec:** create one milestone per wave first, then set the project and wave milestone on each issue. If milestone tools are unavailable, retain wave names in ticket bodies and report the limitation; do not invent a substitute container. Keep the project's status and overview as published.

Verify the resulting issues, project membership, and blocking relationships. Do not close or modify a parent issue as part of ticket publication. The implementation frontier is the tickets whose blockers are all done.

## 7. Review the completed result

Return the spec link (or local path), size call, testing seams, and ticket links grouped by wave. For each ticket, summarize what it delivers and its blockers. Include meaningful assumptions, any publication limitations, and the branch and commits carrying design artifacts.

Only now ask whether the user wants changes to scope, seams, granularity, blockers, or waves. Apply requested revisions to the existing artifacts, keeping the spec, tickets, and dependencies consistent; do not recreate the whole set. A spec revision may update the parent when requested by the user.

Name `/implement` against the single issue or completed spec/project as the next step, but leave starting implementation to the user.
