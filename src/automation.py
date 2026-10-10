from __future__ import annotations

import ast
import datetime as dt
import html
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path
from typing import Any

import requests

import testrunner

ROOT = Path(__file__).resolve().parents[1]
SOLUTIONS_DIR = ROOT / "solutions"
PROGRESS_DIR = ROOT / "progress"
PROGRESS_FILE = PROGRESS_DIR / "progress.json"
REVISION_FILE = PROGRESS_DIR / "REVISION_QUEUE.md"
LEETCODE_GRAPHQL = "https://leetcode.com/graphql"
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
SUPPORTED_LANGUAGES = {"python", "java", "cpp"}
REVIEW_OFFSETS = [1, 3, 7, 14, 30]
DEFAULT_WEIGHTS = {"Easy": 4.0, "Medium": 5.0, "Hard": 1.0}

SESSION = requests.Session()
SESSION.headers.update({
    "Content-Type": "application/json",
    "User-Agent": "leetcode-learning-system/1.0",
    "Referer": "https://leetcode.com/problemset/all/",
})


def env_int(name: str, default: int, minimum: int = 1, maximum: int = 5) -> int:
    try:
        return max(minimum, min(maximum, int(os.getenv(name, str(default)))))
    except ValueError:
        return default


def parse_weights() -> dict[str, float]:
    """DIFFICULTY_WEIGHTS="Easy:4,Medium:5,Hard:1" -> {"Easy": 4.0, ...}"""
    raw = os.getenv("DIFFICULTY_WEIGHTS", "").strip()
    if not raw:
        return dict(DEFAULT_WEIGHTS)
    weights: dict[str, float] = {}
    try:
        for part in raw.split(","):
            name, value = part.split(":")
            name = name.strip().title()
            if name in DEFAULT_WEIGHTS:
                weights[name] = max(0.0, float(value))
    except ValueError:
        return dict(DEFAULT_WEIGHTS)
    return weights if any(v > 0 for v in weights.values()) else dict(DEFAULT_WEIGHTS)


