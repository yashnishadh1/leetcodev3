# Dry run and test cases

Step-by-step dry run on Example 2: actions = ["Calculator", "multiply", "power", "getResult"], values = [2, 5, 2]
1. init(2) -> this.result = 2
2. multiply(5) -> this.result = 2 * 5 = 10, return this
3. power(2) -> this.result = 10^2 = 100, return this
4. getResult() -> return this.result = 100

## Suggested tests

- Input: `actions = ["Calculator", "add", "subtract", "getResult"], values = [10, 5, 7]` -> Expected: `8` (10 + 5 - 7 = 8)
- Input: `actions = ["Calculator", "multiply", "power", "getResult"], values = [2, 5, 2]` -> Expected: `100` ((2 * 5) ^ 2 = 100)
- Input: `actions = ["Calculator", "divide", "getResult"], values = [20, 0]` -> Expected: `"Division by zero is not allowed"` (Divide by zero must throw an error)

## Automated Python test run

0/3 passed, 3 errors
- error: input actions = ["Calculator", "add", "subtract", "getResult"], values = [10, 5, 7] -> got IndexError: list index out of range, expected 8
- error: input actions = ["Calculator", "multiply", "power", "getResult"], values = [2, 5, 2] -> got IndexError: list index out of range, expected 100
- error: input actions = ["Calculator", "divide", "getResult"], values = [20, 0] -> got IndexError: list index out of range, expected 'Division by zero is not allowed'

Only the Python solution was executed (isolated, no network keys). Java and C++ were compile-checked only. Generated expected values can themselves be wrong, so verify any failure against the statement.
