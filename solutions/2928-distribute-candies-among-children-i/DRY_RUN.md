# Dry run and test cases

Consider n = 5, limit = 2:
Initial ans = 0
- i = 0:
  - j = 0: k = 5 - 0 = 5 (> limit, invalid)
  - j = 1: k = 5 - 1 = 4 (invalid)
  - j = 2: k = 5 - 2 = 3 (invalid)
- i = 1:
  - j = 0: k = 4 (invalid)
  - j = 1: k = 3 (invalid)
  - j = 2: k = 5 - 1 - 2 = 2 (valid! ans = 1) -> (1, 2, 2)
- i = 2:
  - j = 0: k = 3 (invalid)
  - j = 1: k = 2 (valid! ans = 2) -> (2, 1, 2)
  - j = 2: k = 1 (valid! ans = 3) -> (2, 2, 1)
Result ans = 3.

## Suggested tests

- Input: `n = 5, limit = 2` -> Expected: `3` (Possible combinations: (1,2,2), (2,1,2), (2,2,1).)
- Input: `n = 3, limit = 3` -> Expected: `10` (Total 10 non-negative combinations jinka sum 3 hai aur koi bhi value > 3 nahi hai.)
- Input: `n = 1, limit = 2` -> Expected: `3` (Candies sirf 1 hai, toh wo child 1, 2 ya 3 kisi ek ko mil sakti hai: (1,0,0), (0,1,0), (0,0,1).)

## Automated Python test run

3/3 passed

Only the Python solution was executed (isolated, no network keys). Java and C++ were compile-checked only. Generated expected values can themselves be wrong, so verify any failure against the statement.
