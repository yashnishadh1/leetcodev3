# 2481. Minimum Cuts to Divide a Circle

- **Difficulty:** Easy
- **Problem:** https://leetcode.com/problems/minimum-cuts-to-divide-a-circle/
- **Topics:** Math, Geometry
- **Generated:** 2026-10-13

## 1. Problem ko simple Hinglish mein samjho

Hamein ek circle ko `n` barabar slices mein divide karna hai. Cut sirf do types ke allowed hain: (1) edge se edge tak jo center se guzre (diameter cut), ya (2) center se circle ke edge tak (radius cut). Hamein batana hai ki minimum kitne cuts lagenge.

## 2. Input aur output

Input: Ek integer `n` (1 <= n <= 100), jo slices ki count represent karta hai.
Output: Minimum number of cuts (integer).
Constraints: `n` bohot chhota hai (1 se 100 tak).

## 3. Example walkthrough

Example 1: n = 4
- Even number hai. Agar hum 1 diameter cut lagayein, toh 2 halves bante hain. Ek aur perpendicular diameter cut lagayein, toh 4 equal slices mil jaate hain.
- Total cuts = 4 / 2 = 2.

Example 2: n = 3
- Odd number hai (aur > 1). Diameter cut dono sides barabar slices banata hai, toh odd count ke liye diameter cut direct use nahi ho sakta bina symmetry tode.
- Isliye center se edge tak radius cuts lagane padenge (3 alag alag angles par).
- Total cuts = 3.

Edge Case: n = 1
- Circle already 1 slice hi hai, koi cut lagane ki zaroorat nahi.
- Output = 0.

## 4. Brute-force approach

Yeh purely mathematical aur geometrical observation based problem hai. Isme koi loop ya brute force simulation ki need nahi hoti, direct condition check kaam karti hai.

## 5. Optimized approach

Geometrical intuition:
1. Base case: Agar `n == 1`, circle already complete hai, 0 cuts chahiye.
2. Even `n`: Har diameter cut circle ko 2 opposite equal sectors mein divide karta hai. Toh ek cut se 2 sectors bante hain. Agar `n` even hai, toh `n / 2` diameter cuts poore circle ko `n` equal pieces mein baant denge.
3. Odd `n`: Odd sectors ke liye opposite boundary align nahi hoti, isliye full diameter cuts se symmetry nahi ban sakti. Hamein center se start karke perimeter tak radius cuts lagane honge, jo exactly `n` cuts honge.

## 6. Dry run

| n | Condition | Calculation | Result |
|---|---|---|---|
| 1 | n == 1 | Special base case | 0 |
| 2 | n % 2 == 0 | 2 / 2 | 1 |
| 3 | n % 2 != 0 | n | 3 |
| 4 | n % 2 == 0 | 4 / 2 | 2 |
| 5 | n % 2 != 0 | n | 5 |

## 7. Complexity

- **Time:** O(1) - Sirf basic arithmetic aur conditional check hai.
- **Space:** O(1) - Koi extra memory allocate nahi hoti.

## 8. Common mistakes

- n = 1 ko handle karna bhool jana (n = 1 par 1 return kar dena jabki answer 0 hona chahiye).
- Odd n ke liye ceiling division sochna, jabki odd cases mein har boundary radius cut se hi banti hai toh answer exactly n hota hai.

## 9. Self-check quiz

- **Q:** Agar n = 6 ho, toh minimum kitne cuts lagenge?
  **A:** 3 cuts, kyunki 6 even hai toh 6 / 2 = 3 diameter cuts lagenge.
- **Q:** n = 1 ke case mein output 1 kyun nahi hota?
  **A:** Kyunki circle ko divide kiye bina hi wo already 1 single slice represent karta hai, isliye 0 cuts chahiye.

## 10. Assumptions and caveats

Statement standard geometry par based hai: diameter cuts require opposite symmetry jo sirf even slices ke liye direct kaam karta hai (except n=1).

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
