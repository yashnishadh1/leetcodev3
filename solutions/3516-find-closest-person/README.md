# 3516. Find Closest Person

- **Difficulty:** Easy
- **Problem:** https://leetcode.com/problems/find-closest-person/
- **Topics:** Math
- **Generated:** 2026-10-18

## 1. Problem ko simple Hinglish mein samjho

Number line par 3 log hain: Person 1 at x, Person 2 at y, aur Person 3 at z (jo move nahi karta). Person 1 aur Person 2 dono same speed se Person 3 ki taraf chalte hain. Hume batana hai ki Person 3 ke paas pehle kaun pahuchega. Agar Person 1 pehle pahuche to 1 return karo, agar Person 2 pehle pahuche to 2, aur agar dono ek hi time par pahunchein to 0 return karo.

## 2. Input aur output

Input: Teen integers x, y, z (1 <= x, y, z <= 100).
Output: Ek integer: 1 (agar Person 1 jeete), 2 (agar Person 2 jeete), ya 0 (agar tie ho).

## 3. Example walkthrough

Example 1: x = 2, y = 7, z = 4.
- Person 1 ka distance: |2 - 4| = 2
- Person 2 ka distance: |7 - 4| = 3
- 2 < 3, isliye Person 1 pehle pahuchega. Output = 1.

Example 2: x = 2, y = 5, z = 6.
- Person 1 ka distance: |2 - 6| = 4
- Person 2 ka distance: |5 - 6| = 1
- 1 < 4, isliye Person 2 pehle pahuchega. Output = 2.

Example 3: x = 1, y = 5, z = 3.
- Person 1 ka distance: |1 - 3| = 2
- Person 2 ka distance: |5 - 3| = 2
- Dono ka distance equal hai (2 == 2), isliye dono saath pahucheinge. Output = 0.

## 4. Brute-force approach

Simulation approach: Har step pe Person 1 aur Person 2 ko 1 unit z ki taraf move karo jab tak koi z tak na pahunch jaye. Lekin yeh unnecessary loop chalayega jabki distance direct formula se nikal sakta hai.

## 5. Optimized approach

Speed constant hai, isliye jo paas hoga wahi pehle pahuchega. Bas absolute difference calculate karna hai: dist1 = |x - z| aur dist2 = |y - z|. Fir compare karke check karo: agar dist1 < dist2 toh 1, agar dist2 < dist1 toh 2, warna dono barabar hone par 0.

## 6. Dry run

Input: x = 2, y = 7, z = 4
Step 1: dist1 = abs(2 - 4) = 2
Step 2: dist2 = abs(7 - 4) = 3
Step 3: Check dist1 < dist2 (2 < 3) -> True
Result: 1

## 7. Complexity

- **Time:** O(1) kyunki sirf basic arithmetic subtraction aur comparison ho raha hai.
- **Space:** O(1) kyunki koi extra memory ya data structure use nahi ho raha.

## 8. Common mistakes

- Absolute value (abs) lena bhool jana: bina abs ke subtraction negative ho sakta hai aur comparison galat ho jayega.
- Variable mapping confuse kar dena, jaise x aur y ko swap kar dena ya z ko galat person samajh lena.

## 9. Self-check quiz

- **Q:** Agar x = 4, y = 4, z = 4 ho toh output kya hoga?
  **A:** Output 0 hoga kyunki dono already z par hain (dono ka distance 0 hai, jo barabar hai).
- **Q:** Agar absolute difference na use karein toh kya issue aayega?
  **A:** Negative differences aa sakte hain, jaise 2 - 4 = -2, jisse galat comparison ho jayegi kyunki distance hamesha non-negative hota hai.

## 10. Assumptions and caveats

LeetCode 3516 standard absolute distance comparison problem hai. Constraints 1 <= x, y, z <= 100 hain, overflow ki koi possibility nahi hai.

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
