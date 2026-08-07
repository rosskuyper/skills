# Issue tracker: Linear

Issues and specs for this repo live as Linear issues. Use the **Linear MCP server** for all operations.

## Access

Operations go through the Linear MCP server's tools, not a CLI — Linear has no first-party CLI. Discover the exact tool names once at the start of a session rather than trusting the names below: they vary by MCP client and server version. The conventional set is `list_issues`, `get_issue`, `create_issue`, `update_issue`, `list_comments`, `create_comment`, `list_issue_labels`, `list_issue_statuses`, `list_teams`, `list_users`.

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
- **Close**: `update_issue` moving it to a state in the `completed` category (usually `Done`), or the `canceled` category for work that won't be done (see below).
- **Identifiers**: Linear issues are referenced as `TEAM-123` (e.g. `ENG-42`), not `#42`. When a skill or commit message says `#42`, treat it as a bare number needing the team prefix, and confirm the match before acting on it.

## Workflow states vs labels

Linear splits what a label-only tracker expresses in one dimension into **two**: every issue has exactly one **workflow state**, and any number of **labels**. This matters for triage — see `triage-labels.md`, which records which of the five canonical roles map to states and which to labels for this repo.

Linear's states are grouped into fixed **categories** — `triage`, `backlog`, `unstarted`, `started`, `completed`, `canceled` — and the display names within them are configurable per team. Resolve the actual names with `list_issue_statuses` before setting a state; don't assume a team calls its `completed` state "Done".

Linear also has a native **Triage** inbox (a queue for un-triaged incoming issues, enabled per team). Where it's on, that queue *is* the `needs-triage` role — prefer it to a label.

## Pull requests as a triage surface

**Not applicable.** Linear has no pull requests, so the PR-as-request-surface flag that the GitHub and GitLab trackers carry doesn't exist here. Code review happens on the git host; `/triage` covers Linear issues only.

Linear does link PRs to issues via its GitHub/GitLab integration (a magic word like `Fixes ENG-42` in the PR body). Those links are useful context when reading an issue, but they aren't a triage surface — don't triage a linked PR as though it were an issue.

## When a skill says "publish to the issue tracker"

Create a Linear issue on the recorded team.

## When a skill says "fetch the relevant ticket"

`get_issue` for the identifier, plus `list_comments`.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single issue with **sub-issues** as tickets.

- **Map**: a single issue labelled `wayfinder:map`, holding the Destination / Notes / Decisions-so-far / Fog body. Create it with `create_issue` and apply the label.
- **Child ticket**: an issue created with the map as its **parent** — Linear's native sub-issue relationship, which renders the children under the map in the UI. Labels: `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, the ticket is assigned to the driving dev.
- **Blocking**: Linear's **native `blocks` / `blocked by` issue relations** — the canonical, UI-visible representation, available on every plan tier. Add the edge from the blocked ticket as `blocked by` the blocker. Linear surfaces blocked issues in its own views, so the frontier is visible without opening the map. A ticket is **unblocked** when every issue blocking it sits in a `completed` or `canceled` state.
- **Frontier query**: list the map's sub-issues in an incomplete state, then drop any with an open `blocked by` relation or an assignee; first in map order wins.
- **Claim**: `update_issue` setting the assignee to the driving dev — the session's first write.
- **Resolve**: `create_comment` with the answer, move the issue to a `completed` state, then append a context pointer (gist + link) to the map's Decisions-so-far. Linear issue URLs are stable and human-readable — use the issue's URL as the link, with its title as the link text.
