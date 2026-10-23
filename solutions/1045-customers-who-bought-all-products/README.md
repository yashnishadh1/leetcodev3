# 1045. Customers Who Bought All Products

- **Difficulty:** Medium
- **Problem:** https://leetcode.com/problems/customers-who-bought-all-products/
- **Topics:** Database
- **Generated:** 2026-10-23

## 1. Problem ko simple Hinglish mein samjho

Humein un sabhi `customer_id`s ko find karna hai jinhone `Product` table ke saare products buy kiye hain. Customer table mein duplicate rows ho sakti hain, isliye unique products count karna zaroori hai.

## 2. Input aur output

Input do tables hain: `Customer` (customer_id, product_key) jisme duplicate entries ho sakti hain, aur `Product` (product_key) jo primary key hai. Output mein single column `customer_id` return karna hai un customers ke liye jinhone `Product` table ke har ek unique product ko khareeda ho. Order kisi bhi sequence mein ho sakta hai.

## 3. Example walkthrough

Example 1:
Product table mein 2 products hain: [5, 6]. Total count = 2.
Customer table records:
- Customer 1: products {5, 6} khareede -> Total distinct products = 2 (Match!)
- Customer 2: products {6} khareeda -> Total distinct products = 1 (Not matching 2)
- Customer 3: products {5, 6} khareede -> Total distinct products = 2 (Match!)
Output customer_id honge: 1 aur 3.

## 4. Brute-force approach

Har ek customer ke liye unke purchased products ka set nikalo, fir Product table ke sabhi keys ke set ke saath compare karo. Database level par ye correlated subqueries ya heavy joins ke barabar hai, jo inefficient ho sakta hai.

## 5. Optimized approach

Hum `GROUP BY customer_id` karenge aur `HAVING` clause ka use karke count compare karenge.
1. Total unique products ki sankhya nikalne ke liye subquery: `(SELECT COUNT(*) FROM Product)`.
2. `Customer` table ko `customer_id` se group karo.
3. Filter condition: `COUNT(DISTINCT product_key) = (SELECT COUNT(*) FROM Product)`.
Kyunki `product_key` foreign key hai, koi invalid product_key Customer table me nahi ho sakti. Bas duplicates avoid karne ke liye `DISTINCT` use karna padega.

## 6. Dry run

Product table count = 2

Customer Table Grouped by customer_id:
| customer_id | distinct product_keys | COUNT(DISTINCT product_key) | Condition: count == 2 | Selected? |
|---|---|---|---|---|
| 1 | {5, 6} | 2 | 2 == 2 (True) | Yes |
| 2 | {6} | 1 | 1 == 2 (False) | No |
| 3 | {5, 6} | 2 | 2 == 2 (True) | Yes |

Final Result: customer_id 1, 3.

## 7. Complexity

- **Time:** O(N + M), jahan N Customer table ki rows hain aur M Product table ki rows hain. Ek scan Product count nikalne ke liye aur hashing/sorting based grouping Customer table par.
- **Space:** O(U), jahan U unique customers ka count hai jo grouping/aggregation hash table ya intermediate buffer mein store hote hain.

## 8. Common mistakes

- Bhul jana ki Customer table mein duplicates ho sakte hain, isliye `COUNT(product_key)` ki jagah `COUNT(DISTINCT product_key)` use karna compulsory hai.
- Ye assume karna ki Customer table mein Product table ke bahar ki keys ho sakti hain (statement me foreign key mention hai, par distinct count hi safe approach hai).

## 9. Self-check quiz

- **Q:** Agar ek customer ne ek hi product multiple times khareeda ho, toh simple `COUNT(product_key)` use karne se kya issue hoga?
  **A:** Simple COUNT duplicates ko bhi count kar lega, jisse lagega customer ne multiple different products khareede hain jabki unhone actually wahi same product baar baar khareeda hai.
- **Q:** Kya `product_key` Product table me duplicate ho sakti hai?
  **A:** Nahi, kyunki problem statement ke according `product_key` Product table ki primary key hai.

## 10. Assumptions and caveats

LeetCode par SQL problem hai. Solutions section me standard SQL solutions include kiye gaye hain. Pandas implementation Python ke liye di gayi hai.

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
