# 2094. Finding 3-Digit Even Numbers

- **Difficulty:** Easy
- **Problem:** https://leetcode.com/problems/finding-3-digit-even-numbers/
- **Topics:** Array, Hash Table, Recursion, Sorting, Enumeration
- **Generated:** 2026-10-11

## 1. Problem ko simple Hinglish mein samjho

Hame ek digits array di gayi hai jisme single-digit numbers (0-9) hain. Hame wo saare unique 3-digit even numbers find karne hain jo in digits me se koi bhi 3 distinct elements use karke banaye ja sakein. Important conditions: number 3-digit hona chahiye (leading zero allowed nahi hai), even hona chahiye (last digit 0, 2, 4, 6, 8 hona chahiye), aur final answer sorted order me unique numbers ka hona chahiye.

## 2. Input aur output

Input: `digits` array of integers (length 3 se 100, elements 0 to 9).
Output: Unique 3-digit even numbers ka sorted integer array (`List[int]` / `vector<int>` / `int[]`).
Constraints: digits ki length 3 to 100 hai, isliye agar brute force triple loop lagayein to bhi N^3 approx 10^6 iterations hoga. Par target range fixed hai: 100 to 999 (sirf 900 possible numbers).

## 3. Example walkthrough

Example 1: digits = [2, 1, 3, 0]
Possible 3-digit even numbers:
- Start digit 0 nahi ho sakta (leading zero not allowed).
- Last digit 0 ya 2 hona chahiye (even condition).
- 102: digits 1, 0, 2 use hue (valid).
- 120: 1, 2, 0 (valid).
- 130: 1, 3, 0 (valid).
- 132: 1, 3, 2 (valid).
- Aur baaki 210, 230, 302, 310, 312, 320 bhi valid hain.
Final sorted list: [102, 120, 130, 132, 210, 230, 302, 310, 312, 320].

Example 2: digits = [2, 2, 8, 8, 2]
Counts: 2 -> 3 baar, 8 -> 2 baar.
Valid combinations: 222, 228, 282, 288, 822, 828, 882.
Sab even hain aur 3-digit hain.

Example 3: digits = [3, 7, 5]
Koi bhi even digit (0, 2, 4, 6, 8) present nahi hai, so last digit even nahi ho sakta. Result: [].

## 4. Brute-force approach

Brute force approach me hum 3 nested loops chala sakte hain: `for i in range(n)`, `for j in range(n)`, `for k in range(n)` jahan `i != j` aur `j != k` aur `i != k` ho. Phir `digits[i] * 100 + digits[j] * 10 + digits[k]` banayenge. Check karenge ki `digits[i] != 0` ho aur number `% 2 == 0` ho. Uske baad ek Set me daalenge taaki duplicates na aayein, aur last me sort karke list return karenge. Time complexity O(N^3 + K log K) hogi. N = 100 ke liye 100^3 = 10^6 steps, jo ki pass to ho jayega par optimal nahi hai.

## 5. Optimized approach

Ulta socho (Enumeration on candidate numbers): Hame pata hai ki valid numbers sirf 100 se 999 tak ke even numbers ho sakte hain! (Yaani 100, 102, 104, ..., 998 - total sirf 450 numbers).
1. Pehle input `digits` array ki frequency map/array bana lo: `count[0..9]`.
2. Ek loop chalao `num` from 100 to 998 with step 2 (sirf even numbers check karne ke liye).
3. Har `num` ke teeno digits extract karo: `d1 = num / 100`, `d2 = (num / 10) % 10`, `d3 = num % 10`.
4. Check karo ki kya hamare input array me ye teeno digits available hain? Hum ek temporary frequency count le sakte hain ya directly verify kar sakte hain:
   - count[d1] > 0
   - count[d2] > 0 (taking care of count reduction if d1 == d2)
   - count[d3] > 0
5. Agar teeno available hain, to `num` ko result list me append kar do.
Kyunki hum 100 se 998 increasing order me loop kar rahe hain, result automatically sorted hoga aur duplicate check ki bhi jarurat nahi padegi!

## 6. Dry run

Input: digits = [2, 1, 3, 0]
Frequency array: count[0]=1, count[1]=1, count[2]=1, count[3]=1, baaki sab 0.
Loop starts: num = 100, 102, ..., 998 (step 2)
- num = 100: digits are 1, 0, 0. Needs two 0s, but count[0]=1 -> Not possible.
- num = 102: digits are 1, 0, 2. count[1]>=1, count[0]>=1, count[2]>=1 -> Valid! Result: [102]
- num = 104: requires 4, count[4]=0 -> Skip.
...
- num = 120: digits 1, 2, 0. Valid! Result: [102, 120]
Har valid even candidate direct order me milta jaata hai bina sorting ya set overhead ke.

## 7. Complexity

- **Time:** O(N + C) jahan N = digits array ki length (frequency count build karne ke liye) aur C = fixed constant iterations (450 numbers from 100 to 998 with step 2). Overall Time Complexity O(N) hai, jo ki extremely fast hai.
- **Space:** O(1) auxiliary space (excluding result array), kyunki frequency array ka size fixed 10 elements hai aur constant candidate space use hoti hai.

## 8. Common mistakes

- Leading zeros allow kar dena (jaise 012 ko count kar lena, jo ki 2-digit number hai).
- Same index ke element ko multiple baar use kar lena agar frequencies ka dhyan na rakha jaye.
- Output array ko sort karna bhool jana ya duplicate numbers ko remove na karna (agar permutations se banaya ho to).
- Odd numbers ko filter out na karna.

## 9. Self-check quiz

- **Q:** 100 se 999 ke beech me kitne unique even integers hote hain?
  **A:** Total 450 even integers (100, 102, ..., 998).
- **Q:** Candidate number enumeration approach me alag se sorting ki jarurat kyun nahi padti?
  **A:** Kyunki hum candidate loop ko already ascending order (100 se 998) me iterate karte hain, isliye numbers naturally sorted order me hi add hote hain.

## 10. Assumptions and caveats

Statement guarantees 3 <= digits.length <= 100 and digits[i] between 0 and 9. Enumerating 100 to 998 is both time-efficient and handles sorting automatically.

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
