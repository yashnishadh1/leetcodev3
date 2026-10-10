# Dry run and test cases

connections = [[0,1],[1,3],[2,3],[4,0],[4,5]]
Adj list representation:
0: [(1, 1), (4, 0)]
1: [(0, 0), (3, 1)]
2: [(3, 0)]
3: [(1, 0), (2, 1)]
4: [(0, 1), (5, 1)]
5: [(4, 0)]

Start DFS/BFS from 0 (visited = {0}, flips = 0):
- From 0 to 1: weight = 1 (flips = 1), visit 1
  - From 1 to 3: weight = 1 (flips = 2), visit 3
    - From 3 to 2: weight = 0 (flips = 2), visit 2
- From 0 to 4: weight = 0 (flips = 2), visit 4
  - From 4 to 5: weight = 1 (flips = 3), visit 5
Total flips = 3.

## Suggested tests

- Input: `n = 6, connections = [[0,1],[1,3],[2,3],[4,0],[4,5]]` -> Expected: `3` (Edges [0,1], [1,3], [4,5] capital 0 se door ja rahi hain, in teeno ko reverse karna hoga.)
- Input: `n = 5, connections = [[1,0],[1,2],[3,2],[3,4]]` -> Expected: `2` (Edges [1,2] aur [3,4] ko flip karna padega taaki 2 aur 4 capital 0 tak pahunch sakein.)
- Input: `n = 3, connections = [[1,0],[2,0]]` -> Expected: `0` (Dono edges already 0 ki taraf point kar rahi hain, koi change require nahi hai.)

## Automated Python test run

3/3 passed

Only the Python solution was executed (isolated, no network keys). Java and C++ were compile-checked only. Generated expected values can themselves be wrong, so verify any failure against the statement.
