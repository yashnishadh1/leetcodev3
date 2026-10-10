class Solution:
    def hasAllCodes(self, s: str, k: int) -> bool:
        need = 1 << k
        if len(s) < need + k - 1:
            return False
        
        seen = [False] * need
        count = 0
        val = 0
        mask = need - 1
        
        for i in range(len(s)):
            val = ((val << 1) & mask) | (int(s[i]))
            if i >= k - 1:
                if not seen[val]:
                    seen[val] = True
                    count += 1
                    if count == need:
                        return True
                        
        return False