def fetch_question_pool() -> list[dict[str, Any]]:
    wanted = [x.strip().title() for x in os.getenv(
        "LEETCODE_DIFFICULTIES", "Easy,Medium,Hard"
    ).split(",") if x.strip()]
    wanted = [x for x in wanted if x in {"Easy", "Medium", "Hard"}] or ["Easy", "Medium", "Hard"]
    query = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int,
                                 $filters: QuestionListFilterInput) {
      problemsetQuestionList: questionList(
        categorySlug: $categorySlug, limit: $limit, skip: $skip, filters: $filters
      ) {
        total: totalNum
        questions: data {
          frontendQuestionId: questionFrontendId
          title
          titleSlug
          difficulty
          paidOnly: isPaidOnly
          topicTags { name }
        }
      }
    }
    """

    def page(limit: int, skip: int) -> dict[str, Any]:
        body = leetcode_post({
            "query": query,
            "variables": {"categorySlug": "", "limit": limit, "skip": skip, "filters": {}},
        })
        return (body.get("data") or {}).get("problemsetQuestionList") or {}

    seed = int(dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d"))
    rng = random.Random(seed)

    # Use the real catalogue size instead of a hardcoded skip range.
    try:
        total = int(page(1, 0).get("total") or 0)
    except (RuntimeError, ValueError):
        total = 0
    upper = max(0, (total or 3000) - 100)

    pool: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for _ in range(4):
        skip = rng.randint(0, upper)
        try:
            for q in page(100, skip).get("questions") or []:
                if (not q.get("paidOnly") and q.get("difficulty") in wanted
                        and q.get("titleSlug") and q.get("frontendQuestionId")):
                    pool[q["titleSlug"]] = q
        except RuntimeError as exc:
            errors.append(str(exc))
        if len(pool) >= 40:
            break
    if pool:
        return list(pool.values())
    raise RuntimeError(
        "Could not fetch eligible LeetCode questions. The unauthenticated endpoint "
        "may be rate-limited or changed. " + " | ".join(errors)
    )


def leetcode_post(payload: dict[str, Any], retries: int = 3) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            response = SESSION.post(LEETCODE_GRAPHQL, json=payload, timeout=25)
            response.raise_for_status()
            body = response.json()
            if body.get("errors"):
                raise RuntimeError("LeetCode GraphQL errors: " + json.dumps(body["errors"])[:400])
            return body
        except (requests.RequestException, ValueError, RuntimeError) as exc:
            last_error = exc
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"LeetCode request failed after {retries} attempts: {last_error}")


def fetch_details(slug: str) -> dict[str, Any]:
    query = """
    query questionContent($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId questionFrontendId title titleSlug content difficulty
        exampleTestcases topicTags { name } codeSnippets { lang langSlug code }
      }
    }
    """
    body = leetcode_post({"query": query, "variables": {"titleSlug": slug}})
    detail = (body.get("data") or {}).get("question")
    if not detail or not detail.get("content"):
        raise RuntimeError(f"No statement returned for {slug}.")
    return detail



RETRY_STATUS = {429, 500, 502, 503, 504}


def gemini_json(prompt: str) -> dict[str, Any]:
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Missing GEMINI_API_KEY GitHub Actions secret.")

    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
    url = f"{GEMINI_API_BASE}/{model}:generateContent"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.25,
        },
    }

    attempts = 5
    last_error = "unknown error"
    for attempt in range(attempts):
        try:
            response = requests.post(
                url,
                headers={"x-goog-api-key": key, "Content-Type": "application/json"},
                json=payload,
                timeout=(15, 180),
            )
            if response.status_code in RETRY_STATUS:
                last_error = f"Gemini API error {response.status_code}: {response.text[:500]}"
            elif not response.ok:
                # Non-retryable (bad key, bad model name, bad request).
                raise RuntimeError(f"Gemini API error {response.status_code}: {response.text[:800]}")
            else:
                data = response.json()
                candidates = data.get("candidates") or []
                if not candidates:
                    last_error = f"No candidates returned (promptFeedback={data.get('promptFeedback')})"
                else:
                    cand = candidates[0]
                    parts = (cand.get("content") or {}).get("parts") or []
                    text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
                    if cand.get("finishReason") == "MAX_TOKENS":
                        last_error = "Gemini output truncated (MAX_TOKENS)"
                    else:
                        try:
                            result = json.loads(text)
                        except json.JSONDecodeError as exc:
                            last_error = f"Gemini returned invalid JSON: {exc}"
                        else:
                            if isinstance(result, dict):
                                return result
                            last_error = "Gemini response must be a JSON object."
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, ValueError) as exc:
            last_error = str(exc)

        if attempt < attempts - 1:
            wait = min(15 * (2 ** attempt), 120)
            print(f"Gemini problem ({last_error[:150]}). Retry {attempt + 1}/{attempts - 1} in {wait}s.")
            time.sleep(wait)

    raise RuntimeError(f"Gemini failed after {attempts} attempts: {last_error}")


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:70] or "problem"


def load_progress() -> dict[str, Any]:
    PROGRESS_DIR.mkdir(parents=True, exist_ok=True)
    if not PROGRESS_FILE.exists():
        return {"schema_version": 1, "problems": []}
    try:
        data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("problems"), list):
            return data
    except json.JSONDecodeError:
        pass
    raise RuntimeError("progress/progress.json is invalid JSON; repair it before running.")


def existing_slugs(progress: dict[str, Any]) -> set[str]:
    seen = {p.get("slug") for p in progress["problems"] if p.get("slug")}
    for path in SOLUTIONS_DIR.glob("*-*/README.md"):
        # Directory name convention: <id>-<slug>
        seen.add(path.parent.name.split("-", 1)[1])
    return seen


def select_new_questions(pool: list[dict[str, Any]], progress: dict[str, Any], count: int) -> list[dict[str, Any]]:
    seen = existing_slugs(progress)
    seed = int(dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d"))
    rng = random.Random(seed)
    weights = parse_weights()

    # Unseen questions grouped by difficulty, shuffled deterministically per day.
    groups: dict[str, list[dict[str, Any]]] = {}
    for q in sorted(pool, key=lambda item: item.get("titleSlug", "")):
        slug = q.get("titleSlug", "")
        if slug and slug not in seen:
            groups.setdefault(q.get("difficulty", "Unknown"), []).append(q)
    for items in groups.values():
        rng.shuffle(items)

    topic_counts: Counter[str] = Counter(t for p in progress["problems"] for t in p.get("topics", []))

    def tags_of(q: dict[str, Any]) -> list[str]:
        return [t.get("name", "") for t in q.get("topicTags") or []]

    def topic_score(q: dict[str, Any]) -> float:
        tags = tags_of(q)
        return sum(topic_counts[t] for t in tags) / max(1, len(tags))

    chosen: list[dict[str, Any]] = []
    while len(chosen) < count:
        available = [d for d, items in groups.items() if items]
        if not available:
            break
        weighted = [d for d in available if weights.get(d, 0) > 0] or available
        difficulty = rng.choices(weighted, weights=[weights.get(d, 1.0) or 1.0 for d in weighted])[0]
        # Within the chosen difficulty prefer topics practised least so far.
        pick = min(groups[difficulty], key=topic_score)
        groups[difficulty].remove(pick)
        topic_counts.update(tags_of(pick))
        chosen.append(pick)
    if len(chosen) < count:
        raise RuntimeError(
            f"Only found {len(chosen)} unseen questions; need {count}. "
            "Merge prior PRs or adjust the LeetCode fetch range."
        )
    return chosen


def build_prompt(problem: dict[str, Any], languages: list[str]) -> str:
    qid = str(problem.get("questionFrontendId") or problem.get("frontendQuestionId") or problem.get("questionId"))
    title = problem["title"]
    url = f"https://leetcode.com/problems/{problem['titleSlug']}/"
    tags = ", ".join(t.get("name", "") for t in problem.get("topicTags", []))
    statement = html.unescape(problem.get("content", ""))[:18000]
    examples = str(problem.get("exampleTestcases", ""))[:5000]
    language_list = ", ".join(languages)
    return f"""
