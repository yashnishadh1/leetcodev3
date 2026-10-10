"""Merge the userscript's exported submission log into progress/progress.json.

Usage:
    python src/import_log.py submission_log.json

Accepted -> status "solved"; any other verdict -> "attempted" (never downgrades "solved").
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import automation as auto  # noqa: E402

RANK = {"new": 0, "attempted": 1, "solved": 2}


def merge(progress: dict, entries: list) -> int:
    changed = 0
    by_slug = {p.get("slug"): p for p in progress["problems"]}
    for e in entries:
        problem = by_slug.get(e.get("slug"))
        if not problem:
            continue
        history = problem.setdefault("submissions", [])
        if any(h.get("ts") == e.get("ts") for h in history):
            continue  # already imported
        history.append({k: e.get(k) for k in ("ts", "date", "language", "verdict")})
        new = "solved" if str(e.get("verdict", "")).strip() == "Accepted" else "attempted"
        if RANK[new] > RANK.get(problem.get("status", "new"), 0):
            problem["status"] = new
        changed += 1
    return changed


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    entries = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    progress = auto.load_progress()
    changed = merge(progress, entries)
    auto.PROGRESS_FILE.write_text(json.dumps(progress, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    auto.write_revision_queue(progress, dt.datetime.now(dt.timezone.utc).date())
    print(f"Imported {changed} new submission record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
