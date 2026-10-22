# 1117. Building H2O

- **Difficulty:** Medium
- **Problem:** https://leetcode.com/problems/building-h2o/
- **Topics:** Concurrency
- **Generated:** 2026-10-17

## 1. Problem ko simple Hinglish mein samjho

Humare paas do tarah ke threads hain: Hydrogen (H) aur Oxygen (O). Hume in threads ko synchronize karna hai taaki har ek molecule banate waqt exactly do 'H' aur ek 'O' thread barrier cross karein. Har 3 threads ka group strictly 2 H aur 1 O contain kare, kisi bhi order mein (jaise HHO, HOH, ya OHH).

## 2. Input aur output

Input mein ek string `water` hoti hai jisme exactly 2*n Hydrogen aur n Oxygen hote hain. Output string form hoti hai barrier cross karne wale threads ke sequence se. Constraints hain: 3 * n == water.length, 1 <= n <= 20. Output mein har chunk of 3 letters mein 2 'H' aur 1 'O' hone chahiye.

## 3. Example walkthrough

Example 1: water = 'HOH'. Yaha 2 H aur 1 O hain. Koi bhi order jaise 'HHO', 'HOH', ya 'OHH' valid hai kyunki 3 ke group mein exactly 2 H aur 1 O bond hue hain.
Example 2: water = 'OOHHHH'. Total 4 H aur 2 O hain (n = 2). Dono groups of 3 (pehle 3 characters aur agle 3 characters) mein 2 H aur 1 O hone chahiye. Valid outputs: 'HHOHHO', 'HOHHHO', etc.

## 4. Brute-force approach

Naive approach mein hum spinlock ya busy-waiting use kar sakte hain counters ke saath (countH, countO) using simple `while(countH < 2)` condition variables ke bina. Par busy-waiting CPU burn karti hai, cache contention badhati hai, aur deadlock/starvation ka high risk hota hai, jo concurrency problems ke liye efficient ya acceptable nahi hai.

## 5. Optimized approach

Is problem ko semaphores ya condition variables + barrier se solve kiya ja sakta hai. Ek clean standard solution hai do Semaphores use karna: `semH` (initialized to 2) aur `semO` (initialized to 0) or cyclic barrier coordination. Better aur classic approach: `semH` initialized to 2 (2 hydrogen threads allow honge) aur `semO` initialized to 0. Lekin next molecule trigger karne ke liye, jab 2 H release ho jayein, wo O ko signal karein, aur jab O release ho jaye wo wapas 2 H ko signal kare. Yaa fir standard counting semaphores + barrier: H thread `semH.acquire()` karega, O thread `semO.acquire()` karega. Hydrogen method mein ek counter rakhenge; jab 2nd hydrogen pahunchta hai, wo oxygen ko allow karta hai (`semO.release()`), aur oxygen thread execute hone ke baad 2 hydrogen ko permit deta hai (`semH.release(2)`).

## 6. Dry run

Initial State: semH = 2, semO = 0.
1. H1 aata hai: semH.acquire() -> semH = 1. releaseHydrogen() call hota hai.
2. H2 aata hai: semH.acquire() -> semH = 0. releaseHydrogen() call hota hai. H2 detects it is 2nd H, releases semO -> semO = 1.
3. O1 aata hai: semO.acquire() -> semO = 0. releaseOxygen() call hota hai. O1 releases 2 permits to semH -> semH = 2.
Next molecule ke liye cycle cleanly repeat ho sakti hai.

## 7. Complexity

- **Time:** O(N) total time jaha N = 3*n threads hain. Har thread constant number of synchronization operations (acquire/release) perform karta hai, O(1) per thread.
- **Space:** O(1) auxiliary space kyunki sirf fixed synchronization primitives (semaphores / mutex / condition variables) use ho rahe hain.

## 8. Common mistakes

- Sirf semH(2) aur semO(1) rakhna bina cross-signaling ke; isse ek saath multiple O ya unbound H release ho sakte hain.
- Deadlock condition create karna jahan O wait kar raha ho H ka aur H wait kar raha ho O ka Bina proper signaling sequence ke.
- Counter variables (jaise hydrogen count) ko bina mutex/lock ke modify karna, causing data race.

## 9. Self-check quiz

- **Q:** semH semaphore ka initial permit count 2 kyun rakha jata hai?
  **A:** Kyunki water molecule (H2O) me shuruat me exactly do Hydrogen threads ko enter karne ki permission honi chahiye before waiting for reset.
- **Q:** Agar 3rd Hydrogen thread bina Oxygen ke release ho jaye toh kya hoga?
  **A:** Ratio violate ho jayega aur consecutive 3 characters me 2 H aur 1 O ki guarantee break ho jayegi.

## 10. Assumptions and caveats

Outputs permutation valid ho sakti hain jaise 'HOH', 'OHH', ya 'HHO'. Test evaluation grouping/validity check karta hai na ki exact string match.

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