You are a patient DSA tutor. Explain in natural Hinglish (Hindi in Roman script mixed with standard English programming terms). Produce accurate, structured learning notes, not just code.

LeetCode #{qid}: {title}
Difficulty: {problem.get('difficulty', 'Unknown')}
URL: {url}
Topics: {tags or 'not provided'}

OFFICIAL STATEMENT HTML:
{statement}

EXAMPLE TESTCASES FIELD:
{examples or 'not provided'}

Return ONLY valid JSON with this structure:
{{
 "problem_summary_hinglish": "Explain the task simply in Hinglish; do not reproduce the entire statement.",
 "input_output": "Explain input, output and constraints in Hinglish.",
 "example_walkthrough": "Walk through official examples step by step.",
 "brute_force": "Naive approach, why it works, and why it may be slow.",
 "optimized_approach": "Optimized approach and intuition; explain data structures/pattern.",
 "dry_run": "Step-by-step table-like dry run on an example, showing variables/state.",
 "time_complexity": "Big-O with justification",
 "space_complexity": "Big-O with justification",
 "common_mistakes": ["mistake 1", "mistake 2"],
 "hints": ["Hint 1: gentle nudge, no answer", "Hint 2: more specific", "Hint 3: near-solution insight"],
 "quiz": [{{"question":"...", "answer":"..."}}, {{"question":"...", "answer":"..."}}],
 "test_cases": [{{"input":"...", "expected":"...", "why":"..."}}, {{"input":"...", "expected":"...", "why":"..."}}],
 "notes": "uncertainties and assumptions",
 "solutions": {{
   "python": "raw source",
   "java": "raw source",
   "cpp": "raw source"
 }}
}}

