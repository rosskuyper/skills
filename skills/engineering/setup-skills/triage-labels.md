# Triage Labels

The skills speak in terms of five canonical triage roles. This file maps those roles to how each one is actually expressed in this repo's issue tracker.

Use **one** of the two tables below — the label-only form for GitHub, GitLab, and local markdown, or the Linear form. Delete the one that doesn't apply.

## Label-only trackers (GitHub, GitLab, local markdown)

| Canonical role    | Label in our tracker | Meaning                                  |
| ----------------- | -------------------- | ---------------------------------------- |
| `needs-triage`    | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`      | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent` | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human` | `ready-for-human`    | Requires human implementation            |
| `wontfix`         | `wontfix`            | Will not be actioned                     |

## Linear

Linear expresses these across **two** dimensions: every issue has exactly one **workflow state**, plus any number of **labels**. Two roles are states, not labels — applying them as labels is wrong and leaves the issue in the wrong state.

| Canonical role    | Mechanism  | Value in our tracker | Meaning                                  |
| ----------------- | ---------- | -------------------- | ---------------------------------------- |
| `needs-triage`    | **state**  | Triage               | Maintainer needs to evaluate this issue  |
| `needs-info`      | label      | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent` | label      | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human` | label      | `ready-for-human`    | Requires human implementation            |
| `wontfix`         | **state**  | Canceled             | Will not be actioned                     |

`needs-triage` uses Linear's native **Triage** inbox where the team has it enabled; where it doesn't, substitute a `backlog`-category state. `wontfix` is a **`canceled`**-category state, so applying it also closes the issue — there's no separate close step.

State display names are configurable per team, so the two state values above are defaults, not guarantees. Confirm them against the team's real states and correct this table if they differ.

## Both forms

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding value from the table — and on Linear, via the mechanism the table names.

Edit the value column to match whatever vocabulary you actually use.
