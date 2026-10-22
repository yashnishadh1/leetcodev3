# Dry run and test cases

Starting with empty map, count = 0.
- `add(2, 3)`: No overlapping intervals. Insert [2, 3]. count = 0 + 2 = 2.
- `add(7, 10)`: No overlap with [2, 3]. Insert [7, 10]. count = 2 + 4 = 6. Map: {2: 3, 7: 10}.
- `add(5, 8)`:
  - Binary search finds overlapping interval [7, 10] because 7 <= 8 and 10 >= 5.
  - Overlap detected: subtract (10 - 7 + 1) = 4 from count -> count = 2.
  - Merge: left = min(5, 7) = 5, right = max(8, 10) = 10. Erase [7, 10].
  - Next check: no more overlaps.
  - Insert [5, 10], add (10 - 5 + 1) = 6 to count -> count = 2 + 6 = 8.
  - Map: {2: 3, 5: 10}.
- `count()`: returns 8 immediately in O(1).

## Suggested tests

- Input: `["CountIntervals","add","add","count","add","count"]
[[],[2,3],[7,10],[],[5,8],[]]` -> Expected: `[null,null,null,6,null,8]` (Standard example provided in problem description.)
- Input: `["CountIntervals","add","add","add","count"]
[[],[1,5],[3,7],[2,6],[]]` -> Expected: `[null,null,null,null,7]` (Multiple completely overlapping intervals all merging into one interval [1, 7].)

**Important:** These test ideas were not executed. Confirm expected values against the statement.
