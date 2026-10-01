# Agent Skills

A collection of agent skills (slash commands and behaviors) loaded by Claude Code. Skills are organized into buckets and consumed by per-repo configuration emitted by `/setup-skills`.

## Language

**Issue tracker**:
The tool that hosts a repo's issues — by default local markdown committed under `docs/specs/`, otherwise Linear, GitHub Issues, GitLab Issues, or similar. Skills like `to-tickets`, `to-spec`, and `triage` read from and write to it.
_Avoid_: backlog manager, backlog backend, issue host

**Issue**:
A single tracked unit of work inside an **Issue tracker** — a bug, task, spec, or slice produced by `to-tickets`.
_Avoid_: "ticket" as a glossary term — the skills' prose says "ticket" freely for an **Issue** that is a unit of work, and that usage is fine; keep **Issue** for the defined concept.

**Decision ticket**:
A `wayfinder` unit — a child **Issue** of a `wayfinder:map` holding a *question* whose resolution is a decision, not a slice of a build to execute. The **decision** qualifier is what keeps it distinct from an implementation ticket; `wayfinder` introduces the term, then uses "ticket".

**Spec**:
The synthesised description of a change produced by `to-spec` — problem, solution, user stories, implementation and testing decisions. It is published to the **Issue tracker** in whichever shape that tracker supports: on local markdown, a `spec.md` in a dated feature folder under `docs/specs/` with a `Status:` line (`ready` → `in-progress` → `done`); a **Project-shaped spec** where the tracker has one; otherwise a single **Issue**. Specs are committed repo history, never moved once finished.

**Project-shaped spec**:
A **Spec** published as a container rather than an **Issue** — on Linear, a project whose overview holds the problem/solution and links to one document per remaining spec section, with the **Issues** `to-tickets` derives from it living inside the same container. A local-markdown feature folder is not project-shaped: the whole spec is one `spec.md`, with its tickets in `tickets/` beside it.
_Avoid_: epic, spec issue

**Wave**:
An ordered delivery phase grouping the **Issues** `to-tickets` produces — a checkpoint you could stop at and still have something coherent. Recorded as a `Wave:` line in each local ticket file; maps to a Linear project milestone where the tracker has them.
_Avoid_: phase, milestone (reserve "milestone" for the tracker's own object)

**Work list**:
The ordered **Issues** `implement` resolves a reference into before building anything — a **Project-shaped spec** or local feature folder expands to its **Issues** in **Wave** order, an **Issue** with children to its children, an **Issue** without them to itself.

**Frontier**:
The **Issues** in a **Work list** that are open and have no open blocker — the ones that can be started right now. `to-tickets`, `implement`, and `wayfinder` all work the frontier.

**Triage role**:
A canonical state-machine label applied to an **Issue** during triage (e.g. `needs-triage`, `ready-for-agent`). Each role maps to a real label string in the **Issue tracker** via `docs/agents/triage-labels.md`. On local markdown the ticket's `Status:` line carries the role, then moves on to the lifecycle values `in-progress` and `done`.

**Summary layer**:
A consumer repo's `CONTEXT.md` and `docs/adr/` — concise, read directly by any session before exploring.

**Spec archive**:
A consumer repo's `docs/specs/` — every past **Spec**, its tickets, and wayfinder maps. A session reads only the feature folder it was pointed at; everything else is reached through `recall`, which delegates the reading to a low-cost model and returns a short answer with file pointers.
_Avoid_: backlog, history folder

## Relationships

- An **Issue tracker** holds many **Issues**
- An **Issue** carries one **Triage role** at a time
- A **Decision ticket** is an **Issue** (a child of a `wayfinder:map`)
- A **Project-shaped spec** holds one **Spec** and the **Issues** derived from it
- An **Issue** derived from a **Spec** belongs to exactly one **Wave**
- A **Work list** is the **Issues** a reference resolves to; its **Frontier** is the subset ready to start
- The **Summary layer** is read directly; the **Spec archive** is read only through `recall`
- An ADR in the **Summary layer** may backlink the **Spec** it came from

## Flagged ambiguities

- "backlog" was previously used to mean both the *tool* hosting issues and the *body of work* inside it — resolved: the tool is the **Issue tracker**; "backlog" is no longer used as a domain term.
- "backlog backend" / "backlog manager" — resolved: collapsed into **Issue tracker**.
- "project" means both the consumer codebase a skill runs against and the Linear object a **Project-shaped spec** lives in — say "the repo"/"the codebase" for the former, and reserve bare "project" for the tracker object.
