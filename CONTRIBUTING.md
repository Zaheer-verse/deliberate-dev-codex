# Contributing

Thank you for improving Deliberate Dev.

## Local checks

Use Python 3.10 or newer and Git 2.36 or newer. No third-party Python packages are required by the helpers or their tests.

```sh
python -m unittest discover -s tests -v
python scripts/workflow.py check examples/plan.json --stage plan
```

Keep changes focused. For a helper change, add a behavioral regression test that fails before the fix and passes after it. Keep the six-skill workflow, explicit worktree boundaries, and truthful evidence reporting intact.

Do not commit credentials, private briefs, local run records, worktrees, caches, or release archives. Explain the problem, the behavior after your change, test results, and any security implications in the pull request.

For larger changes, open an issue first with the user need and acceptance criteria. Report security issues privately under the instructions in [SECURITY.md](SECURITY.md).
