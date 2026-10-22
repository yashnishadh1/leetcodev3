# Dry run and test cases

Input: celsius = 36.50
Step 1: kelvin = 36.50 + 273.15 = 309.65
Step 2: fahrenheit = 36.50 * 1.80 + 32.00 = 65.7 + 32.00 = 97.7
Step 3: ans = [309.65, 97.7]
Result: [309.65, 97.70]

## Suggested tests

- Input: `celsius = 36.50` -> Expected: `[309.65000, 97.70000]` (Official Example 1 testcase.)
- Input: `celsius = 122.11` -> Expected: `[395.26000, 251.79800]` (Official Example 2 testcase.)
- Input: `celsius = 0.0` -> Expected: `[273.15000, 32.00000]` (Lower bound of constraint (celsius = 0).)

## Automated Python test run

3/3 passed

Only the Python solution was executed (isolated, no network keys). Java and C++ were compile-checked only. Generated expected values can themselves be wrong, so verify any failure against the statement.
