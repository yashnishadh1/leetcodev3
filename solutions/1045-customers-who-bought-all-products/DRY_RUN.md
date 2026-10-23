# Dry run and test cases

Product table count = 2

Customer Table Grouped by customer_id:
| customer_id | distinct product_keys | COUNT(DISTINCT product_key) | Condition: count == 2 | Selected? |
|---|---|---|---|---|
| 1 | {5, 6} | 2 | 2 == 2 (True) | Yes |
| 2 | {6} | 1 | 1 == 2 (False) | No |
| 3 | {5, 6} | 2 | 2 == 2 (True) | Yes |

Final Result: customer_id 1, 3.

## Suggested tests

- Input: `Customer: [[1, 1], [1, 2], [2, 1]], Product: [[1], [2]]` -> Expected: `customer_id: [1]` (Customer 1 ne product 1 aur 2 dono khareede hain, customer 2 ne sirf 1 khareeda.)
- Input: `Customer: [[1, 1], [1, 1]], Product: [[1]]` -> Expected: `customer_id: [1]` (Total product 1 hi hai, aur customer 1 ne wahi khareeda hai bhale hi 2 baar.)

**Important:** These test ideas were not executed. Confirm expected values against the statement.
