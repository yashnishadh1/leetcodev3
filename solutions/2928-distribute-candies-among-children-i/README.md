# 2928. Distribute Candies Among Children I

- **Difficulty:** Easy
- **Problem:** https://leetcode.com/problems/distribute-candies-among-children-i/
- **Topics:** Math, Combinatorics, Enumeration
- **Generated:** 2026-10-14

## 1. Problem ko simple Hinglish mein samjho

Humein total `n` candies ko 3 bacho mein divide karna hai. Har child ko 0 se lekar `limit` tak candies mil sakti hain (koi bhi child `limit` se zyada candies nahi le sakta). Humein total aise combinations (ways) count karne hain jinka sum exactly `n` ho.

## 2. Input aur output

Input:
- `n` (integer): Total candies ki sankhya (1 <= n <= 50).
- `limit` (integer): Ek child ko maximum kitni candies mil sakti hain (1 <= limit <= 50).

Output:
- Total valid distributions count (integer).

Constraints:
- Values kafi choti hain (`n, limit <= 50`), isliye brute-force ya O(limit^2) enumeration easily run ho jayega.

## 3. Example walkthrough

Example 1: n = 5, limit = 2
Bache 3 hain: (c1, c2, c3), jisme 0 <= c1, c2, c3 <= 2 aur c1 + c2 + c3 = 5.
Possible distributions check karte hain:
- Maximum total candies jo 3 bache le sakte hain wo 2 + 2 + 2 = 6 hai.
- Agar kisi ko 1 candy mile, to baki dono ko 2-2 milni padegi: (1, 2, 2), (2, 1, 2), (2, 2, 1).
- Agar kisi ko 0 candy mile, baki do milke max 4 hi ho sakte hain, 5 nahi ban payega.
Total ways = 3.

Example 2: n = 3, limit = 3
Yahan limit = 3 hai, toh kisi bhi child ko 0 se 3 candies mil sakti hain.
- c1 = 0: (0,0,3), (0,1,2), (0,2,1), (0,3,0) -> 4 ways
- c1 = 1: (1,0,2), (1,1,1), (1,2,0) -> 3 ways
- c1 = 2: (2,0,1), (2,1,0) -> 2 ways
- c1 = 3: (3,0,0) -> 1 way
Total ways = 4 + 3 + 2 + 1 = 10.

## 4. Brute-force approach

Teen nested loops use karein: child 1 ke liye `i` (0 to limit), child 2 ke liye `j` (0 to limit), child 3 ke liye `k` (0 to limit). Agar `i + j + k == n`, to counter increment karein. Yeh approach O(limit^3) time legi. Chuki limit <= 50, 50^3 = 125,000 operations, jo ki LeetCode par easily pass ho jayega, par third loop ki zaroorat nahi hai.

## 5. Optimized approach

Child 1 ko `i` candies dete hain (0 se min(n, limit)), aur Child 2 ko `j` candies dete hain (0 se min(n - i, limit)).
Ab teesre child ko exact `k = n - i - j` candies milni chahiye taaki sum `n` ho sake.
Humein bas yeh verify karna hai ki kya `0 <= k <= limit` satisfy ho raha hai. Agar haan, toh `ans++`.
Yeh nested 2 loops O(min(n, limit)^2) mein kaam karte hain, jo max 50 * 50 = 2500 operations hi leta hai.
(Alternative: Combinatorics / Inclusion-Exclusion Principle se yeh O(1) mein bhi solve ho sakta hai, jo Distribute Candies II mein kaam aata hai).

## 6. Dry run

Consider n = 5, limit = 2:
Initial ans = 0
- i = 0:
  - j = 0: k = 5 - 0 = 5 (> limit, invalid)
  - j = 1: k = 5 - 1 = 4 (invalid)
  - j = 2: k = 5 - 2 = 3 (invalid)
- i = 1:
  - j = 0: k = 4 (invalid)
  - j = 1: k = 3 (invalid)
  - j = 2: k = 5 - 1 - 2 = 2 (valid! ans = 1) -> (1, 2, 2)
- i = 2:
  - j = 0: k = 3 (invalid)
  - j = 1: k = 2 (valid! ans = 2) -> (2, 1, 2)
  - j = 2: k = 1 (valid! ans = 3) -> (2, 2, 1)
Result ans = 3.

## 7. Complexity

- **Time:** O(min(n, limit)^2) - Do nested loops hain jo at most `min(n, limit) + 1` iterations chalte hain. Maximum 51 * 51 ≈ 2600 operations, jo instantly execute hote hain.
- **Space:** O(1) - Sirf counters aur simple variables use ho rahe hain, koi extra space ya data structure nahi chahiye.

## 8. Common mistakes

- Teesre child ke candies ka check miss karna ki wo `k >= 0` ke saath-saath `k <= limit` bhi hona chahiye.
- Child ko 0 candies mil sakti hain, loop ko 1 se start karne ki galti karna.
- Agar n > 3 * limit ho, to directly 0 return kiya ja sakta hai kyunki 3 bache milkar bhi n candies nahi le sakte.

## 9. Self-check quiz

- **Q:** Agar n = 10 aur limit = 2 ho, to output kya aayega?
  **A:** 0, kyunki 3 bache milkar maximum 3 * 2 = 6 candies hi le sakte hain, 10 candies distribute karna impossible hai.
- **Q:** Kya kisi child ko 0 candies mil sakti hain?
  **A:** Haan, problem statement mein candies positive integers hain par distribution mein 0 allowed hai (jaise example 2 mein (0, 0, 3)).

## 10. Assumptions and caveats

Problem statement specifies positive integers n and limit, but children can receive 0 candies each as confirmed by Example 2.

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
