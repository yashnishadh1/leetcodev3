# Dry run and test cases

Initial State: semH = 2, semO = 0.
1. H1 aata hai: semH.acquire() -> semH = 1. releaseHydrogen() call hota hai.
2. H2 aata hai: semH.acquire() -> semH = 0. releaseHydrogen() call hota hai. H2 detects it is 2nd H, releases semO -> semO = 1.
3. O1 aata hai: semO.acquire() -> semO = 0. releaseOxygen() call hota hai. O1 releases 2 permits to semH -> semH = 2.
Next molecule ke liye cycle cleanly repeat ho sakti hai.

## Suggested tests

- Input: `water = "HOH"` -> Expected: `"HHO"` (Single molecule ke 2 H aur 1 O bond honge.)
- Input: `water = "OOHHHH"` -> Expected: `"HHOHHO"` (Do molecules hain, har chunk of 3 me 2 H aur 1 O aayenge.)

## Automated Python test run

0/2 passed, 2 errors
- error: input water = "HOH" -> got IndexError: list index out of range, expected 'HHO'
- error: input water = "OOHHHH" -> got IndexError: list index out of range, expected 'HHOHHO'

Only the Python solution was executed (isolated, no network keys). Java and C++ were compile-checked only. Generated expected values can themselves be wrong, so verify any failure against the statement.
