# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML/CSS: one self-contained `site/index.html`, no build step, deployed to GitHub Pages by a
workflow in this repository. English only.

## Users

Developers who use GitHub Actions and Claude Code, and who either pay for Actions minutes, have run
out of the free quota (private repositories on a free plan), or are tired of pushing commits just to
find out whether a workflow passes. They evaluate the page in a few minutes, usually arriving from a
link, and decide whether to install the skill.

## Product Purpose

`local-ci` is a Claude Code skill that runs a repository's GitHub Actions workflows on the
developer's own machine with nektos/act (Docker / OrbStack), and keeps the local setup in sync with
`.github/workflows`. Success: the user catches red builds before pushing, spends fewer GitHub
minutes, and never maintains a second copy of their pipeline.

## Positioning

The workflow YAML stays the single source of truth. The skill does not translate workflows into
another CI format or a hand-written script (the measured failure mode without it: an agent wrote
`scripts/ci-local.sh`, a copy of the CI steps that must be updated by hand). "Keeping the two in
sync" is reduced to a mechanical drift check (`act_drift.py`) over a small local configuration:
image mapping, secrets, vars, event payloads.

## Operating Context

- Installed as a Claude Code plugin: `/plugin marketplace add Atypical-Consulting/local-ci`, then
  `/plugin install local-ci@local-ci`.
- Requires act and a running Docker engine; the drift check is Python 3 stdlib.
- Works one repository at a time.
- Saving minutes requires the user to change GitHub triggers themselves; branch protection,
  automerge and merge tooling read only GitHub's checks.

## Capabilities and Constraints

- Drift check reports: triggers, unmapped `runs-on` labels, GitHub-only jobs (macOS/Windows),
  missing secrets/vars, OIDC, `.secrets` not gitignored, host-path flags in a project `.actrc`,
  forced amd64 on Apple Silicon, generated workflow files.
- Measured act limitations (act 0.2.97): no macOS/Windows jobs; no OIDC; `upload-artifact@v4+`
  rejected by act's artifact server (`unknown field "mime_type"`); `--container-architecture
  linux/amd64` on Apple Silicon breaks node after `setup-dotnet` and is ~4.5× slower (format step
  7.6 s native vs 34 s emulated); same-job concurrent runs collide by container name.
- Licence: MIT. Author: Philippe Matray, Atypical Consulting.

## Brand Commitments

- Atypical Consulting palette: Ink `#24292e`, Cream `#fcfaf4`, Coral `#fd9b83` (charter accents
  Gold `#f1c362`, Green `#38d084`, Blue `#549dfa`, Violet `#837dfb` available; two or three per
  composition, never all).
- Illustration is flat, never photorealistic; no generated human portraits.
- Voice: first person, Philippe's ("I built this because…"), as in his articles on
  atypical.consulting. Integrity first: no invented fact, figure, quote or anecdote.
- Credit and link to https://www.atypical.consulting.

## Evidence on Hand

- Origin story (confirmed for publication): the Atypical-Consulting GitHub organisation, on the free
  plan, exhausted its Actions quota; jobs on its private repositories then failed with 0 steps in
  3–4 seconds, unrelated to the code.
- Evaluation, one run per configuration on three public repositories (x402-dotnet, TaLibStandard,
  PipeException), graded on objective checks: with skill vs without — 6/6 vs 2/6 (set up local CI),
  9/9 vs 7/9 (re-sync after a workflow edit), 7/7 vs 7/7 (run the PR workflow). Small sample; must be
  presented as such.
- No testimonials, users, star counts or adoption figures exist. Do not fabricate any.

## Product Principles

1. One source of truth: never a second pipeline.
2. Measured, not assumed: every limitation on the page was reproduced.
3. Honest about the trade-off: local green is invisible to GitHub; cutting triggers is the user's
   decision.
4. Ask before touching what GitHub runs.

## Accessibility & Inclusion

WCAG 2.2 AA. The company's mission is inclusion of neurodivergent developers: calm, uncluttered,
predictable reading order, no motion the visitor did not ask for.
