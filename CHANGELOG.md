# Changelog

## 0.1.1

- Reject invalid UTF-8 in local Git configuration before filter inspection can invoke a configured checkout filter.
- Canonicalize the default worktree root so Windows short-path aliases cannot make a valid plan look inconsistent.

## 0.1.0

Initial public release.

- Six skills for discovery, task planning, test-first implementation, isolated Git worktrees, review, and delivery.
- Standard-library Python helpers for validating workflow evidence and creating task worktrees.
- Templates, an example plan, and automated behavioral, integration, and package tests.
