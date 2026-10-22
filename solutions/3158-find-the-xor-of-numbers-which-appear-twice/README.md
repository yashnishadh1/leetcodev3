# 3158. Find the XOR of Numbers Which Appear Twice

- **Difficulty:** Easy
- **Problem:** https://leetcode.com/problems/find-the-xor-of-numbers-which-appear-twice/
- **Topics:** Array, Hash Table, Bit Manipulation
- **Generated:** 2026-10-20

## 1. Problem ko simple Hinglish mein samjho

Hume ek integer array `nums` diya gaya hai jisme har number ya toh ek baar aata hai ya do baar. Hume un sabhi numbers ka bitwise XOR calculate karke return karna hai jo array me exactly do baar (twice) appear hote hain. Agar koi bhi number do baar nahi aata, toh 0 return karna hai.

## 2. Input aur output

Input: `nums` (ek integer array, size 1 se 50 ke beech, har element ki value bhi 1 se 50 ke beech).
Output: Ek single integer jo un sabhi elements ka bitwise XOR hoga jo array me twice appear hue hain.
Constraints: Array length aur values choti hain (<= 50). Har number sirf 1 ya 2 baar hi aa sakta hai.

## 3. Example walkthrough

Example 1: nums = [1, 2, 1, 3]
- Elements count: 1 -> 2 baar, 2 -> 1 baar, 3 -> 1 baar.
- Only '1' appears twice. Result = 1.

Example 2: nums = [1, 2, 3]
- Koi bhi element do baar nahi aaya. Sab 1 baar hain.
- Result = 0.

Example 3: nums = [1, 2, 2, 1]
- Elements count: 1 -> 2 baar, 2 -> 2 baar.
- Dono twice aaye hain, so hume unka XOR nikalna hai: 1 XOR 2 = 3.
- Result = 3.

## 4. Brute-force approach

Brute force approach me hum nested loops use kar sakte hain. Outer loop me har element nums[i] uthao aur inner loop me check karo ki kya wo aage dobara repeat ho raha hai (nums[j] == nums[i]). Agar repeat ho raha hai, toh use result variable ke sath XOR kar do (`ans ^= nums[i]`). Yeh O(n^2) time lega. Given n <= 50, yeh bhi accept ho jayega, par hash set ya frequency array se hum isse linearly solve kar sakte hain.

## 5. Optimized approach

Optimized approach ke liye hum ek Hash Set ya Boolean Array (ya Frequency Array) use karenge.
Intuition: Array me traverse karte waqt agar element pehle se set me nahi hai, toh set me add kar do (iska matlab yeh pehli baar dekha gaya hai). Agar element pehle se set me present hai, iska matlab yeh doosri baar aaya hai! Jaise hi doosri baar dikhe, use hum apne `xor_sum` variable me XOR kar denge (`xor_sum ^= num`).
Kyunki constraints me numbers 1 se 50 tak hi hain, hum ek simple boolean array ya bitmask bhi use kar sakte hain to achieve O(1) space, but HashSet/Array dono O(N) time me easily kaam karenge.

## 6. Dry run

Input: nums = [1, 2, 2, 1]
Initial: seen = {}, ans = 0

1. num = 1:
   - Kya 1 'seen' me hai? Nahi.
   - seen = {1}, ans = 0
2. num = 2:
   - Kya 2 'seen' me hai? Nahi.
   - seen = {1, 2}, ans = 0
3. num = 2:
   - Kya 2 'seen' me hai? Haan!
   - ans = ans ^ 2 = 0 ^ 2 = 2
4. num = 1:
   - Kya 1 'seen' me hai? Haan!
   - ans = ans ^ 1 = 2 ^ 1 = 3

Final Output: 3

## 7. Complexity

- **Time:** O(N) - Hume array ko sirf ek baar iterate karna padta hai. Set operations (insert aur lookup) average O(1) time leti hain. (N <= 50, toh operations at most 50 hain).
- **Space:** O(N) ya O(1) - Agar HashSet use karte hain toh max 50 unique elements store honge (O(N)). Agar fixed-size boolean array ya 64-bit integer bitmask use karein toh auxiliary space O(1) hai.

## 8. Common mistakes

- Pure array ka XOR nikal lena: Yaad rahe single appearance wale elements ko ignore karna hai, pure array ka XOR nikalne se answer galat ho jayega (kyunki single element ek baar XOR hoga aur duplicate wale cancel out hoke 0 ban jayenge, jo problem ke ulta hai).
- Initial answer ko 0 ke alawa kisi aur value se initialize karna: XOR me 0 neutral identity hota hai (0 ^ X = X).

## 9. Self-check quiz

- **Q:** Agar hum direct saare elements ka XOR le lein (`a ^ b ^ c...`), toh duplicates ke sath kya hota hai?
  **A:** Duplicate elements a ^ a ban ke 0 ban jate hain aur cancel ho jate hain, jabki hume exactly duplicate elements ka hi XOR chahiye.
- **Q:** XOR operation me identity element kya hota hai (i.e. x ^ ? = x)?
  **A:** 0 hota hai (x ^ 0 = x).

## 10. Assumptions and caveats

Problem statement specifies ki har element ya toh once aayega ya twice (never 3 or more times). Is guarantee ki wajah se first time seen check karna aur second time aane par directly XOR kar dena completely safe hai.

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
