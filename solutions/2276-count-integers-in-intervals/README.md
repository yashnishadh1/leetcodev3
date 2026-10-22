# 2276. Count Integers in Intervals

- **Difficulty:** Hard
- **Problem:** https://leetcode.com/problems/count-integers-in-intervals/
- **Topics:** Design, Segment Tree, Ordered Set
- **Generated:** 2026-10-21

## 1. Problem ko simple Hinglish mein samjho

Hame ek class `CountIntervals` design karni hai jo intervals add kare aur overall unique integers ka count track kare. Intervals overlap ho sakte hain. Jab bhi `add(left, right)` call ho, hume interval ko store karna hai aur `count()` call hone par total kitne unique integers at least ek interval me cover hue hain, wo return karna hai.

## 2. Input aur output

Input me methods call honge: `CountIntervals()`, `add(left, right)`, aur `count()`. Output me `count()` integer return karega aur baki `null`. Constraints: `1 <= left <= right <= 10^9`, total method calls up to `10^5`. Range bohot badi hai (10^9 tak), isliye simple boolean array ya direct array mapping possible nahi hai.

## 3. Example walkthrough

Example 1 ke steps:
1. Init: empty set, total count = 0.
2. `add(2, 3)`: interval [2, 3] add hua. Length = 3 - 2 + 1 = 2. Total count = 2. Intervals: {[2, 3]}.
3. `add(7, 10)`: [7, 10] disjoint hai [2, 3] se. Length = 10 - 7 + 1 = 4. Total count = 2 + 4 = 6. Intervals: {[2, 3], [7, 10]}.
4. `count()`: Return 6.
5. `add(5, 8)`: Ye [7, 10] ke sath overlap karta hai (since 8 >= 7). Dono merge ho kar ban jate hain [min(5, 7), max(8, 10)] = [5, 10]. Purana [7, 10] remove hua (-4), naya [5, 10] add hua (+6). Net change +2. Total count = 6 + 2 = 8. Intervals: {[2, 3], [5, 10]}.
6. `count()`: Return 8.

## 4. Brute-force approach

Brute force approach me hum ek hash set use karein jo har ek integer ko store kare jo interval me aata hai. But yahan intervals [1, 10^9] tak ho sakte hain, to ek single interval [1, 10^9] hi Memory Limit Exceed (MLE) aur Time Limit Exceed (TLE) kar dega. Dusra approach hai non-overlapping intervals ki list rakhna aur har `add` operation par linear scan se check karke merge karna, jo O(N) time lega per add, resulting in overall O(N^2) worst case.

## 5. Optimized approach

Optimized approach do tareeqon se solve ho sakta hai:
1. **Dynamic / Segment Tree with Lazy Propagation**: Range [1, 10^9] hai to dynamically nodes create karte hain. Agar koi node completely covered ho gaya, to children explore karne ki zaroorat nahi.
2. **Ordered Map / Balanced BST (Merge Intervals)**: C++ me `std::map`, Java me `TreeMap`, Python me `SortedDict` ya binary search with intervals list. Hum disjoint non-overlapping intervals `[L, R]` store karte hain. Jab naya interval `[left, right]` aata hai, binary search se overlapping intervals find karte hain: koi interval `[l, r]` tab overlap karta hai jab `l <= right` aur `r >= left`. Hum saare overlapping intervals ko ek ek karke delete karte hain aur unka contribution `(r - l + 1)` total count se subtract karte hain, aur interval ko expand karte hain: `left = min(left, l)`, `right = max(right, r)`. Finally expanded interval `[left, right]` insert karte hain aur `(right - left + 1)` add karte hain. Amortized time per `add` is O(log N) kyunki har interval maximum ek baar create aur ek baar delete hota hai.

## 6. Dry run

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

## 7. Complexity

- **Time:** add(left, right): Amortized O(log N) time. Har interval BST/Map me ek baar insert hota hai aur maximum ek baar remove hota hai. Total intervals removed across all calls <= total intervals inserted.
count(): O(1) time kyunki hum count variable maintain karte hain.
- **Space:** O(N) space, jahan N total number of intervals inserted hai (worst-case at most 10^5 intervals in the map).

## 8. Common mistakes

- Overlap condition galat lagana: intervals [l, r] aur [left, right] overlap karte hain if and only if max(l, left) <= min(r, right), yaani l <= right and r >= left.
- Har `count()` par saare intervals ko iterate karke sum karna, jisse count() O(N) ho jata hai. Iske bajaye ek running `cnt` maintain karna better hai.
- Range 10^9 hone par normal segment tree array bana dena jo out-of-memory crash kar dega.

## 9. Self-check quiz

- **Q:** Do intervals [2, 5] aur [6, 8] overlap karte hain integers ke context me?
  **A:** Nahi, integers ke context me 5 aur 6 ke beech koi integer overlap nahi hai, but if continuous integers are considered they are adjacent. Ye problem discrete intervals overlap maangti hai (left <= r and right >= l).
- **Q:** Ek single `add` call me maximum kitne intervals erase ho sakte hain?
  **A:** Worst-case me ek single call me O(N) intervals erase ho sakte hain, but amortized cost across all calls O(log N) hi rehti hai kyunki koi bhi interval ek se zyada baar delete nahi ho sakta.

## 10. Assumptions and caveats

Sorted containers / Tree structures provide an elegant way to maintain disjoint intervals with amortized logarithmic operations. Python implementation uses `bisect` over a sorted list of pairs, or dynamically splitting/merging.

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
