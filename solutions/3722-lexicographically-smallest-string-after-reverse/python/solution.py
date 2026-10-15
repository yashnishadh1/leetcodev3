class Solution:
    def smallestString(self, s: str) -> str:
        n = len(s)
        best = s
        
        for k in range(1, n + 1):
            # Reverse prefix of length k
            cand1 = s[:k][::-1] + s[k:]
            if cand1 < best:
                best = cand1
            
            # Reverse suffix of length k
            cand2 = s[:n - k] + s[n - k:][::-1]
            if cand2 < best:
                best = cand2
                
        return best
