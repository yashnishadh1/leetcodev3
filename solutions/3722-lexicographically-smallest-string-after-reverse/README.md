# 3722. Lexicographically Smallest String After Reverse

- **Difficulty:** Medium
- **Problem:** https://leetcode.com/problems/lexicographically-smallest-string-after-reverse/
- **Topics:** Two Pointers, Binary Search, Enumeration
- **Generated:** 2026-10-15

## 1. Problem ko simple Hinglish mein samjho

Humein ek string `s` di gayi hai length `n` ki. Humein exactly ek operation perform karna hai: koi bhi integer `k` choose karo ($1 \le k \le n$), aur ya toh pehle `k` characters ko reverse karo ya last ke `k` characters ko reverse karo. Aisa karne ke baad jo lexicographically smallest string ban sakti hai, use return karna hai.

## 2. Input aur output

Input: Ek string `s` jisme lowercase English letters hain (length $n$ between 1 and 1000).
Output: Single string jo exactly ek valid reverse operation ke baad lexicographically smallest ho.
Constraints: $1 \le n \le 1000$, string sirf lowercase English letters contain karti hai.

## 3. Example walkthrough

Example 1: s = 'dcab'
- Option 1 (Prefix k=3): 'dca' reverse hoke 'acd' ban jayega, baki 'b' waisa hi rahega -> 'acdb'.
- Ye sabhi $2n$ possibilities me se lexicographically sabse chhota hai, isliye answer 'acdb' hai.

Example 2: s = 'abba'
- Option 2 (Suffix k=3): Last 3 chars 'bba' ko reverse kiya -> 'abb', first char 'a' waise hi raha -> 'aabb'.
- Result: 'aabb'.

Example 3: s = 'zxy'
- Prefix k=2: 'zx' reverse hoke 'xz' ban gaya -> 'xzy'.
- Result: 'xzy'.

## 4. Brute-force approach

Har possible operation ko simulate karna: $k$ ki value 1 se lekar $n$ tak ho sakti hai. Har $k$ ke liye do choices hain: ya toh prefix reverse karo (0 to k-1) ya suffix reverse karo (n-k to n-1). Total $2n$ combinations hain. Har candidate string generate karke minimum track kar lo. Kyunki $n \le 1000$, total states $2000$ hain aur har string generation/comparison $O(n)$ leta hai, toh total time $O(n^2)$ hoga jo ki ~10^6 operations hai aur 1 second ke limit se bohot easily pass ho jayega.

## 5. Optimized approach

Given constraints ($n \le 1000$) ke hisab se $O(n^2)$ brute-force enumeration hi intended aur optimal simple solution hai. Algorithm:
1. Ek variable `best` maintain karo, initially set to `s`.
2. $k = 1$ se $n$ tak loop chalao.
3. Har $k$ ke liye:
   - Prefix reverse candidate banao: reverse `s[0...k-1]` and concatenate `s[k...n-1]`.
   - Suffix reverse candidate banao: `s[0...n-k-1]` concatenate reverse `s[n-k...n-1]`.
   - Agar koi candidate `best` se lexicographically chhota hai, toh `best` ko update karo.
4. Loop khatam hone par `best` return karo.

## 6. Dry run

String s = 'dcab', n = 4. Initially best = 'dcab'.
- k = 1: Prefix rev -> 'dcab', Suffix rev -> 'dcab' (best = 'dcab')
- k = 2: Prefix rev (dc -> cd) -> 'cdab' (chhota hai, best = 'cdab'); Suffix rev (ab -> ba) -> 'dcba'
- k = 3: Prefix rev (dca -> acd) -> 'acdb' (aur chhota hai, best = 'acdb'); Suffix rev (cab -> bac) -> 'dbac'
- k = 4: Prefix/Suffix rev (dcab -> bacd) -> 'bacd'
Final best = 'acdb'.

## 7. Complexity

- **Time:** O(n^2): Loop 1 se n tak chalta hai ($n$ iterations). Har iteration me 2 strings create aur compare hoti hain jo $O(n)$ time leti hain. Overall time = $2 \times n \times O(n) = O(n^2)$, jisme $n=1000$ par max $2 \times 10^6$ operations honge, easily passing within ~50ms.
- **Space:** O(n): Har step par candidate string generate karne ke liye $O(n)$ temporary space chahiye hota hai.

## 8. Common mistakes

- k=1 aur k=n ke boundary cases me 0-based indexing handle karte waqt off-by-one errors (jaise suffix ka start point galat lena: n - k hona chahiye).
- Ye bhool jana ki exact ek operation karna mandatory hai (halanki k=1 choose karne par string unchanged hi rehti hai, toh original string valid answer ho sakti hai).
- Overcomplicating the problem: Sochna ki greedy ya advanced string algorithms (like suffix automaton) ki zaroorat hai, jabki n <= 1000 me simple enumeration hi kafi hai.

## 9. Self-check quiz

- **Q:** Total kitni distinct operations check karni padengi length n ke liye?
  **A:** At most 2 * n operations (n prefix reverses aur n suffix reverses).
- **Q:** Kya k=1 lene par string change hoti hai?
  **A:** Nahi, single character ko reverse karne se string exactly same rehti hai.

## 10. Assumptions and caveats

LeetCode constraints me n <= 1000 diya gaya hai, isliye O(n^2) time complexity perfectly acceptable aur optimal implementation choice hai.

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
