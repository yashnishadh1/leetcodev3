"""Run generated Python solutions against generated test cases.

Generated code is untrusted, so it runs in a separate isolated interpreter
(`python -I`) with an empty environment (no API keys), a temp working
directory, a memory limit and a timeout. Only simple literal inputs are
supported; linked-list / tree style inputs are skipped, not failed.
"""
from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

_FAIL = object()
_ARG = re.compile(r"(?:^|,\s*)([A-Za-z_]\w*)\s*=\s*")

PRELUDE = (
    "from typing import *\n"
    "import collections, heapq, bisect, math, itertools, functools, string, re, random\n"
    "from collections import *\nfrom itertools import *\nfrom functools import *\n"
    "from heapq import *\nfrom bisect import *\nfrom math import *\n\n"
)

HARNESS = r'''
import json, os, sys
try:
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (1 << 30, 1 << 30))
except Exception:
    pass

real_stdout = sys.stdout
sys.stdout = open(os.devnull, "w")

def norm(x):
    if isinstance(x, tuple):
        x = list(x)
    if isinstance(x, set):
        x = sorted(x, key=repr)
    if isinstance(x, list):
        return [norm(i) for i in x]
    return x

def eq(a, b):
    a, b = norm(a), norm(b)
    if isinstance(a, float) or isinstance(b, float):
        try:
            return abs(a - b) <= 1e-5
        except Exception:
            return False
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(eq(x, y) for x, y in zip(a, b))
    return a == b

def deep_sort(x):
    x = norm(x)
    if isinstance(x, list):
        return sorted((deep_sort(i) for i in x), key=lambda v: json.dumps(v, sort_keys=True, default=repr))
    return x

ns = {"__name__": "solution"}
exec(compile(open("full.py").read(), "solution.py", "exec"), ns)
Solution = ns["Solution"]
obj = Solution()
names = [n for n, f in vars(Solution).items() if callable(f) and not n.startswith("_")]
cases = json.load(open("cases.json"))

def pick(args):
    import inspect
    wanted = set(args) if isinstance(args, dict) else None
    count = len(args)
    best = None
    for n in names:
        params = [p for p in inspect.signature(getattr(obj, n)).parameters]
        if wanted is not None and set(params) == wanted:
            return n
        if best is None and len(params) == count:
            best = n
    return best or names[0]

results = []
for case in cases:
    args, expected = case["args"], case["expected"]
    try:
        fn = getattr(obj, pick(args))
        got = fn(**args) if isinstance(args, dict) else fn(*args)
        shown = None
        if got is None and expected is not None:  # in-place problems
            got = list(args.values())[0] if isinstance(args, dict) else args[0]
            shown = "None (first argument after the call: " + repr(got)[:120] + ")"
        if eq(got, expected):
            status = "pass"
        elif isinstance(norm(got), list) and isinstance(norm(expected), list) and deep_sort(got) == deep_sort(expected):
            status = "unordered"
        else:
            status = "fail"
        results.append({"status": status, "got": shown or repr(got)[:160]})
    except Exception as exc:
        results.append({"status": "error", "got": f"{type(exc).__name__}: {exc}"[:160]})

real_stdout.write(json.dumps(results))
'''


def to_value(raw: str) -> Any:
    raw = raw.strip()
    if not raw:
        return _FAIL
    try:
        return json.loads(raw)
    except ValueError:
        pass
    try:
        return ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        return _FAIL


def parse_args(text: str) -> dict[str, Any] | list[Any] | None:
    """'nums = [2,7], target = 9' -> {'nums': [2, 7], 'target': 9}; '[2,7], 9' -> [[2, 7], 9]."""
    text = text.strip()
    matches = list(_ARG.finditer(text))
    if matches and matches[0].start() == 0:
        args: dict[str, Any] = {}
        for i, m in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            value = to_value(text[m.end():end])
            if value is _FAIL:
                return None
            args[m.group(1)] = value
        return args
    try:
        parsed = json.loads("[" + text + "]")
    except ValueError:
        return None
    return parsed or None


def empty_report() -> dict[str, Any]:
    return {"ran": False, "total": 0, "passed": 0, "unordered": 0, "failed": 0, "errors": 0, "skipped": 0, "details": []}


def run_python_tests(code: str, test_cases: Any, timeout: int = 30) -> dict[str, Any]:
    report = empty_report()
    if not isinstance(test_cases, list):
        return report
    cases = []
    for tc in test_cases:
        if not isinstance(tc, dict):
            continue
        args = parse_args(str(tc.get("input", "")))
        expected = to_value(str(tc.get("expected", "")))
        if args is None or expected is _FAIL or "Node" in str(tc.get("input", "")):
            report["skipped"] += 1
            continue
        cases.append({"args": args, "expected": expected, "label": str(tc.get("input", ""))[:80]})
    report["total"] = len(cases)
    if not cases:
        return report

    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "full.py").write_text(PRELUDE + code, encoding="utf-8")
        Path(tmp, "cases.json").write_text(json.dumps(cases), encoding="utf-8")
        Path(tmp, "harness.py").write_text(HARNESS, encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, "-I", "harness.py"], cwd=tmp, env={},
                capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            report["ran"] = True
            report["errors"] = len(cases)
            report["details"].append(f"Timed out after {timeout}s (possible infinite loop or very slow code)")
            return report

    report["ran"] = True
    try:
        results = json.loads(proc.stdout)
    except ValueError:
        report["errors"] = len(cases)
        tail = (proc.stderr or "no output").strip().splitlines()[-1:] or ["no output"]
        report["details"].append("Harness failed: " + tail[0][:200])
        return report

    for case, res in zip(cases, results):
        status = res["status"]
        key = {"pass": "passed", "unordered": "unordered", "fail": "failed", "error": "errors"}[status]
        report[key] += 1
        if status != "pass":
            report["details"].append(f"{status}: input {case['label']} -> got {res['got']}, expected {case['expected']!r}"[:300])
    return report


def summarize(report: dict[str, Any] | None) -> str:
    if not report or not report.get("ran"):
        return "not run (no parsable test cases)"
    ok = report["passed"] + report["unordered"]
    parts = [f"{ok}/{report['total']} passed"]
    if report["unordered"]:
        parts.append(f"{report['unordered']} only with different order")
    if report["failed"]:
        parts.append(f"{report['failed']} failed")
    if report["errors"]:
        parts.append(f"{report['errors']} errors")
    if report["skipped"]:
        parts.append(f"{report['skipped']} skipped")
    return ", ".join(parts)
