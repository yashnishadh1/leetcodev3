"""Mark spaced-revision intervals as done and refresh the queue.

Usage:
    python src/mark_revision.py <question_id> <day|all>

Examples:
    python src/mark_revision.py 1 1      # Two Sum, day-1 review done
    python src/mark_revision.py 1 all    # every interval done
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import automation as auto  # noqa: E402


def mark(progress: dict, question_id: str, which: str) -> int:
    if which != "all" and which not in {str(d) for d in auto.REVIEW_OFFSETS}:
        raise ValueError(f"day must be 'all' or one of {auto.REVIEW_OFFSETS}")
    changed = 0
    matched = False
    for problem in progress["problems"]:
        if str(problem.get("question_id")) != str(question_id):
            continue
        matched = True
        statuses = problem.setdefault("revision_status", {})
        for key in list(statuses):
            if which in ("all", key) and statuses[key] != "done":
                statuses[key] = "done"
                changed += 1
    if not matched:
        raise ValueError(f"No tracked problem with question id {question_id}")
    return changed


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    progress = auto.load_progress()
    try:
        changed = mark(progress, argv[1], argv[2])
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    auto.PROGRESS_FILE.write_text(json.dumps(progress, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    auto.write_revision_queue(progress, dt.datetime.now(dt.timezone.utc).date())
    print(f"Marked {changed} revision(s) done and refreshed the queue.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
