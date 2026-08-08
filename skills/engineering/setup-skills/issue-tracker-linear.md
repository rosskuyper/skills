# Issue tracker: Linear

Issues and specs for this repo live as Linear issues. Use the **Linear MCP server** for all operations.

## Access

Operations go through the Linear MCP server's tools, not a CLI — Linear has no first-party CLI. Discover the exact tool names once at the start of a session rather than trusting the names below: they vary by MCP client and server version. The conventional set is `list_issues`, `get_issue`, `create_issue`, `update_issue`, `list_comments`, `create_comment`, `list_issue_labels`, `list_issue_statuses`, `list_teams`, `list_users`, plus the project-shaped tools listed under "Projects, documents and milestones".

If the Linear MCP server isn't connected, **stop and tell the user** — don't fall back to writing local markdown files, because the issues other sessions expect to find won't be there. Setting it up is a one-time step the user must do themselves.

Two facts to resolve before the first write, and to cache for the session:

- **Team** — Linear scopes issues to a team. If this repo maps to exactly one team, use it. If several teams exist, ask the user once which one this repo tracks, and record the answer in this file under "Team" so later sessions don't re-ask.
- **Workflow states** — the state names for this team, which are configurable per team (see "Workflow states vs labels" below).

**Team:** _(not yet recorded — ask the user and write it here)_

## Conventions

- **Create an issue**: `create_issue` with the team, a title, and a markdown description. Linear descriptions are markdown, so headings and checklists in the templates below render natively.
- **Read an issue**: `get_issue`, then `list_comments` for the conversation. Fetch both — triage and review decisions usually live in the comments, not the description.
- **List issues**: `list_issues`, filtered by team, state, label, or assignee. Prefer filtering server-side over listing everything and filtering locally.
- **Comment on an issue**: `create_comment`.
- **Apply / remove labels**: `update_issue` with the full desired label set. Linear's update **replaces** the label list rather than adding to it, so read the current labels first and send the union — otherwise you silently strip labels another session applied.
- **Start**: `update_issue` moving it to a state in the `started` category (usually `In Progress`). Do this before the first edit of a build session — it's how a parallel session sees the slice is taken.
- **Close**: `update_issue` moving it to a state in the `completed` category (usually `Done`), or the `canceled` category for work that won't be done (see below).
- **Identifiers**: Linear issues are referenced as `TEAM-123` (e.g. `ENG-42`), not `#42`. When a skill or commit message says `#42`, treat it as a bare number needing the team prefix, and confirm the match before acting on it.

## Workflow states vs labels

Linear splits what a label-only tracker expresses in one dimension into **two**: every issue has exactly one **workflow state**, and any number of **labels**. This matters for triage — see `triage-labels.md`, which records which of the five canonical roles map to states and which to labels for this repo.

Linear's states are grouped into fixed **categories** — `triage`, `backlog`, `unstarted`, `started`, `completed`, `canceled` — and the display names within them are configurable per team. Resolve the actual names with `list_issue_statuses` before setting a state; don't assume a team calls its `completed` state "Done".

Linear also has a native **Triage** inbox (a queue for un-triaged incoming issues, enabled per team). Where it's on, that queue *is* the `needs-triage` role — prefer it to a label.

## Projects, documents and milestones

Linear has a container the label-only trackers don't: a **project**. A project holds an **overview** (its description — a full markdown document), any number of attached **documents**, an ordered list of **milestones**, and the issues that belong to it. Specs live in this shape; individual units of work stay as issues inside it.

Conventional tool names, again worth discovering rather than trusting: `list_projects`, `get_project`, `create_project`, `update_project`, `list_documents`, `get_document`, `create_document`, `update_document`, `list_project_milestones`, `create_project_milestone`.

- **Project status** — every project carries exactly one status, drawn from the fixed categories `backlog`, `planned`, `started`, `completed`, `canceled`. Display names are configurable per workspace, so resolve the real name before setting one — don't assume a workspace calls its `started` status "In Progress".
- **Issues in a project** — `create_issue` (or `update_issue`) with the project set. An issue belongs to at most one project.
- **Milestones** — ordered checkpoints inside a project, each holding a subset of its issues. Use them to group issues into delivery waves; an issue belongs to at most one milestone.
- **Labels** — projects have their own label set, separate from issue labels. Triage roles are issue-level vocabulary; don't apply them to a project.
- **Completing a project** — `update_project` to a `completed`-category status once every issue in it is `completed` or `canceled`. Linear does not do this on the last issue closing, so a project stays `started` forever unless something closes it.

