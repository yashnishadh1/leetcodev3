# 2469. Convert the Temperature

- **Difficulty:** Easy
- **Problem:** https://leetcode.com/problems/convert-the-temperature/
- **Topics:** Math
- **Generated:** 2026-10-19

## 1. Problem ko simple Hinglish mein samjho

Humein ek non-negative floating-point number diya gaya hai jo temperature Celsius mein represent karta hai. Humein is Celsius temperature ko Kelvin aur Fahrenheit mein convert karna hai aur result ko ek array `[kelvin, fahrenheit]` ke format mein return karna hai.

## 2. Input aur output

Input: `celsius` (double / float type, 0 <= celsius <= 1000).
Output: Ek array / list jismein 2 elements honge: `[kelvin, fahrenheit]`.
Constraints: Answer accurate hona chahiye within 10^-5 precision.

## 3. Example walkthrough

Example 1:
Input: celsius = 36.50
- Kelvin formula: celsius + 273.15 = 36.50 + 273.15 = 309.65
- Fahrenheit formula: celsius * 1.80 + 32.00 = 36.50 * 1.80 + 32.00 = 65.70 + 32.00 = 97.70
Output: [309.65, 97.70]

Example 2:
Input: celsius = 122.11
- Kelvin = 122.11 + 273.15 = 395.26
- Fahrenheit = 122.11 * 1.80 + 32.00 = 219.798 + 32.00 = 251.798
Output: [395.26, 251.798]

## 4. Brute-force approach

Yeh ek direct mathematical calculation problem hai. Isme koi loops ya complex data structures ki zarurat nahi hai. Sidha formula apply karke list/array return karna hi simplest aur direct way hai.

## 5. Optimized approach

Given formulas direct use karenge:
1. `kelvin = celsius + 273.15`
2. `fahrenheit = celsius * 1.80 + 32.00` (ya `celsius * 9 / 5 + 32`)
Directly ek 2-element array ya vector banakar return kar denge. Isme standard double-precision floating point numbers ka use hota hai jo automatic 10^-5 precision handle kar lete hain.

## 6. Dry run

Input: celsius = 36.50
Step 1: kelvin = 36.50 + 273.15 = 309.65
Step 2: fahrenheit = 36.50 * 1.80 + 32.00 = 65.7 + 32.00 = 97.7
Step 3: ans = [309.65, 97.7]
Result: [309.65, 97.70]

## 7. Complexity

- **Time:** O(1) kyunki sirf basic constant time arithmetic operations (+, *) perform ho rahe hain.
- **Space:** O(1) auxiliary space kyunki sirf ek fixed size (2 elements) ka array/vector banaya ja raha hai output ke liye.

## 8. Common mistakes

- Integer division mistake: Agar Celsius ko 9/5 se multiply kar rahe ho toh integer division (9/5 = 1) na ho jaye, hamesha 9.0/5.0 ya 1.80 use karo.
- Output array ka order galat karna: Pehle Kelvin aana chahiye, fir Fahrenheit.
- Precision loss: Float ki jagah double use karna standard rehta hai accuracy preserve karne ke liye.

## 9. Self-check quiz

- **Q:** Is problem mein time complexity O(1) kyu hai?
  **A:** Kyunki input size chahe jo bhi ho, calculation sirf ek baar fixed constant time arithmetic operations ke sath hoti hai.
- **Q:** Agar hum Fahrenheit ke liye `celsius * (9 / 5) + 32` likhte hain C++ ya Java mein, toh output galat kyu aayega?
  **A:** Kyunki `9 / 5` integer division evaluate hoke `1` ban jayega, jisse formula galat ho jayega. Hamein `9.0 / 5.0` ya `1.8` likhna chahiye.

## 10. Assumptions and caveats

LeetCode allows answers within 10^-5 precision of the actual value. Standard 64-bit IEEE 754 floating point (double) easily fulfills this requirement.

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
