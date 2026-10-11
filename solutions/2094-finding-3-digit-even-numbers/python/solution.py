class Solution:
    def findEvenNumbers(self, digits: list[int]) -> list[int]:
        from collections import Counter
        
        freq = Counter(digits)
        result = []
        
        for num in range(100, 1000, 2):
            d1 = num // 100
            d2 = (num // 10) % 10
            d3 = num % 10
            
            needed = Counter([d1, d2, d3])
            
            if all(freq[d] >= needed[d] for d in needed):
                result.append(num)
                
        return result
