# 1466. Reorder Routes to Make All Paths Lead to the City Zero

- **Difficulty:** Medium
- **Problem:** https://leetcode.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/
- **Topics:** Depth-First Search, Breadth-First Search, Graph Theory
- **Generated:** 2026-10-10

## 1. Problem ko simple Hinglish mein samjho

Humare paas `n` cities hain (0 se n-1) aur `n-1` directed roads hain, jo milkar ek tree banate hain. Hum chahte hain ki har city se road ke zariye city 0 (capital) tak travel kiya ja sake. Iske liye humein minimum kitni roads ki direction reverse karni padegi, ye count nikalna hai.

## 2. Input aur output

Input: An integer `n` aur ek 2D array `connections` jisme har pair `[a, b]` ek directed road represent karta hai from city `a` to city `b`.
Output: Ek integer jo batata hai minimum edges jinki direction flip karni padegi.
Constraints: `2 <= n <= 5 * 10^4`, `connections.length == n - 1`, graph cycle-free hai (tree structure).

## 3. Example walkthrough

Example 1: n = 6, connections = [[0,1],[1,3],[2,3],[4,0],[4,5]]
Hum city 0 se shuru karke bahar ki taraf traverse karte hain:
1. 0 -> 1: original direction 0 se bahar ja rahi hai (0->1). Lekin hume 1 se 0 aana hai, toh is edge ko reverse karna padega. Flip count = 1.
2. 1 -> 3: original direction 1->3 hai (away from 0). Isko reverse karna padega. Flip count = 2.
3. 3 -> 2: original edge 2->3 thi. Hum 3 se 2 ja rahe hain, aur edge already 2->3 (towards 3, jo ultimately 0 ki taraf ja raha hai) hai. No flip needed.
4. 0 -> 4: original edge 4->0 thi (towards 0). No flip needed.
5. 4 -> 5: original edge 4->5 thi (away from 0). Isko flip karna padega. Flip count = 3.
Total flips = 3.

## 4. Brute-force approach

Har node ke liye individually check karna ki kya wo 0 tak reach kar sakta hai (using DFS/BFS). Agar nahi, toh incoming path ko reverse karo. Ye approach repetitive hogi aur tree structure ka fayda nahi uthata. Time complexity O(n^2) ho sakti hai jo n = 5 * 10^4 par TLE de degi.

## 5. Optimized approach

Intuition: Har node ko 0 ki taraf point karna chahiye. Iska matlab agar hum city 0 se start karein aur outward traverse karein, toh har edge humare travel direction ke *opposite* honi chahiye (child -> parent honi chahiye). Agar koi edge parent -> child point kar rahi hai, iska matlab wo 0 se door ja rahi hai, toh usko flip karna padega (cost 1). Graph ko undirected graph ki tarah represent karo, but har edge ke sath ek flag rakho: (neighbor, 1) agar original edge parent->neighbor hai (needs flip), aur (neighbor, 0) agar original edge neighbor->parent hai (already correct). Phir node 0 se BFS ya DFS chalao aur simple visited set ya parent pointer se traverse karke weights sum kar lo.

## 6. Dry run

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

## 7. Complexity

- **Time:** O(n): Graph me `n` nodes aur `n-1` edges hain. DFS/BFS har node aur har edge ko exactly ek baar process karta hai.
- **Space:** O(n): Adjacency list store karne ke liye O(n) space lagta hai aur recursion stack / BFS queue ke liye O(n) space lagta hai.

## 8. Common mistakes

- Directed graph treat karke sirf outward traversal try karna, jisse disconnected nodes visit nahi ho payenge kyunki edges reverse direction me ho sakti hain.
- Visited array ya parent check bhool jana, jisse infinite loops ho jayein kyunki graph bidirectional banaya hai.
- Flag logic ulta kar dena: yaad rakho edge away from 0 ko flip karna hai, towards 0 ko nahi.

## 9. Self-check quiz

- **Q:** Hum graph ko bidirectional kyu treat karte hain jabki original edges directed hain?
  **A:** Kyunki agar hum city 0 se traverse karein, toh hum sirf un nodes tak pahunch payenge jinpe 0 se outgoing paths hain. Lekin tree ke sare nodes tak pahunchne ke liye edges ko dono directions me traverse karna padega.
- **Q:** Agar connection [u, v] hai, toh 0 se outward traversal me hum u -> v edge ko count karenge ya v -> u?
  **A:** Agar hum u se v ja rahe hain aur original edge u -> v thi, toh ye 0 se door ja rahi hai, isliye ise flip karna padega (count += 1).

## 10. Assumptions and caveats

Tree undirected form me connected aur acyclic hoti hai, jisse DFS/BFS me har edge exactly ek baar child ki direction me consider hogi.

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
