# LeetCode Learning System — Gemini + GitHub PRs

A daily learning journal that prepares **LeetCode problems on a daily schedule** (default 1 per run, max 5 via `DAILY_PROBLEM_COUNT`), asks Gemini for full Hinglish explanations, saves solutions in Python/Java/C++, includes graduated hints and a dry run, and opens a pull request for review.

It is designed for learning, not for claiming that generated code is accepted by LeetCode.

## Daily workflow
1. Fetch a pool of free LeetCode problems from the whole catalogue and pick by difficulty weights (default Easy 4 : Medium 5 : Hard 1, set with `DIFFICULTY_WEIGHTS`).
2. Avoid problems already recorded in `progress/progress.json` or already present in `solutions/`.
3. For each problem, generate:
   - simple Hinglish problem explanation
   - input/output breakdown and example walkthrough
   - brute-force approach and optimized approach
   - dry run table
   - time and space complexity
   - three graduated hints
   - common mistakes and a short self-check quiz
   - Python, Java, and C++ submissions, compile-checked (g++ / javac) and auto-repaired by Gemini when they fail
   - sample/edge-case test ideas
4. Create an `MY_ATTEMPT.md` template so you can record your own attempt.
5. Add the new problems to progress tracking and schedule spaced revision at days 1, 3, 7, 14 and 30.
6. Open a PR. Nothing merges automatically.

## Setup
1. Create a GitHub repository, e.g. `leetcode-learning-system`.
2. Extract this ZIP and upload the contents to the repository root.
3. Add a repository secret named `GEMINI_API_KEY` containing an API key from Google AI Studio.
4. In **Settings → Actions → General → Workflow permissions**, allow workflows to create pull requests if required by your organization/repository policy.
5. In **Actions**, run `Daily LeetCode Learning PR` manually once.
6. Review the PR and merge only after checking the generated content. Progress and revision dates persist on the default branch only after you merge.

## Schedule
Daily at 02:00 India Standard Time (`30 20 * * *` UTC). GitHub scheduled runs can be delayed. You can also run manually.

## Files written per problem
```text
solutions/<id>-<slug>/
  README.md            # Full Hinglish lesson
  HINTS.md             # Graduated hints
  DRY_RUN.md           # Dry run + test cases
  MY_ATTEMPT.md        # Blank attempt template for you
  validation.json      # Static validation report
  python/solution.py
  java/Solution.java
  cpp/solution.cpp
progress/progress.json
progress/REVISION_QUEUE.md
```

## Spaced revision
When a new problem is added, revision dates are scheduled for 1, 3, 7, 14 and 30 days after the run date. Each daily run updates `progress/REVISION_QUEUE.md` with due and upcoming reviews. It does not automatically re-solve old problems yet; the queue tells you which problems to revisit and lets you mark them complete in a future PR. For accurate persistence, merge the PR into the default branch.

## Testing and safety caveats
- The project checks Python syntax and compiles Java (`javac`) and C++ (`g++ -fsyntax-only`). If a check fails, Gemini gets up to `MAX_REPAIR_ROUNDS` (default 2) attempts to fix it; remaining problems are listed as warnings in the PR body. Python solutions are also **run against the generated test cases** in an isolated subprocess (empty environment, no API keys, memory limit, timeout); Java and C++ are compile-checked only. Nothing is submitted to LeetCode.
- `DRY_RUN.md` contains hand-check prompts and example/edge test cases to run yourself.
- LeetCode's unauthenticated GraphQL interface may be rate-limited or change.
- Generated explanations or solutions can be wrong. Review the problem statement and verify the code.
- Never store API keys in the repository. Use GitHub Actions secrets (`GEMINI_API_KEY`).
- The workflow uses limited permissions and never merges PRs automatically.
- For production use, pin third-party GitHub Actions to reviewed full commit SHAs.

## Local run (optional)
Set `GEMINI_API_KEY` in your shell, then:
```bash
pip install -r requirements.txt
python src/automation.py
```

## Automated Python tests
`src/testrunner.py` parses each generated test (`nums = [2,7], target = 9` -> arguments, `[0,1]` -> expected), runs the solution and reports pass / fail / error / skipped. It understands in-place problems and flags answers that match only in a different order. Linked-list and tree inputs are skipped. The result appears in `DRY_RUN.md`, `validation.json`, the PR body and the Actions job summary. A failing test can mean wrong code **or** a wrong generated expectation, so check the statement.

## Topic balance and daily reminders
Within the chosen difficulty, the picker prefers topics you have practised least (topics are stored in `progress.json`). The PR body also lists revisions that are due that day.

## Browser helper (one click, not unattended)
`leetcode-fill.user.js` (Tampermonkey) fills the editor from this repo. With "Click Submit after fill" switched on in the Tampermonkey menu it clicks Submit once per button press (max 5 per day), reads the verdict and stores it locally. Export the log from the menu, save it as `submission_log.json` and run:
```bash
python src/import_log.py submission_log.json
```
This marks problems `solved` / `attempted` in `progress.json` and shows the solved count in the queue stats. It runs only in your own logged-in browser; there is deliberately no headless or scheduled submission.

## Marking revisions done
```bash
python src/mark_revision.py <question_id> <day|all>   # day: 1, 3, 7, 14 or 30
```
This updates `progress/progress.json` and regenerates `progress/REVISION_QUEUE.md`, which also shows simple stats (problems tracked, revisions done).

## Configuration (environment variables)
| Variable | Default | Meaning |
| --- | --- | --- |
| `GEMINI_API_KEY` | required | Repository secret |
| `GEMINI_MODEL` | `gemini-3.8-flash` | Check the exact name in Google AI Studio |
| `SOLUTION_LANGUAGES` | `python,java,cpp` | Languages to generate |
| `DAILY_PROBLEM_COUNT` | `1` | 1 to 5 problems per run |
| `LEETCODE_DIFFICULTIES` | `Easy,Medium,Hard` | Allowed difficulties |
| `DIFFICULTY_WEIGHTS` | `Easy:4,Medium:5,Hard:1` | Relative pick probability |
| `MAX_REPAIR_ROUNDS` | `2` | Gemini repair attempts for failing code (0 disables) |
| `COMPILE_CHECK` | `1` | Set `0` to skip compiler checks |
| `RUN_PYTHON_TESTS` | `1` | Set `0` to skip the automated Python test run |

## Development
```bash
pip install -r requirements.txt pytest
python -m pytest -q
```
CI runs the same tests on every push or PR that touches `src/`, `tests/` or the workflows.
