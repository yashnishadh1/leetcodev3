# 1461. Check If a String Contains All Binary Codes of Size K

- **Difficulty:** Medium
- **Problem:** https://leetcode.com/problems/check-if-a-string-contains-all-binary-codes-of-size-k/
- **Topics:** Hash Table, String, Bit Manipulation, Rolling Hash, Hash Function, Directed Acyclic Graph
- **Generated:** 2026-10-10

## 1. Problem ko simple Hinglish mein samjho

Hamein ek binary string `s` aur integer `k` diya gaya hai. Hamein check karna hai ki kya size `k` ke saare possible binary codes (total 2^k codes) string `s` ke andar as a substring exist karte hain ya nahi. Agar saare exist karte hain toh true return karo, warna false.

## 2. Input aur output

Input: `s` (binary string consisting only of '0' and '1'), `k` (integer representing length of binary codes).
Output: `true` ya `false` (boolean).
Constraints: 1 <= s.length <= 5 * 10^5, k <= 20. Dhyaan rahe 2^20 lagbhag 10^6 hota hai.

## 3. Example walkthrough

Example 1: s = '00110110', k = 2.
Size 2 ke binary codes hote hain: 2^2 = 4 combinations ('00', '01', '10', '11').
Substring dekhte hain length 2 ki: '00' (idx 0), '01' (idx 1), '11' (idx 2), '10' (idx 3), etc.
Saare 4 codes cover ho gaye, toh answer hai true.

Example 2: s = '0110', k = 1.
Codes of size 1: '0', '1' (total 2^1 = 2).
s me '0' aur '1' dono present hain. So answer is true.

Example 3: s = '0110', k = 2.
Size 2 ke codes: '00', '01', '10', '11'.
Substring length 2: '01', '11', '10'.
'00' missing hai! Isliye answer false hai.

## 4. Brute-force approach

Har ek binary code generate karo 0 se lekar 2^k - 1 tak. Phir har binary code ko check karo ki kya wo `s` ka substring hai (using `s.find()` ya naive search). Total 2^k codes hain aur har search O(N) le sakta hai, so time complexity O(2^k * N) hogi. Agar N = 5 * 10^5 aur k = 20, ye definitely Time Limit Exceeded (TLE) dega.

## 5. Optimized approach

Do approaches hain:
1. HashSet approach: `s` ke saare substrings of length `k` nikaalo aur ek HashSet me insert kar do. HashSet ka size agar 2^k ke barabar ho gaya, toh return true. Early exit: Agar baaki bache substrings itne kam hain ki total 2^k kabhi nahi ban sakte, directly return false. Par string slicing aur hashing extra memory and time leti hai.

2. Rolling Hash / Bit Manipulation + Boolean Array / BitSet:
Length `k` ke binary string ko ek integer me represent kar sakte hain. Jab sliding window ek step right move karti hai:
- Naya integer value = `((val << 1) & all_ones_mask) | new_bit`
Yahan `all_ones_mask = (1 << k) - 1` purana leftmost bit drop kar deta hai.
Hum ek boolean array ya bitset of size `1 << k` rakhte hain. Har window ke integer value par visit mark karte hain aur unique count track karte hain. Jab count == 2^k ho jaye, turant return true! Ye O(1) per step aur minimal memory me kaam karta hai.

## 6. Dry run

s = '00110110', k = 2. Target unique codes = 2^2 = 4. Mask = (1 << 2) - 1 = 3 (binary 11).
Initial window (first k bits): '00' -> val = 0. Visited[0] = true, count = 1.
Step i=2 (char '1'): val = ((0 << 1) & 3) | 1 = 1 ('01'). Visited[1] = true, count = 2.
Step i=3 (char '1'): val = ((1 << 1) & 3) | 1 = 3 ('11'). Visited[3] = true, count = 3.
Step i=4 (char '0'): val = ((3 << 1) & 3) | 0 = 2 ('10'). Visited[2] = true, count = 4.
count == 4 (target reached) -> Return true immediately!

## 7. Complexity

- **Time:** O(N) jahan N = s.length(). Hum string ko ek hi baar traverse karte hain aur bit operations O(1) time leti hain.
- **Space:** O(2^k) boolean flags store karne ke liye. Maximum 2^20 bits ya booleans jo lagbhag 1 MB memory legi.

## 8. Common mistakes

- Check na karna agar s.length() < (1 << k) + k - 1, kyunki agar string hi itni choti hai ki 2^k unique k-length substrings fit na ho sakein, seedha false return kar sakte hain.
- Bit manipulation me 1 << k overflow hone dena agar k = 31+ ho (halanki yahan k <= 20 hai, fir bhi safe bounds dhyan rakhna zaroori hai).
- Substrings ko bar-bar string form me HashSet me daalna, jisse O(N * k) time aur string overhead lagta hai, jo k=20 pe memory limit exceed kar sakta hai.

## 9. Self-check quiz

- **Q:** Size k ke total kitne unique binary strings hote hain?
  **A:** 2^k unique binary strings hote hain.
- **Q:** Agar string `s` ki length 2^k + k - 1 se kam ho, toh kya possible hai ki saare binary codes present hon?
  **A:** Nahi, kyunki 2^k distinct length-k substrings hone ke liye string ki minimum length 2^k + k - 1 honi chahiye (de Bruijn sequence ki length).

## 10. Assumptions and caveats

k <= 20 diya gaya hai, iska matlab 2^k maximum 1,048,576 hoga. Standard boolean array / bitset is easily feasible within memory limits.

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
