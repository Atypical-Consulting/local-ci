# local-ci

Run your GitHub Actions workflows on your own machine, and keep the local setup in sync with
`.github/workflows`. One workflow file, no second pipeline.

A [Claude Code](https://claude.com/claude-code) skill built on [nektos/act](https://github.com/nektos/act).
Page: **https://atypical-consulting.github.io/local-ci/**

## Install

```text
/plugin marketplace add Atypical-Consulting/local-ci
/plugin install local-ci@local-ci
```

Requires [act](https://nektosact.com) and a running Docker engine (OrbStack or Docker Desktop).
Then, in any repository: *"set up local CI for this repo"*.

## How it works

The workflow YAML stays the single source of truth. act runs it in Docker; the only local files are
the ingredients act needs:

| File | Commit it? | Purpose |
|---|---|---|
| `.actrc` | yes | one image per `runs-on` label |
| `.vars` | yes, if nothing sensitive | values for `${{ vars.* }}` |
| `.secrets` | **never** (gitignored) | values for `${{ secrets.* }}`; an empty value marks a secret you deliberately don't have locally |
| `.github/act/<event>.json` | yes | event payloads |

`skills/local-ci/scripts/act_drift.py` (Python 3 stdlib) checks those files against what the
workflows reference and exits 1 on drift: unmapped `runs-on` labels, GitHub-only jobs, missing
secrets and vars, OIDC, `.secrets` not gitignored, host-path flags in a project `.actrc`, forced
amd64 on Apple Silicon, generated workflow files. It prints names, never secret values.

```bash
python3 skills/local-ci/scripts/act_drift.py          # from a repository root
python3 skills/local-ci/scripts/act_drift.py --json
```

## Known act limitations (act 0.2.97, measured)

- macOS and Windows jobs cannot run (Linux containers only).
- No OIDC: publishing and cloud login stay on GitHub.
- `upload-artifact@v4+` is rejected by act's artifact server (`unknown field "mime_type"`).
- `--container-architecture linux/amd64` on Apple Silicon breaks node after `setup-dotnet` and runs
  ~4.5× slower; run natively.
- Two runs of the same job collide (containers are named by workflow + job).

## Results

Three tasks on three public repositories, one run each with and without the skill, graded on fixed
checks ([evals/evals.json](evals/evals.json)): 6/6 vs 2/6 (set up local CI), 9/9 vs 7/9 (re-sync
after a workflow edit), 7/7 vs 7/7 (run the PR workflow). A small sample.

## Saving minutes

Running act locally saves money only if GitHub runs less, and branch protection, required checks
and automerge read only GitHub's checks. The skill never changes your triggers; it proposes options
from gentlest (`concurrency: cancel-in-progress`, `paths-ignore`) to last resort (dropping
`pull_request`).

## License

MIT © Philippe Matray, [Atypical Consulting](https://www.atypical.consulting).