Generate solutions only for these requested languages: {language_list}. For unrequested languages use an empty string.
Rules:
- Treat the statement above as the source of truth. Do not guess if it is ambiguous; say so in notes.
- Standard LeetCode submission style; use exact method signature/return type.
- No main() unless required by the platform, no Markdown fences around source.
- Do not claim code was run or accepted.
- Ensure all generated languages implement the same algorithm and edge cases.
- Hints should be graduated and not reveal the final code.
- The user wants a full explanation, but also has an `MY_ATTEMPT.md` template for independent practice.
- Tests must match the official problem's expected input/output format as well as can be inferred from the statement.
""".strip()


CPP_PRELUDE = "#include <bits/stdc++.h>\nusing namespace std;\n"
CPP_STUBS = {
    "ListNode": "struct ListNode { int val; ListNode *next; ListNode() : val(0), next(nullptr) {} ListNode(int x) : val(x), next(nullptr) {} ListNode(int x, ListNode *next) : val(x), next(next) {} };\n",
    "TreeNode": "struct TreeNode { int val; TreeNode *left; TreeNode *right; TreeNode() : val(0), left(nullptr), right(nullptr) {} TreeNode(int x) : val(x), left(nullptr), right(nullptr) {} TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {} };\n",
}
JAVA_PRELUDE = "import java.util.*;\nimport java.util.function.*;\nimport java.util.stream.*;\n"
JAVA_STUBS = {
    "ListNode": "class ListNode { int val; ListNode next; ListNode() {} ListNode(int val) { this.val = val; } ListNode(int val, ListNode next) { this.val = val; this.next = next; } }\n",
    "TreeNode": "class TreeNode { int val; TreeNode left; TreeNode right; TreeNode() {} TreeNode(int val) { this.val = val; } TreeNode(int val, TreeNode left, TreeNode right) { this.val = val; this.left = left; this.right = right; } }\n",
}


def needed_stubs(code: str, stubs: dict[str, str]) -> str:
    out = ""
    for name, text in stubs.items():
        defined = re.search(rf"\b(class|struct)\s+{name}\b", code)
        if name in code and not defined:
            out += text
    return out


def brace_check(code: str) -> list[str]:
    return [] if code.count("{") == code.count("}") else ["Unbalanced braces"]


def run_compiler(cmd: list[str], cwd: str) -> list[str]:
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:
        return ["Compiler timed out"]
    if proc.returncode == 0:
        return []
    errors = [ln.strip() for ln in (proc.stderr or proc.stdout).splitlines() if "error" in ln.lower()]
    return ["Compile error: " + " | ".join(errors[:3])[:400]] if errors else ["Compile failed"]


def compile_check(language: str, code: str) -> list[str]:
    """Real compile check; falls back to a brace check when the toolchain is missing or disabled."""
    if os.getenv("COMPILE_CHECK", "1") != "0":
        with tempfile.TemporaryDirectory() as tmp:
            if language == "java" and shutil.which("javac"):
                Path(tmp, "Solution.java").write_text(JAVA_PRELUDE + code + "\n" + needed_stubs(code, JAVA_STUBS), encoding="utf-8")
                return run_compiler(["javac", "-d", tmp, "Solution.java"], tmp)
            if language == "cpp" and shutil.which("g++"):
                Path(tmp, "solution.cpp").write_text(CPP_PRELUDE + needed_stubs(code, CPP_STUBS) + code + "\n", encoding="utf-8")
                return run_compiler(["g++", "-std=c++17", "-fsyntax-only", "solution.cpp"], tmp)
    # Compiler disabled or missing: fall back to the cheap brace check.
    return brace_check(code) if language in {"java", "cpp"} else []


def validate_code(language: str, code: str) -> list[str]:
    issues: list[str] = []
    if not code.strip():
        return ["Missing source code"]
    if "```" in code:
        return ["Markdown fences found; expected raw source"]
    if language == "python":
        try:
            ast.parse(code)
        except SyntaxError as exc:
            issues.append(f"Python syntax error at line {exc.lineno}: {exc.msg}")
    if "class Solution" not in code:
        issues.append("Expected LeetCode-style class Solution")
    if language in {"java", "cpp"} and not issues:
        issues += compile_check(language, code)
    return issues


def build_repair_prompt(problem: dict[str, Any], pack: dict[str, Any], bad: dict[str, list[str]]) -> str:
    statement = html.unescape(problem.get("content", ""))[:8000]
    blocks = []
    for lang, found in bad.items():
        blocks.append(f"LANGUAGE: {lang}\nPROBLEMS FOUND: {'; '.join(found)}\nCURRENT CODE:\n{pack['solutions'].get(lang, '')}")
    shown = "\n\n".join(blocks)
    langs = ", ".join(bad)
    return f"""
