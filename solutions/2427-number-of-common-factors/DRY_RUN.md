# Dry run and test cases

Dry run for a = 12, b = 6 using GCD approach:
1. g = gcd(12, 6) = 6
2. Count factors of 6 by iterating i from 1 to sqrt(6) ≈ 2:
   - i = 1: 6 % 1 == 0 -> true. Pair is (1, 6). Dono distinct hain, count += 2 (count = 2).
   - i = 2: 6 % 2 == 0 -> true. Pair is (2, 3). Dono distinct hain, count += 2 (count = 4).
3. Loop ends. Total count = 4.

## Suggested tests

- Input: `a = 12, b = 6` -> Expected: `4` (Common factors 1, 2, 3, 6 hain.)
- Input: `a = 25, b = 30` -> Expected: `2` (Common factors 1 aur 5 hain.)
- Input: `a = 1, b = 1` -> Expected: `1` (Minimum possible input constraints, only 1 divides both.)
- Input: `a = 7, b = 11` -> Expected: `1` (Dono prime numbers hain, common factor sirf 1 hai.)

## Automated Python test run

4/4 passed

Only the Python solution was executed (isolated, no network keys). Java and C++ were compile-checked only. Generated expected values can themselves be wrong, so verify any failure against the statement.
