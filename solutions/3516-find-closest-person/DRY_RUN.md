# Dry run and test cases

Input: x = 2, y = 7, z = 4
Step 1: dist1 = abs(2 - 4) = 2
Step 2: dist2 = abs(7 - 4) = 3
Step 3: Check dist1 < dist2 (2 < 3) -> True
Result: 1

## Suggested tests

- Input: `x = 2, y = 7, z = 4` -> Expected: `1` (dist1 is 2, dist2 is 3; 2 < 3 so person 1 reaches first.)
- Input: `x = 2, y = 5, z = 6` -> Expected: `2` (dist1 is 4, dist2 is 1; 1 < 4 so person 2 reaches first.)
- Input: `x = 1, y = 5, z = 3` -> Expected: `0` (dist1 is 2, dist2 is 2; equal distances lead to a tie (0).)

## Automated Python test run

3/3 passed

Only the Python solution was executed (isolated, no network keys). Java and C++ were compile-checked only. Generated expected values can themselves be wrong, so verify any failure against the statement.
