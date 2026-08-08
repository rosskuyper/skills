---
name: to-spec
description: Turn the current conversation into a spec and publish it to the repo's issue tracker — as a project with an overview and spec documents where the tracker has projects, otherwise as a single issue. No interview, just synthesis of what you've already discussed.
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user — just synthesize what you already know.

The issue tracker and triage label vocabulary should have been provided to you — run `/setup-skills` if not.

## Process

### 1. Explore

Explore the repo to understand the current state of the codebase, if you haven't already. Use the codebase's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

### 2. Agree the seams

Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

Check with the user that these seams match their expectations.

### 3. Write the spec

Write the whole spec using the template below before publishing anything. The template's sections are the unit of publication in step 4, so write them as sections that stand on their own.

### 4. Publish it

Follow the "publish a spec" convention in `docs/agents/issue-tracker.md`. Two shapes, depending on what the tracker has:

- **A tracker with projects (Linear)** → a **project**, moved straight to its in-progress status, whose overview holds Problem Statement / Solution / Out of Scope / Further Notes and links onward to one **document** per remaining section: User Stories, Implementation Decisions, Testing Decisions. Don't apply a triage label — the project isn't a unit of work, the tickets inside it are. The tracker config carries the exact tool names and the overview shape.
- **A tracker without projects (GitHub, GitLab, local markdown)** → a single issue carrying the entire spec as its body, under the template's headings. Apply the `ready-for-agent` triage label — no need for additional triage.

### 5. Hand off

Report where the spec landed, with its URL. Then tell the user the next step is `/to-tickets` against it, which breaks the spec into tracer-bullet tickets inside the same container. Do not run `/to-tickets` yourself — the breakdown is a decision the user drives.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

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
