# Dry run and test cases

Input: digits = [2, 1, 3, 0]
Frequency array: count[0]=1, count[1]=1, count[2]=1, count[3]=1, baaki sab 0.
Loop starts: num = 100, 102, ..., 998 (step 2)
- num = 100: digits are 1, 0, 0. Needs two 0s, but count[0]=1 -> Not possible.
- num = 102: digits are 1, 0, 2. count[1]>=1, count[0]>=1, count[2]>=1 -> Valid! Result: [102]
- num = 104: requires 4, count[4]=0 -> Skip.
...
- num = 120: digits 1, 2, 0. Valid! Result: [102, 120]
Har valid even candidate direct order me milta jaata hai bina sorting ya set overhead ke.

## Suggested tests

- Input: `digits = [2,1,3,0]` -> Expected: `[102,120,130,132,210,230,302,310,312,320]` (Standard example jahan 0 present hai aur strictly 3-digit even numbers form karne hain bina leading zero ke.)
- Input: `digits = [2,2,8,8,2]` -> Expected: `[222,228,282,288,822,828,882]` (Duplicates present hain input me, output me unique numbers aane chahiye.)
- Input: `digits = [3,7,5]` -> Expected: `[]` (Array me koi bhi even digit nahi hai, isliye koi valid number nahi ban sakta.)

## Automated Python test run

3/3 passed

Only the Python solution was executed (isolated, no network keys). Java and C++ were compile-checked only. Generated expected values can themselves be wrong, so verify any failure against the statement.