**If the connected server exposes documents read-only** (older versions ship `get_document` / `list_documents` with no create), fold the content that would have been separate documents into the project description under its own headings, and tell the user that's what happened. The content lands whole either way — only the shape degrades.

## Pull requests as a triage surface

**Not applicable.** Linear has no pull requests, so the PR-as-request-surface flag that the GitHub and GitLab trackers carry doesn't exist here. Code review happens on the git host; `/triage` covers Linear issues only.

Linear does link PRs to issues via its GitHub/GitLab integration (a magic word like `Fixes ENG-42` in the PR body). Those links are useful context when reading an issue, but they aren't a triage surface — don't triage a linked PR as though it were an issue.

## When a skill says "publish to the issue tracker"

Create a Linear issue on the recorded team.

## When a skill says "publish a spec"

A spec is bigger than an issue — publish it as a **project** on the recorded team, never as a single issue:

1. `create_project` on the recorded team, named after the feature in the codebase's own domain vocabulary. Set its one-line summary to the problem in a sentence.
2. Set the project description to the **overview** — Problem, Solution, Out of Scope, and a link to each spec document (see the shape below).
3. Set its status to the workspace's `started` status (usually "In Progress"). A spec is written because the work is about to begin, so it does not sit in `planned`.
4. Create one **document** per remaining spec section, attached to the project. Title each after its section.
5. Go back and `update_project` so the overview's document links point at the real document URLs — they only exist once the documents do.

<project-overview-shape>

## Problem

The problem the user is facing, from their perspective.

## Solution

The solution, from the user's perspective.

## Out of scope

What this work deliberately does not cover.

## Spec documents

- [User Stories](url)
- [Implementation Decisions](url)
- [Testing Decisions](url)

## Further notes

Anything that didn't belong in a document. Omit the heading if there is nothing.

</project-overview-shape>

Don't apply triage labels to the project — those are issue-level vocabulary, and the issues inside the project carry them.

## When a skill says "fetch the relevant ticket"

`get_issue` for the identifier, plus `list_comments`.

## When a skill says "resolve the work list"

Turn a reference into the ordered list of issues to actually work:

- **A project** → `list_issues` filtered to it. Order by milestone position, then by blocking edges within each milestone. The project itself is never a unit of work.
- **An issue with sub-issues** → its children, same ordering. The parent is a container.
- **An issue with no sub-issues** → that issue alone, *even when it belongs to a project*. Pointing at one ticket means one ticket; don't expand to its siblings.
- **A document** → the project it's attached to, resolved as above.

An issue is on the **frontier** when it sits in an incomplete state and every issue in its `blocked by` relations sits in a `completed` or `canceled` state.

## When a skill says "start a ticket"

`update_issue` moving it to a `started`-category state, and assign it to the driving dev, before the first edit. Close it by moving it to a `completed`-category state once the work is reviewed and committed.

## When a skill says "fetch the spec"

If the reference is a project (a project URL, a project name, or an issue whose project is set), read the whole container: `get_project` for the overview, `list_documents` + `get_document` for every attached document, and `list_issues` filtered to the project for the work already broken out of it. The overview alone is a summary, not the spec.

If the reference is a bare issue with no project, `get_issue` plus `list_comments` is the spec.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single issue with **sub-issues** as tickets.

- **Map**: a single issue labelled `wayfinder:map`, holding the Destination / Notes / Decisions-so-far / Fog body. Create it with `create_issue` and apply the label.
- **Child ticket**: an issue created with the map as its **parent** — Linear's native sub-issue relationship, which renders the children under the map in the UI. Labels: `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, the ticket is assigned to the driving dev.
- **Blocking**: Linear's **native `blocks` / `blocked by` issue relations** — the canonical, UI-visible representation, available on every plan tier. Add the edge from the blocked ticket as `blocked by` the blocker. Linear surfaces blocked issues in its own views, so the frontier is visible without opening the map. A ticket is **unblocked** when every issue blocking it sits in a `completed` or `canceled` state.
- **Frontier query**: list the map's sub-issues in an incomplete state, then drop any with an open `blocked by` relation or an assignee; first in map order wins.
- **Claim**: `update_issue` setting the assignee to the driving dev — the session's first write.
- **Resolve**: `create_comment` with the answer, move the issue to a `completed` state, then append a context pointer (gist + link) to the map's Decisions-so-far. Linear issue URLs are stable and human-readable — use the issue's URL as the link, with its title as the link text.