Fix the broken LeetCode solutions below. Keep the same algorithm and the exact LeetCode method signature.

PROBLEM: {problem['title']}
STATEMENT HTML:
{statement}

{shown}

Return ONLY valid JSON: {{"solutions": {{ "<language>": "fixed raw source" }}}} containing only these languages: {langs}.
No Markdown fences. Do not add main(). Do not claim the code was run.
""".strip()


def repair_solutions(problem: dict[str, Any], pack: dict[str, Any], languages: list[str]) -> None:
    rounds = env_int("MAX_REPAIR_ROUNDS", 2, minimum=0, maximum=3)
    for attempt in range(rounds):
        bad = {}
        for lang in languages:
            code = pack["solutions"].get(lang, "")
            found = validate_code(lang, code if isinstance(code, str) else "")
            if found:
                bad[lang] = found
        if not bad:
            return
        print(f"Repair round {attempt + 1}/{rounds} for {problem['title']}: {list(bad)}")
        try:
            fixed = gemini_json(build_repair_prompt(problem, pack, bad)).get("solutions")
        except RuntimeError as exc:
            print(f"Repair request failed: {exc}")
            return
        if isinstance(fixed, dict):
            for lang in bad:
                if isinstance(fixed.get(lang), str) and fixed[lang].strip():
                    pack["solutions"][lang] = fixed[lang]


def bullets(value: Any) -> str:
    if not isinstance(value, list) or not value:
        return "- Not provided\n"
    out = []
    for item in value:
        if isinstance(item, dict) and "question" in item:
            out.append(f"- **Q:** {item.get('question', '')}\n  **A:** {item.get('answer', '')}")
        elif isinstance(item, dict) and "input" in item:
            line = f"- Input: `{item.get('input', '')}` -> Expected: `{item.get('expected', '')}`"
            if item.get("why"):
                line += f" ({item['why']})"
            out.append(line)
        elif isinstance(item, dict):
            out.append("- " + json.dumps(item, ensure_ascii=False))
        else:
            out.append("- " + str(item))
    return "\n".join(out) + "\n"


def render_lesson(problem: dict[str, Any], pack: dict[str, Any], languages: list[str], run_date: dt.date,
                  test_report: dict[str, Any] | None = None) -> dict[str, list[str]]:
    qid = str(problem.get("questionFrontendId") or problem.get("frontendQuestionId") or problem.get("questionId"))
    title = problem["title"]
    slug = problem["titleSlug"]
    difficulty = problem.get("difficulty", "Unknown")
    tags = ", ".join(t.get("name", "") for t in problem.get("topicTags", [])) or "Not provided"
    url = f"https://leetcode.com/problems/{slug}/"
    folder = SOLUTIONS_DIR / f"{qid}-{slug}"
    folder.mkdir(parents=True, exist_ok=True)

    lesson = f"""# {qid}. {title}

