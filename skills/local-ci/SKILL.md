---
name: local-ci
description: Run a repository's GitHub Actions workflows locally with nektos/act (Docker/OrbStack) instead of paying for GitHub-hosted minutes, and keep the local setup in sync with .github/workflows. Use this skill whenever the user wants to run CI locally, test a workflow before pushing, avoid or cut GitHub Actions cost/quota ("quota épuisé", "minutes", "billing"), set up act, mirror or copy GitHub workflows to a local CI, debug a workflow without push-and-pray, or check that their local CI still matches the GitHub one after a workflow changed — even if they never say "act". Works one repository at a time.
---

# local-ci — GitHub Actions, run on this machine

The idea: **the workflow YAML in `.github/workflows/` stays the single source of truth.** We do not
translate it into another CI format, because two definitions of the same pipeline drift the moment
someone edits one of them. `act` executes the real YAML in Docker containers, so "keeping the two
systems in sync" reduces to keeping a small amount of *local configuration* (image mapping,
secrets, variables, event payloads) consistent with what the workflows reference — and that is
checkable mechanically with `scripts/act_drift.py`.

## Workflow

### 1. Preflight

```bash
command -v act || brew install act          # nektos/act
docker info >/dev/null && echo docker-ok    # OrbStack / Docker Desktop must be running
ls .github/workflows/
```

Read every workflow file before configuring anything — you need to know the triggers, the
`runs-on` labels, and which secrets/vars each job touches.

### 2. Run the drift check first

```bash
python3 <skill-dir>/scripts/act_drift.py            # from the repo root; exit 1 = drift
python3 <skill-dir>/scripts/act_drift.py --json     # machine-readable
```

It reports, per workflow: triggers, `runs-on` labels without an image mapping, labels act cannot
run at all (macOS/Windows), secrets and vars referenced but absent from the local files, OIDC
(`id-token: write`), and whether `.secrets` is gitignored. It prints key **names**, never values.
Use its output as your to-do list for step 3, and re-run it at the end — a clean exit is the
definition of "in sync".

### 3. Create the local configuration (only what the check asks for)

All files live at the repo root, next to `.github/`:

| File | Commit it? | Purpose |
|---|---|---|
| `.actrc` | yes | image mapping only (see below for why nothing else) |
| `.vars` | yes, if nothing sensitive | `KEY=value` for `${{ vars.KEY }}` |
| `.secrets` | **never** — add to `.gitignore` first | `KEY=value` for `${{ secrets.KEY }}` |
| `.github/act/<event>.json` | yes | event payloads (`pull_request`, `push`, `workflow_dispatch` inputs) |

The project `.actrc` should map the labels the drift check lists, and nothing more:

```
-P ubuntu-latest=catthehacker/ubuntu:act-latest
-P ubuntu-24.04=catthehacker/ubuntu:act-24.04
```

- **`-P` mappings**: act needs a Docker image per `runs-on` label. The `catthehacker/*:act-*`
  images carry node, git and common tooling, but **not** .NET, Java, etc. — GitHub's runners do.
  If a job calls `dotnet` without an `actions/setup-dotnet` step, it passes on GitHub only by luck
  of the runner image; the right fix is to add the setup step to the workflow (a real fix that
  also pins the SDK on GitHub, so ask), not to switch to the `full-*` images (tens of GB).
- **No host-path flags in the project file.** Recent act refuses flags that reach host resources
  (`--artifact-server-path`, `--cache-server-path`, binds…) when they come from a repo's `.actrc`
  — it prints a warning and ignores them, because a cloned repo should not decide what touches
  your disk. Put them on the command line or in the user's `~/.actrc`. Don't reach for
  `--trust-project-actrc` to silence it.
- **No `--container-architecture linux/amd64` on Apple Silicon.** It sounds faithful to GitHub's x64
  runners, but measured: it breaks every JavaScript action after `setup-dotnet` (`node: executable
  file not found` — the image's arm64 PATH gets reapplied) and runs ~4.5× slower. Run natively;
  add `linux/amd64` for one job only if it ships x64-only binaries, and say so.

**Secrets you know about but deliberately don't have locally** (a Codecov token, an RPC URL, a
publish key): write the name with an **empty value**, `CODECOV_TOKEN=`. On GitHub an empty and an
unset secret behave the same, so this changes no step's behaviour — but it records the decision,
and the drift check counts the name as covered. That is what "in sync" means for a secret.

**`GITHUB_TOKEN`** is not provided automatically. Pass it per run rather than storing it:
`act -s GITHUB_TOKEN="$(gh auth token)" …`. Do not write a personal token into `.secrets` unless
the user asks — it is a long-lived credential sitting in a plain file.

**Secrets the user must supply**: list the missing names from the drift check and ask for them.
Never invent placeholder values that make a step "pass" — a fake API key turns a real failure
into a misleading green.

### 4. Run it

```bash
act -l                                   # list jobs per event — sanity check the mapping
act -n                                   # dry run: validates the plan without containers
act pull_request -e .github/act/pull_request.json \
    --artifact-server-path "$HOME/.cache/act-artifacts"   # what a PR would run
act push                                 # what a push to the default branch would run
act -j <job-id>                          # one job
act -W .github/workflows/ci.yml          # one workflow
```

Add `--pull=false` once the image is local (otherwise act re-checks a multi-GB image each run).

