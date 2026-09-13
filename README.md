# Deliberate Dev for Codex

**Turn a rough software idea into clear requirements, small tasks, and tested, reviewed changes.**

[![CI](https://github.com/Zaheer-verse/deliberate-dev-codex/actions/workflows/ci.yml/badge.svg)](https://github.com/Zaheer-verse/deliberate-dev-codex/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Zaheer-verse/deliberate-dev-codex)](https://github.com/Zaheer-verse/deliberate-dev-codex/releases)
[![License](https://img.shields.io/github/license/Zaheer-verse/deliberate-dev-codex)](LICENSE)

[Quick start](#quick-start) · [Workflow](#workflow) · [Skills](#six-skills) · [Contributing](CONTRIBUTING.md) · [Claude Code edition](https://github.com/Zaheer-verse/deliberate-dev-claude)

AI agents can start changing code before the problem is understood, let unrelated tasks collide, or finish without checking the integrated result. Deliberate Dev gives Codex a disciplined path: clarify the request, define observable outcomes, isolate work, write tests first, and review the result before delivery.

The plugin has six skills and two local Python helpers. It uses Git and Python's standard library; it needs no API key, server, or third-party Python package.

## Quick start

Add this repository as a Codex marketplace, then install the plugin:

```sh
codex plugin marketplace add Zaheer-verse/deliberate-dev-codex
codex plugin add deliberate-dev@deliberate-dev-codex
```

Start a new Codex task in your software project and enter:

```text
Use $deliberate-dev to help me build a booking system for a tutoring business.
```

The main skill coordinates the other five. It asks focused questions about **what**, **why**, and **who** whenever material answers are missing.

For a downloaded release or local clone, use its absolute path in the first command instead of `Zaheer-verse/deliberate-dev-codex`. Publishing this repository makes a marketplace source available; it does not place the plugin in an official curated directory. See the [Codex plugin documentation](https://learn.chatgpt.com/docs/plugins) for current installation details.

## Workflow

```mermaid
flowchart LR
    A[Clarify request] --> B[Plan small tasks]
    B --> C[Separate Git worktree]
    C --> D[Write and run failing tests]
    D --> E[Implement and run checks]
    E --> F[Correctness, security, quality review]
    F -->|Findings| E
    F -->|Passed| G[Integrate reviewed commits]
    G --> H[Combined tests and final review]
```

Every task maps to acceptance criteria, owns a defined scope, and begins from an explicit Git baseline. Dependent work starts from reviewed prerequisite revisions.

## Six skills

| Skill | Purpose |
| --- | --- |
| `deliberate-dev` | Coordinates the full workflow and final integration gate |
| `clarify-request` | Turns an idea into a brief and observable acceptance criteria |
| `plan-tasks` | Splits requirements into small tasks with dependencies and ownership |
| `test-first` | Guides red, green, refactor and records actual test evidence |
| `isolated-worktrees` | Plans or creates a separate branch and checkout for each task |
| `review-delivery` | Reviews correctness, security, and quality before delivery |

You can ask Codex to use an individual skill, for example `$clarify-request`.

## Example

**Request:** “Build a booking system.”

Discovery establishes who books, whether cancellations are allowed, and which timezone controls availability. A resulting requirement might say: customers reserve tutoring slots, a tutor cannot receive overlapping bookings, and cancellation reopens a slot.

| Task | Test written first |
| --- | --- |
| Define availability | Overlapping intervals are rejected; adjacent slots are allowed |
| Reserve a slot | Two requests cannot both reserve the same slot |
| Cancel a booking | Cancelling an active booking makes its slot available |

Each task runs in its own worktree. The reservation task starts from the reviewed availability revision. Combined checks run after reviewed commits are integrated.

## Requirements and checks

- Codex with plugin support and access to the target project.
- Python 3.10+, Git 2.36+, and the project's test tools.
- A Git repository with a committed baseline, clean checkout, and writable sibling directory for worktrees and private run records.

```sh
python -m unittest discover -s tests -v
python scripts/workflow.py check examples/plan.json --stage plan
python scripts/workflow.py --help
python scripts/worktrees.py --help
```

`workflow.py` checks a coordinator's evidence record. `worktrees.py` defaults to a dry run; pass `--apply` only after inspecting the plan. Read [workflow format](docs/workflow-format.md), [worktree CLI](docs/worktrees-cli.md), and the [brief](skills/deliberate-dev/assets/brief.md), [task](skills/deliberate-dev/assets/task.md), and [review](skills/deliberate-dev/assets/review.md) templates.

## Boundaries

Skills guide an agent; they cannot enforce every edit or guarantee compliance. The evidence checker validates record structure and consistency, not the truth of claimed command output. Compare records against real Git state and test output.

Independent review requires subagents. When unavailable, the agent performs sequential role passes and should disclose self-review. The plugin does not guarantee secure application code, merge or deploy changes, or replace host permission controls.

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), [CHANGELOG.md](CHANGELOG.md), and [LICENSE](LICENSE). This is an independent community project, not an official OpenAI plugin.