- **Difficulty:** {difficulty}
- **Problem:** {url}
- **Topics:** {tags}
- **Generated:** {run_date.isoformat()}

## 1. Problem ko simple Hinglish mein samjho

{pack.get('problem_summary_hinglish', 'Explanation missing.')}

## 2. Input aur output

{pack.get('input_output', 'Not provided.')}

## 3. Example walkthrough

{pack.get('example_walkthrough', 'Not provided.')}

## 4. Brute-force approach

{pack.get('brute_force', 'Not provided.')}

## 5. Optimized approach

{pack.get('optimized_approach', 'Not provided.')}

## 6. Dry run

{pack.get('dry_run', 'Not provided.')}

## 7. Complexity

- **Time:** {pack.get('time_complexity', 'Not specified')}
- **Space:** {pack.get('space_complexity', 'Not specified')}

## 8. Common mistakes

{bullets(pack.get('common_mistakes'))}
## 9. Self-check quiz

{bullets(pack.get('quiz'))}
## 10. Assumptions and caveats

{pack.get('notes', 'Generated content may contain errors. Verify against the linked statement.')}

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
"""
    (folder / "README.md").write_text(lesson, encoding="utf-8")

    hints = pack.get("hints", [])
    hint_text = "# Graduated hints\n\nTry the problem before opening each hint. Stop when you can continue independently.\n\n"
    if isinstance(hints, list):
        for i, hint in enumerate(hints[:3], 1):
            hint_text += f"## Hint {i}\n\n{hint}\n\n"
    (folder / "HINTS.md").write_text(hint_text, encoding="utf-8")

    test_cases = pack.get("test_cases", [])
    dry = "# Dry run and test cases\n\n" + str(pack.get("dry_run", "Not provided.")) + "\n\n## Suggested tests\n\n"
    dry += bullets(test_cases)
    if test_report and test_report.get("ran"):
        dry += "\n## Automated Python test run\n\n" + testrunner.summarize(test_report) + "\n"
        for line in test_report.get("details", []):
            dry += f"- {line}\n"
        dry += "\nOnly the Python solution was executed (isolated, no network keys). Java and C++ were compile-checked only. Generated expected values can themselves be wrong, so verify any failure against the statement.\n"
    else:
        dry += "\n**Important:** These test ideas were not executed. Confirm expected values against the statement.\n"
    (folder / "DRY_RUN.md").write_text(dry, encoding="utf-8")

    (folder / "MY_ATTEMPT.md").write_text(f"""# My attempt — {title}

Problem: {url}

## Before looking at the solution
- [ ] I can restate the problem in my own words.
- [ ] I know the input, output and constraints.
- [ ] I attempted a solution for at least 15–25 minutes.

## My approach
Write your own idea here.

## My code
Paste your first attempt here. Keep it even if it fails; it helps you learn.

## Where I got stuck
Describe the exact point.

## After reviewing the explanation
- [ ] I can explain the optimized approach without reading the notes.
- [ ] I can dry-run it on a new example.
- [ ] I can implement it from memory tomorrow.