**One act run of a given job at a time.** act names containers after workflow + job, so a second
run of the same job — another terminal, another agent, another clone of the same repo — removes
the first one's container mid-step (exit 137, looks like an OOM kill). Concurrent runs of
*different* repos also fight over the default artifact/cache ports; give each its own
`--artifact-server-port` / `--cache-server-port`. If a container dies with 137, check
`docker ps` for a twin before suspecting the code.

**act keeps a failed job's container running** — and with the artifact-upload limitation below,
most jobs "fail" locally, so they pile up. Clean up after yourself, but only your own: check
`docker inspect -f '{{.Config.WorkingDir}}' <name>` points at this repo before `docker rm -f` —
another session's run of another repo uses the same `act-` prefix.

Judge the result like a real CI run: read the failing step's log. Then classify every failure as
one of three, because they lead to different fixes:

1. **Real failure** — the code or test is broken. Same answer GitHub would give; fix the code.
2. **act limitation** — something GitHub provides that act cannot (see the table below). Make the
   workflow tolerate local runs with a guard, keeping GitHub behaviour unchanged:
   `if: ${{ !env.ACT }}` on the step (act sets `ACT=true`). Never weaken the step for GitHub.
3. **Local config gap** — missing image, secret, var, or event field. Fix the local files.

Only (2) justifies editing a workflow, and the edit must be a no-op on GitHub. Mention each such
guard to the user: a guarded step is a step the local run no longer checks. Ask before adding
one — it is still an edit to a file GitHub runs.

**Check whether the workflow is generated before editing it.** Nuke (`[GitHubActions(...)]` in
`build/Build.cs`), Cake, projen and similar tools write `.github/workflows/*.yml` from code; the
drift check flags files with a "generated" header. A hand-added guard there is erased at the next
regeneration. Make the change in the generator's source, or tell the user why you didn't.

A job that is green on every code step and red only on an act-limitation step (artifact upload
is the usual one) **is a pass** for the question "would this pass on GitHub" — report it that way,
naming the step, rather than as a failure.

### Known act limitations

| GitHub feature | Under act | What to do |
|---|---|---|
| `runs-on: macos-*` / `windows-*` | cannot run (Linux containers only) | report as "GitHub-only job"; run the Linux jobs locally |
| `permissions: id-token: write` (OIDC: NuGet Trusted Publishing, cloud login) | no OIDC provider | guard the publish/deploy step with `!env.ACT`; local CI is for build/test, not release |
| `services:` containers | supported, but networking differs | usually works; if not, check hostnames (`localhost` vs service name) |
| `actions/upload-artifact@v4+` / `download-artifact` | act 0.2.97's built-in artifact server rejects `CreateArtifact` from recent upload-artifact versions (`unknown field "mime_type"`, surfacing as ECONNRESET after retries), even with `--artifact-server-path` set; reproduced on two repos | classify as act limitation; the files were produced by the earlier step. Optionally guard with `!env.ACT` (ask) |
| `actions/cache` | built-in cache server; may warn and carry on | nothing — a cache miss only costs time |
| `github.event.*` fields | empty unless you pass `-e event.json` | write the payload fields the workflow actually reads |
| reusable workflows from other repos, private actions | need network + token | pass `-s GITHUB_TOKEN`; `--action-offline-mode` once cached |
| Matrix `runs-on: ${{ matrix.os }}` | each OS entry needs a mapping; macOS/Windows entries can't run | `--matrix os:ubuntu-latest` to run only the Linux leg |

### 5. Keep the two in sync

The workflow file changes; the local config must follow. Three habits keep that honest:

- **Re-run `act_drift.py` whenever a workflow changes** (a new secret, a new `runs-on` label, a
  new trigger). It is cheap and exits non-zero on drift.
- **Optional pre-push gate** — offer, don't impose: a `.git/hooks/pre-push` (or the repo's hook
  manager) that runs `act_drift.py` and then `act push` (or the PR event). This is where the money
  is saved: a red build caught locally is a GitHub run that never happens.
- **Changes flow one way: YAML → local files.** If something only works locally after editing the
  local config, that's fine; if it only works after editing the workflow, the edit must be a
  GitHub no-op (step 4, case 2).

### 6. Cutting GitHub minutes — say the trade-off out loud

Running act locally saves money only if GitHub runs *less*. The lever is the GitHub triggers, and
it has a cost the user must choose knowingly — do not change triggers without asking:

- Required status checks, branch protection, Renovate automerge and any tool that merges "when CI
  is green" read **GitHub's** checks. A PR with no GitHub run has **no verdict** — local green is
  invisible to them.
- Lower-risk options, from least to most invasive: keep GitHub CI but add `paths-ignore` for
  docs-only changes; add `concurrency: { group: …, cancel-in-progress: true }` so superseded runs
  stop; move heavy jobs (full matrix, macOS) to `workflow_dispatch` / nightly; and only then drop
  the `pull_request` trigger.

## Finishing

Report back in this shape:

```
local-ci: <repo>
  workflows: <n>   jobs runnable locally: <n>/<total>   GitHub-only: <list + reason>
  act result: <event> → <pass/fail per job>, failures classified (real / act-limitation / config)
  files: <created/changed, and whether .secrets is gitignored>
  drift check: clean | <remaining items>
  workflow edits: <none | each !env.ACT guard and why>
  still needed from you: <secret names, decisions on triggers>
```

Do not claim "CI passes locally" unless `act` actually ran the jobs (not just `act -n`).
