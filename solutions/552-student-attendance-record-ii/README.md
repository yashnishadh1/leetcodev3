# 552. Student Attendance Record II

- **Difficulty:** Hard
- **Problem:** https://leetcode.com/problems/student-attendance-record-ii/
- **Topics:** Dynamic Programming
- **Generated:** 2026-10-16

## 1. Problem ko simple Hinglish mein samjho

Humein length n ke aise total attendance strings ('P', 'A', 'L') find karne hain jo award ke eligible hon. Award ke liye 2 conditions hain: poori string me total 'A' (Absent) 2 se kam hone chahiye (matlab ya toh 0 ya 1 'A'), aur kabhi bhi consecutive 3 ya zyada 'L' (Late) nahi aane chahiye (matlab max consecutive 'L' 2 ho sakte hain). Answer modulo 10^9 + 7 return karna hai.

## 2. Input aur output

Input: Ek integer n (1 <= n <= 10^5) jo attendance record ki length represent karta hai.
Output: Total valid attendance records ki count modulo 10^9 + 7.

## 3. Example walkthrough

Example 1: n = 2
Total possible length 2 strings = 3^2 = 9 ('PP', 'PA', 'PL', 'AP', 'AA', 'AL', 'LP', 'LA', 'LL').
Invalid strings check karte hain:
- 'AA' me do 'A' hain (total 'A' < 2 hona chahiye tha), toh yeh invalid hai.
- Baaki sab me consecutive 'L' < 3 hain aur 'A' <= 1 hai. 'LL' valid hai kyunki 2 consecutive 'L' allowed hain (3 ya zyada mana hai).
Toh valid records = 9 - 1 = 8.

Example 2: n = 1
Possible strings: 'P', 'A', 'L'. Teeno valid hain, so output = 3.

## 4. Brute-force approach

Naive approach yeh hoga ki recursion/backtracking use karke har position pe 'P', 'A', aur 'L' rakh kar saare 3^n combinations generate karein aur check karein ki kisi me 2 'A' ya 3 consecutive 'L' toh nahi hain. Lekin n = 10^5 ke liye 3^(100000) operations lagenge jo instantly Time Limit Exceeded (TLE) dega.

## 5. Optimized approach

Is problem ko Dynamic Programming se bohot efficiently solve kiya ja sakta hai. Humein sirf do cheezein track karne ki zaroorat hoti hai:
1. Ab tak kitne 'A' aa chuke hain (sirf 0 ya 1 ho sakte hain, kyunki 2 aate hi invalid ho jayega).
2. String ke end me abhi kitne consecutive 'L' chal rahe hain (0, 1, ya 2).

Toh total states sirf 2 x 3 = 6 banti hain:
State: dp[total_A][trailing_L]

Har next day ke liye 3 choices hain:
- Add 'P': trailing_L ban jayega 0, total_A wahi rahega.
- Add 'A': trailing_L ban jayega 0, total_A 0 se 1 ho jayega (agar total_A already 1 tha toh 'A' nahi laga sakte).
- Add 'L': trailing_L increment ho jayega (trailing_L + 1), provided current trailing_L < 2. total_A wahi rahega.

Kyunki current day ka result sirf previous day ke 6 states par depend karta hai, hum O(1) space me rolling array ya 6 variables use karke O(n) time me solve kar sakte hain.

## 6. Dry run

Base state (Day 0, empty string):
dp[0][0] = 1, baaki saare 5 states 0 hain.

Day 1:
- Add 'P' to (0,0) -> dp[0][0] = 1 ('P')
- Add 'L' to (0,0) -> dp[0][1] = 1 ('L')
- Add 'A' to (0,0) -> dp[1][0] = 1 ('A')
Total sum = 1 + 1 + 1 = 3.

Day 2:
From dp[0][0] ('P'): +P -> (0,0), +A -> (1,0), +L -> (0,1)
From dp[0][1] ('L'): +P -> (0,0), +A -> (1,0), +L -> (0,2)
From dp[1][0] ('A'): +P -> (1,0), +L -> (1,1) [Cannot add 'A']
Naye values:
dp[0][0] = 1 + 1 = 2 ('PP', 'LP')
dp[0][1] = 1 ('PL')
dp[0][2] = 1 ('LL')
dp[1][0] = 1 + 1 + 1 = 3 ('AP', 'PA', 'LA')
dp[1][1] = 1 ('AL')
dp[1][2] = 0
Total sum = 2 + 1 + 1 + 3 + 1 + 0 = 8.

## 7. Complexity

- **Time:** O(n): Loop 1 se n tak chalta hai aur har step par sirf constant (6) states update hoti hain.
- **Space:** O(1): Hum sirf previous day ke 6 states store karte hain, koi bada array ya recursion stack nahi chahiye.

## 8. Common mistakes

- Consecutive 'L' aur total 'A' ko mix up kar dena; 'A' pure string ka total count hai jabki 'L' sirf consecutive count hai.
- Modulo 10^9 + 7 har addition step par na lagana, jisse integer overflow ho jaye.
- Bhool jana ki 'P' ya 'A' aane par consecutive 'L' ka streak reset hokar 0 ho jata hai.

## 9. Self-check quiz

- **Q:** Agar current state me trailing_L = 2 hai, toh kya hum next character 'L' add kar sakte hain?
  **A:** Nahi, kyunki criteria ke according 3 ya zyada consecutive 'L' strictly disallowed hain.
- **Q:** Total kitne unique DP states maintain karne padte hain har day ke liye?
  **A:** Sirf 6 states (count_A in {0, 1} * consec_L in {0, 1, 2}).

## 10. Assumptions and caveats

DP table ko rolling variables ke roop me rakha gaya hai taaki memory usage minimal rahe aur O(1) space guarantee ho.

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
