# 2726. Calculator with Method Chaining

- **Difficulty:** Easy
- **Problem:** https://leetcode.com/problems/calculator-with-method-chaining/
- **Topics:** Not provided
- **Generated:** 2026-10-22

## 1. Problem ko simple Hinglish mein samjho

Hame ek `Calculator` class design karni hai jo method chaining support kare. Constructor me ek initial value milegi. Isme `add`, `subtract`, `multiply`, `divide`, `power`, aur `getResult` methods honge. Har arithmetic operation current result ko update karega aur updated Calculator instance (method chaining ke liye `this`) return karega, jabki `divide` me zero aane par error throw karna hai. Last me `getResult()` numerical answer return karega.

## 2. Input aur output

Input: actions array jisme method names honge (pehla 'Calculator' aur aakhri 'getResult'), aur values array jisme respective method arguments honge.
Output: Final numerical result ya fir error string ("Division by zero is not allowed") agar divide by zero encounter hota hai.
Constraints: actions.length 2 se 2 * 10^4 tak, values.length valid numbers, solutions within 10^-5 of actual result are accepted.

## 3. Example walkthrough

Example 1:
- Calculator(10): result = 10
- add(5): result = 10 + 5 = 15, returns calculator
- subtract(7): result = 15 - 7 = 8, returns calculator
- getResult(): returns 8.

Example 2:
- Calculator(2): result = 2
- multiply(5): result = 2 * 5 = 10
- power(2): result = 10^2 = 100
- getResult(): returns 100.

Example 3:
- Calculator(20): result = 20
- divide(0): value == 0 check fail hoti hai, throw error 'Division by zero is not allowed'.

## 4. Brute-force approach

Yeh problem design category ka hai, koi complex algorithmic brute force nahi hai. Simple implementation me har method instance variable ko modify karke calculator object ya `this` return karta hai. Agar chaining support nahi karenge toh functions chain nahi ho payenge.

## 5. Optimized approach

OOP pattern me method chaining implement karne ke liye har modifying method se current object ka reference (`self` Python me, `this` Java aur C++ me) return karte hain. 
State ko store karne ke liye ek single variable `result` (floating point/double type) maintain karenge. `divide` me pehle `value === 0` check karenge aur exception throw karenge. `power` ke liye language ka built-in power function ya operator use karenge.

## 6. Dry run

Step-by-step dry run on Example 2: actions = ["Calculator", "multiply", "power", "getResult"], values = [2, 5, 2]
1. init(2) -> this.result = 2
2. multiply(5) -> this.result = 2 * 5 = 10, return this
3. power(2) -> this.result = 10^2 = 100, return this
4. getResult() -> return this.result = 100

## 7. Complexity

- **Time:** Har method call constant time O(1) leti hai. Agar total N actions hain, toh total time complexity O(N) hogi.
- **Space:** O(1) auxiliary space kyunki hum sirf ek numeric variable store kar rahe hain calculator state ke liye.

## 8. Common mistakes

- Method chaining bhool jana ya methods se result return kar dena instead of returning `this` / `self`.
- Divide by zero check ko ignore karna ya simple return kar dena instead of throwing an error/exception.
- Error message exact na match karna: problem me explicitly bola hai "Division by zero is not allowed".

## 9. Self-check quiz

- **Q:** Method chaining achieve karne ke liye method ko kya return karna padta hai?
  **A:** Current instance ka reference (Python me self, C++ me *this, Java me this).
- **Q:** Agar divide(0) call ho jaye toh expected behavior kya hai?
  **A:** Error/exception throw karna with message 'Division by zero is not allowed'.

## 10. Assumptions and caveats

Problem JavaScript/TypeScript category me original thi LeetCode par, par standard class design principles sabhi OOP languages (Python, Java, C++) par directly apply hote hain. Java/C++ me method chaining ke liye return type `Calculator` / `Calculator&` banaya gaya hai.

## Validation

Static checks only. No code was executed and no LeetCode judge result was obtained.