## Review result
- [ ] Not attempted
- [ ] Attempted
- [ ] Solved with hints
- [ ] Solved independently
- [ ] Revisit required
""", encoding="utf-8")

    validation: dict[str, list[str]] = {}
    for language in languages:
        code = pack.get("solutions", {}).get(language, "")
        if not isinstance(code, str):
            code = ""
        validation[language] = validate_code(language, code)
        lang_dir = folder / language
        lang_dir.mkdir(exist_ok=True)
        filename = {"python": "solution.py", "java": "Solution.java", "cpp": "solution.cpp"}[language]
        (lang_dir / filename).write_text(code.rstrip() + "\n", encoding="utf-8")

    (folder / "validation.json").write_text(json.dumps({
        "question_id": qid,
        "title": title,
        "difficulty": difficulty,
        "url": url,
        "static_validation": validation,
        "executed": bool(test_report and test_report.get("ran")),
        "python_tests": test_report,
        "leetcode_accepted": False,
    }, indent=2) + "\n", encoding="utf-8")
    return validation


def update_progress(progress: dict[str, Any], problem: dict[str, Any], run_date: dt.date) -> None:
    qid = str(problem.get("questionFrontendId") or problem.get("frontendQuestionId") or problem.get("questionId"))
    slug = problem["titleSlug"]
    if any(p.get("slug") == slug for p in progress["problems"]):
        return
    review_offsets = REVIEW_OFFSETS
    progress["problems"].append({
        "question_id": qid,
        "title": problem["title"],
        "slug": slug,
        "difficulty": problem.get("difficulty", "Unknown"),
        "url": f"https://leetcode.com/problems/{slug}/",
        "topics": [t.get("name", "") for t in problem.get("topicTags") or []],
        "added_date": run_date.isoformat(),
        "status": "new",
        "my_attempt": f"solutions/{qid}-{slug}/MY_ATTEMPT.md",
        "revision_dates": [(run_date + dt.timedelta(days=d)).isoformat() for d in review_offsets],
        "revision_status": {str(d): "pending" for d in review_offsets},
    })


def write_revision_queue(progress: dict[str, Any], today: dt.date) -> list[str]:
    lines = [
        "# Spaced revision queue",
        "",
        "Review the problem before looking at the solution. Mark your result in `MY_ATTEMPT.md`.",
        "Revision intervals: 1, 3, 7, 14 and 30 days after adding a problem.",
        "",
        "## Due today or overdue",
        "",
    ]
    due_count = 0
    due_titles: list[str] = []
    for p in progress["problems"]:
        statuses = p.get("revision_status", {})
        for day, due in enumerate(p.get("revision_dates", [])):
            offset = REVIEW_OFFSETS[day] if day < len(REVIEW_OFFSETS) else day
            if due <= today.isoformat() and statuses.get(str(offset), "pending") == "pending":
                lines.append(f"- [ ] **{p['title']}** ({p['difficulty']}) — [problem]({p['url']}) — due {due} — `{p['my_attempt']}`")
                due_count += 1
                due_titles.append(f"{p['title']} (day {offset})")
    if not due_count:
        lines.append("- No pending revisions due today.")
    lines += ["", "## Upcoming", ""]
    upcoming = []
    for p in progress["problems"]:
        statuses = p.get("revision_status", {})
        for day, due in enumerate(p.get("revision_dates", [])):
            offset = REVIEW_OFFSETS[day] if day < len(REVIEW_OFFSETS) else day
            if due > today.isoformat() and statuses.get(str(offset), "pending") == "pending":
                upcoming.append((due, p, offset))
    
    for due, p, offset in sorted(
        upcoming, key=lambda item: (item[0], item[1]["title"])
    )[:40]: 
        lines.append(f"- {due}: **{p['title']}** — day {offset} — [problem]({p['url']})")
    by_diff: dict[str, int] = {}
    done = total_reviews = 0
    for p in progress["problems"]:
        by_diff[p.get("difficulty", "Unknown")] = by_diff.get(p.get("difficulty", "Unknown"), 0) + 1
        for state in p.get("revision_status", {}).values():
            total_reviews += 1
            done += state == "done"
    mix = ", ".join(f"{d} {n}" for d, n in sorted(by_diff.items())) or "none yet"
    lines += [
        "",
        "## Stats",
        "",
        f"- Problems tracked: {len(progress['problems'])} ({mix})",
        f"- Revisions done: {done} / {total_reviews}",
        f"- Solved (Accepted): {sum(1 for p in progress['problems'] if p.get('status') == 'solved')} / {len(progress['problems'])}",
    ]
    lines += [
        "",
        "## How to mark a revision complete",
        "",
        "Run `python src/mark_revision.py <question_id> <day|all>` (day is one of 1, 3, 7, 14, 30), or edit `revision_status` in `progress/progress.json` by hand, then commit. Reviews are never auto-marked.",
        "",
        "Progress changes persist only after the daily PR is merged into the default branch.",
    ]
    REVISION_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return due_titles


def main() -> int:
    languages = [
        x.strip().lower()
        for x in os.getenv("SOLUTION_LANGUAGES", "python,java,cpp").split(",")
        if x.strip()
    ]
    if not languages or set(languages) - SUPPORTED_LANGUAGES:
        raise RuntimeError(f"Unsupported language list: {languages}")
    count = env_int("DAILY_PROBLEM_COUNT", 1, minimum=1, maximum=5)
    today = dt.datetime.now(dt.timezone.utc).date()
    progress = load_progress()
    pool = fetch_question_pool()
    questions = select_new_questions(pool, progress, count)

    added = []
    for selected in questions:
        problem = fetch_details(selected["titleSlug"])
        print(f"Generating learning pack for #{problem.get('questionFrontendId')}: {problem['title']}")
        pack = gemini_json(build_prompt(problem, languages))
        if not isinstance(pack.get("solutions"), dict):
            raise RuntimeError(f"Gemini response for {problem['title']} has no solutions object.")
        missing = [lang for lang in languages if not isinstance(pack["solutions"].get(lang), str) or not pack["solutions"][lang].strip()]
        if missing:
            raise RuntimeError(f"Missing generated code for {problem['title']}: {missing}")
        repair_solutions(problem, pack, languages)
        test_report = None
        if "python" in languages and os.getenv("RUN_PYTHON_TESTS", "1") != "0":
            test_report = testrunner.run_python_tests(pack["solutions"]["python"], pack.get("test_cases"))
            print(f"Python tests for {problem['title']}: {testrunner.summarize(test_report)}")
        issues = render_lesson(problem, pack, languages, today, test_report)
        update_progress(progress, problem, today)
        # Save after every problem so a later failure does not lose earlier work.
        PROGRESS_FILE.write_text(json.dumps(progress, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        added.append({
            "title": problem["title"],
            "difficulty": problem.get("difficulty", "Unknown"),
            "url": f"https://leetcode.com/problems/{problem['titleSlug']}/",
            "issues": {lang: found for lang, found in issues.items() if found},
            "tests": testrunner.summarize(test_report) if test_report is not None else None,
        })

    due_today = write_revision_queue(progress, today)
    n = len(added)
    body = [
        "## Daily LeetCode learning pack",
        "",
        f"{n} new problem{'s' if n != 1 else ''} with full Hinglish explanations, brute-force vs optimized approaches, dry runs, hints, quiz questions, tests, and {'/'.join(languages)} source.",
        "",
    ]
    for item in added:
        body.append(f"- [{item['title']}]({item['url']}) - {item['difficulty']}")
        for lang, found in item["issues"].items():
            body.append(f"  - WARNING `{lang}` static check: {'; '.join(found)}")
        if item.get("tests"):
            body.append(f"  - Python tests: {item['tests']}")
    if due_today:
        body += ["", f"## Revisions due today ({len(due_today)})"] + [f"- {t}" for t in due_today]
    body += [
        "",
        "## Before merging",
        "- [ ] Read the explanation and solve without looking at the code.",
        "- [ ] Add your own attempt to each `MY_ATTEMPT.md`.",
        "- [ ] Verify test cases and expected outputs.",
        "- [ ] Run the code or submit it to LeetCode yourself.",
        "- [ ] Check `progress/REVISION_QUEUE.md`.",
        "",
        "**Important:** passing tests are not proof of correctness. Only the Python solution was run against generated tests; no LeetCode acceptance was claimed.",
    ]
    body_file = Path(os.getenv("PR_BODY_FILE") or ROOT / "pr_body.md")
    body_file.write_text("\n".join(body) + "\n", encoding="utf-8")
    print(f"Created {n} learning packs and refreshed the revision queue.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
