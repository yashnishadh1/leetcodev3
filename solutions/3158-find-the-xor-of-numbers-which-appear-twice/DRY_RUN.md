# Dry run and test cases

Input: nums = [1, 2, 2, 1]
Initial: seen = {}, ans = 0

1. num = 1:
   - Kya 1 'seen' me hai? Nahi.
   - seen = {1}, ans = 0
2. num = 2:
   - Kya 2 'seen' me hai? Nahi.
   - seen = {1, 2}, ans = 0
3. num = 2:
   - Kya 2 'seen' me hai? Haan!
   - ans = ans ^ 2 = 0 ^ 2 = 2
4. num = 1:
   - Kya 1 'seen' me hai? Haan!
   - ans = ans ^ 1 = 2 ^ 1 = 3

Final Output: 3

## Suggested tests

- Input: `nums = [1, 2, 1, 3]` -> Expected: `1` (1 do baar aaya hai, baaki 1 baar. 1 ka XOR = 1.)
- Input: `nums = [1, 2, 3]` -> Expected: `0` (Koi bhi number do baar nahi aaya, so answer 0 hai.)
- Input: `nums = [1, 2, 2, 1]` -> Expected: `3` (1 aur 2 dono do baar aaye. 1 ^ 2 = 3.)
- Input: `nums = [4, 4]` -> Expected: `4` (Sirf ek hi number 4 do baar aaya hai, so answer 4.)

## Automated Python test run

4/4 passed

Only the Python solution was executed (isolated, no network keys). Java and C++ were compile-checked only. Generated expected values can themselves be wrong, so verify any failure against the statement.
