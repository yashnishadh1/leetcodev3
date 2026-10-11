# Dry run and test cases

Input: operations = ["--X", "X++", "X++"]
Initial state: x = 0

Step 1: op = "--X", op[1] is '-' -> x = x - 1 = -1
Step 2: op = "X++", op[1] is '+' -> x = x + 1 = 0
Step 3: op = "X++", op[1] is '+' -> x = x + 1 = 1

Final x = 1.

## Suggested tests

- Input: `["--X","X++","X++"]` -> Expected: `1` (One decrement (-1) followed by two increments (+2), net change is +1.)
- Input: `["++X","++X","X++"]` -> Expected: `3` (Three increments, net change is +3.)
- Input: `["X++","++X","--X","X--"]` -> Expected: `0` (Two increments and two decrements cancel each other out, net change is 0.)

## Automated Python test run

3/3 passed

Only the Python solution was executed (isolated, no network keys). Java and C++ were compile-checked only. Generated expected values can themselves be wrong, so verify any failure against the statement.
