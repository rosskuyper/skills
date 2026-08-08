# Agent Skills

A collection of agent skills (slash commands and behaviors) loaded by Claude Code. Skills are organized into buckets and consumed by per-repo configuration emitted by `/setup-skills`.

## Language

**Issue tracker**:
The tool that hosts a repo's issues — GitHub Issues, Linear, a local `.scratch/` markdown convention, or similar. Skills like `to-tickets`, `to-spec`, and `triage` read from and write to it.
_Avoid_: backlog manager, backlog backend, issue host

**Issue**:
A single tracked unit of work inside an **Issue tracker** — a bug, task, spec, or slice produced by `to-tickets`.
_Avoid_: ticket (use only when quoting external systems that call them tickets, or for a **Decision ticket** — see below)

**Decision ticket**:
A `wayfinder` unit — a child **Issue** of a `wayfinder:map` holding a *question* whose resolution is a decision, not a slice of a build to execute. The **decision** qualifier is what keeps it distinct from an implementation ticket; `wayfinder` introduces the term, then uses "ticket".

**Spec**:
The synthesised description of a change produced by `to-spec` — problem, solution, user stories, implementation and testing decisions. It is published to the **Issue tracker** in whichever shape that tracker supports: a **Project-shaped spec** where there is one, otherwise a single **Issue**.

**Project-shaped spec**:
A **Spec** published as a container rather than an **Issue** — on Linear, a project whose overview holds the problem/solution and links to one document per remaining spec section, with the **Issues** `to-tickets` derives from it living inside the same container.
_Avoid_: epic, spec issue

**Wave**:
An ordered delivery phase grouping the **Issues** `to-tickets` produces — a checkpoint you could stop at and still have something coherent. Maps to a Linear project milestone where the tracker has them.
_Avoid_: phase, milestone (reserve "milestone" for the tracker's own object)

**Triage role**:
A canonical state-machine label applied to an **Issue** during triage (e.g. `needs-triage`, `ready-for-afk`). Each role maps to a real label string in the **Issue tracker** via `docs/agents/triage-labels.md`.

## Relationships

- An **Issue tracker** holds many **Issues**
- An **Issue** carries one **Triage role** at a time
- A **Decision ticket** is an **Issue** (a child of a `wayfinder:map`)
- A **Project-shaped spec** holds one **Spec** and the **Issues** derived from it
- An **Issue** derived from a **Spec** belongs to exactly one **Wave**

## Flagged ambiguities

- "backlog" was previously used to mean both the *tool* hosting issues and the *body of work* inside it — resolved: the tool is the **Issue tracker**; "backlog" is no longer used as a domain term.
- "backlog backend" / "backlog manager" — resolved: collapsed into **Issue tracker**.
- "project" means both the consumer codebase a skill runs against and the Linear object a **Project-shaped spec** lives in — say "the repo"/"the codebase" for the former, and reserve bare "project" for the tracker object.
