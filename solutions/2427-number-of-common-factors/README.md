# 2427. Number of Common Factors

- **Difficulty:** Easy
- **Problem:** https://leetcode.com/problems/number-of-common-factors/
- **Topics:** Math, Enumeration, Number Theory, Euclidean Algorithm, Greatest Common Divisor
- **Generated:** 2026-10-13

## 1. Problem ko simple Hinglish mein samjho

Hame do positive integers 'a' aur 'b' diye gaye hain. Hame batana hai ki kitne aise numbers 'x' hain jo dono 'a' aur 'b' ko perfectly divide karte hain (yani remainder 0 aata hai). Basically, 'a' aur 'b' ke common factors ka count find karna hai.

## 2. Input aur output

Input: Do positive integers 'a' aur 'b' (Constraints: 1 <= a, b <= 1000).
Output: Ek single integer jo represent karta hai common factors ka total count.

## 3. Example walkthrough

Example 1: a = 12, b = 6
Factors of 12: 1, 2, 3, 4, 6, 12
Factors of 6: 1, 2, 3, 6
Common factors jo dono ko divide karte hain: 1, 2, 3, 6. Total count = 4.

Example 2: a = 25, b = 30
Factors of 25: 1, 5, 25
Factors of 30: 1, 2, 3, 5, 6, 10, 15, 30
Common factors: 1, 5. Total count = 2.

## 4. Brute-force approach

Brute force approach ye hai ki 1 se lekar min(a, b) tak har integer 'i' ke liye check karo ki kya (a % i == 0) aur (b % i == 0) dono true hain ya nahi. Agar dono true hain, toh counter ko 1 se badha do. Constraints bohot chote hain (up to 1000), toh ye approach easily pass ho jayegi.

## 5. Optimized approach

Number theory ki ek property hoti hai: 'a' aur 'b' ke saare common factors unke Greatest Common Divisor (GCD) ke bhi factors hote hain. Toh hum pehle g = gcd(a, b) nikal sakte hain Euclidean Algorithm use karke. Phir bas 'g' ke factors count karne hain. Kisi number 'g' ke factors count karne ke liye hum 1 se lekar sqrt(g) tak loop chala sakte hain: agar 'i' divides 'g', toh 'i' ek factor hai aur agar (i != g / i) toh (g / i) dusra factor hai. Isse time complexity O(log(min(a,b)) + sqrt(gcd(a, b))) ho jaati hai.

## 6. Dry run

Dry run for a = 12, b = 6 using GCD approach:
1. g = gcd(12, 6) = 6
2. Count factors of 6 by iterating i from 1 to sqrt(6) ≈ 2:
   - i = 1: 6 % 1 == 0 -> true. Pair is (1, 6). Dono distinct hain, count += 2 (count = 2).
   - i = 2: 6 % 2 == 0 -> true. Pair is (2, 3). Dono distinct hain, count += 2 (count = 4).
3. Loop ends. Total count = 4.

## 7. Complexity

- **Time:** O(sqrt(gcd(a, b))) optimized approach ke liye (ya O(min(a, b)) brute force ke liye). Euclidean algorithm O(log(min(a, b))) leta hai aur sqrt check O(sqrt(g)) leta hai, jo dono hi 1000 ke limit ke liye extremely fast (< 1ms) hain.
- **Space:** O(1) auxiliary space kyunki hum sirf constant number of variables use kar rahe hain.

## 8. Common mistakes

- Loop ko min(a, b) ke bajaye max(a, b) tak chalana (halaki answer same aayega par extra operations honge kyunki min se bada koi common factor nahi ho sakta).
- Optimized approach mein sqrt check karte time perfect squares ke case mein duplicate count karna (jaise i * i == g par ek hi baar count hona chahiye).
- 0 se loop start karna jisse DivisionByZero error aa jaye.

## 9. Self-check quiz

- **Q:** Agar do numbers coprime hain (jaise a = 8, b = 9), toh common factors ka count kya hoga?
  **A:** 1, kyunki coprime numbers ka GCD 1 hota hai aur unka ek hi common factor hota hai: 1.
- **Q:** Kya 1 hamesha kisi bhi do positive integers ka common factor hota hai?
  **A:** Haan, kyunki 1 har positive integer ko perfectly divide karta hai.

## 10. Assumptions and caveats

Constraints 1 <= a, b <= 1000 bohot small hain, isliye simple O(min(a, b)) iteration bhi completely acceptable hai. Par GCD-based O(sqrt(gcd(a, b))) solution number-theory ke perspective se standard aur scalable hai.

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
