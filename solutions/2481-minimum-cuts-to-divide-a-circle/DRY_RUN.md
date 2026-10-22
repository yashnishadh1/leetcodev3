# Dry run and test cases

| n | Condition | Calculation | Result |
|---|---|---|---|
| 1 | n == 1 | Special base case | 0 |
| 2 | n % 2 == 0 | 2 / 2 | 1 |
| 3 | n % 2 != 0 | n | 3 |
| 4 | n % 2 == 0 | 4 / 2 | 2 |
| 5 | n % 2 != 0 | n | 5 |

## Suggested tests

- Input: `1` -> Expected: `0` (Circle is already 1 piece.)
- Input: `4` -> Expected: `2` (4 is even, 4 / 2 = 2 diameter cuts.)
- Input: `3` -> Expected: `3` (3 is odd, requires 3 radius cuts.)

## Automated Python test run

3/3 passed

Only the Python solution was executed (isolated, no network keys). Java and C++ were compile-checked only. Generated expected values can themselves be wrong, so verify any failure against the statement.
