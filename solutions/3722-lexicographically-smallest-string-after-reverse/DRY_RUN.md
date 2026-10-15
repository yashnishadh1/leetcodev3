# Dry run and test cases

String s = 'dcab', n = 4. Initially best = 'dcab'.
- k = 1: Prefix rev -> 'dcab', Suffix rev -> 'dcab' (best = 'dcab')
- k = 2: Prefix rev (dc -> cd) -> 'cdab' (chhota hai, best = 'cdab'); Suffix rev (ab -> ba) -> 'dcba'
- k = 3: Prefix rev (dca -> acd) -> 'acdb' (aur chhota hai, best = 'acdb'); Suffix rev (cab -> bac) -> 'dbac'
- k = 4: Prefix/Suffix rev (dcab -> bacd) -> 'bacd'
Final best = 'acdb'.

## Suggested tests

- Input: `s = "dcab"` -> Expected: `"acdb"` (Prefix of length 3 ('dca') reverse karne par 'acd' + 'b' = 'acdb' banta hai, jo smallest hai.)
- Input: `s = "abba"` -> Expected: `"aabb"` (Suffix of length 3 ('bba') reverse karne par 'a' + 'abb' = 'aabb' milta hai.)
- Input: `s = "a"` -> Expected: `"a"` (Single character string me k=1 hi choose ho sakta hai, result 'a' hi rahega.)

## Automated Python test run

3/3 passed

Only the Python solution was executed (isolated, no network keys). Java and C++ were compile-checked only. Generated expected values can themselves be wrong, so verify any failure against the statement.
