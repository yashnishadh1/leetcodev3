import math

class Solution:
    def commonFactors(self, a: int, b: int) -> int:
        g = math.gcd(a, b)
        count = 0
        i = 1
        while i * i <= g:
            if g % i == 0:
                count += 1
                if i * i != g:
                    count += 1
            i += 1
        return count
