#!/usr/bin/env python3
"""Drift check: do the local act files cover what .github/workflows references?

Run from a repo root. Exit 0 = in sync, 1 = drift, 2 = no workflows.
Prints secret/var NAMES only, never values. Stdlib only (regex, not a YAML parser:
good enough for the keys we look at; expressions are reported, not evaluated).
"""
import json
import platform
import re
import subprocess
import sys
from pathlib import Path

ACT_UNRUNNABLE = re.compile(r"^(macos|windows)", re.I)
REF = re.compile(r"\b(secrets|vars)\.([A-Za-z_][A-Za-z0-9_]*)")
RUNS_ON = re.compile(r"^\s*runs-on:\s*(.+?)\s*$", re.M)
PROVIDED = {"GITHUB_TOKEN"}  # passed per run with -s GITHUB_TOKEN="$(gh auth token)"
GENERATED = re.compile(r"auto-?generated|this (code|file) was generated|do not (edit|modify)", re.I)
HOST_FLAGS = re.compile(r"--(artifact-server-path|cache-server-path|bind|container-options)\b")


def keys(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    out = set()
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            out.add(line.split("=", 1)[0].removeprefix("export ").strip())
    return out


def mapped_labels(actrc: Path) -> set[str]:
    if not actrc.is_file():
        return set()
    return set(re.findall(r"(?:-P|--platform)[ =]+([^=\s]+)=", actrc.read_text()))


def labels(raw: str) -> list[str]:
    raw = raw.split("#", 1)[0].strip()
    if raw.startswith("["):
        return [x.strip().strip("'\"") for x in raw.strip("[]").split(",") if x.strip()]
    return [raw.strip("'\"")]


def triggers(text: str) -> list[str]:
    m = re.search(r"^(?:on|\"on\"|'on'):[ \t]*(.*)$", text, re.M)
    if not m:
        return []
    inline = m.group(1).split("#", 1)[0].strip()
    if inline:
        return labels(inline)
    block = re.split(r"^\S", text[m.end():], maxsplit=1, flags=re.M)[0]  # up to next top-level key
    return re.findall(r"^  ([a-z_]+):", block, re.M)


def matrix_os(text: str) -> list[str]:
    # ponytail: file-wide, not per job — a matrix.os list anywhere counts for every ${{ matrix.os }}.
    return [l for raw in re.findall(r"^\s*os:\s*(\[.*\])", text, re.M) for l in labels(raw)]


def gitignored(root: Path, name: str) -> bool:
    r = subprocess.run(["git", "-C", str(root), "check-ignore", "-q", name], capture_output=True)
    return r.returncode == 0


def check(root: Path) -> dict:
    wf_dir = root / ".github" / "workflows"
    files = sorted(list(wf_dir.glob("*.yml")) + list(wf_dir.glob("*.yaml"))) if wf_dir.is_dir() else []
    mapped = mapped_labels(root / ".actrc")
    have_secrets, have_vars = keys(root / ".secrets"), keys(root / ".vars")
    report = {"workflows": [], "drift": []}
    for f in files:
        text = f.read_text()
        refs = REF.findall(text)
        secrets = sorted({n for k, n in refs if k == "secrets"})
        vars_ = sorted({n for k, n in refs if k == "vars"})
        runs = {l for raw in RUNS_ON.findall(text) for l in labels(raw)}
        if "${{ matrix.os }}" in runs:
            expanded = matrix_os(text)
            runs = (runs - {"${{ matrix.os }}"}) | set(expanded) if expanded else runs
        runs = sorted(runs)
        w = {
            "file": str(f.relative_to(root)),
            "triggers": triggers(text),
            "runs_on": runs,
            "github_only": [l for l in runs if ACT_UNRUNNABLE.match(l)],
            "expression_labels": [l for l in runs if "${{" in l],
            "unmapped": [l for l in runs if "${{" not in l and not ACT_UNRUNNABLE.match(l)
                         and l != "self-hosted" and l not in mapped],
            "missing_secrets": [s for s in secrets if s not in have_secrets and s not in PROVIDED],
            "missing_vars": [v for v in vars_ if v not in have_vars],
            "oidc": bool(re.search(r"id-token:\s*write", text)),
            "reusable_remote": sorted(set(re.findall(r"uses:\s*([\w.-]+/[\w.-]+/\.github/workflows/\S+)", text))),
            "generated": bool(GENERATED.search("\n".join(text.splitlines()[:15]))),
        }
        report["workflows"].append(w)
        for key in ("unmapped", "missing_secrets", "missing_vars"):
            for item in w[key]:
                report["drift"].append(f"{w['file']}: {key.replace('_', ' ')}: {item}")
    if (root / ".secrets").exists() and not gitignored(root, ".secrets"):
        report["drift"].append(".secrets exists but is NOT gitignored")
    elif any(w["missing_secrets"] for w in report["workflows"]) and not gitignored(root, ".secrets"):
        report["drift"].append(".secrets is not in .gitignore (add it before creating the file)")
    actrc = (root / ".actrc").read_text() if (root / ".actrc").is_file() else ""
    for flag in sorted(set(HOST_FLAGS.findall(actrc))):
        report["drift"].append(f".actrc sets {flag}: act ignores host-path flags in a project .actrc "
                               "— pass it on the command line or in ~/.actrc")
    if platform.machine() == "arm64" and "linux/amd64" in actrc:
        report["drift"].append(".actrc forces linux/amd64 on Apple Silicon: breaks node after setup-* "
                               "actions and runs ~4.5x slower — run natively")
    return report


def main() -> int:
    root = Path.cwd()
    report = check(root)
    if not report["workflows"]:
        print("no .github/workflows/*.yml here — run from the repo root", file=sys.stderr)
        return 2
    if "--json" in sys.argv:
        print(json.dumps(report, indent=2))
    else:
        for w in report["workflows"]:
            print(f"{w['file']}  on={','.join(w['triggers']) or '?'}  runs-on={','.join(w['runs_on']) or '?'}")
            for label, key in (("GitHub-only (act can't run)", "github_only"),
                               ("expression runs-on, check matrix", "expression_labels"),
                               ("remote reusable workflow", "reusable_remote")):
                if w[key]:
                    print(f"  note  {label}: {', '.join(w[key])}")
            if w["generated"]:
                print("  note  generated file — edit its generator (Nuke/Cake/projen…), not the YAML")
            if w["oidc"]:
                print("  note  id-token: write (OIDC) — guard publish/deploy steps with !env.ACT")
        print()
        print("in sync" if not report["drift"] else "DRIFT:\n  " + "\n  ".join(report["drift"]))
    return 1 if report["drift"] else 0


if __name__ == "__main__":
    sys.exit(main())
