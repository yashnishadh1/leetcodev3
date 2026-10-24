class Solution:
    def checkRecord(self, n: int) -> int:
        MOD = 1_000_000_007
        
        # dp[a][l] -> a in {0, 1}, l in {0, 1, 2}
        dp = [[0] * 3 for _ in range(2)]
        dp[0][0] = 1
        
        for _ in range(n):
            next_dp = [[0] * 3 for _ in range(2)]
            
            for a in range(2):
                for l in range(3):
                    count = dp[a][l]
                    if count == 0:
                        continue
                    
                    # 1. Append 'P': resets l to 0, a remains same
                    next_dp[a][0] = (next_dp[a][0] + count) % MOD
                    
                    # 2. Append 'A': resets l to 0, a increments from 0 to 1
                    if a == 0:
                        next_dp[1][0] = (next_dp[1][0] + count) % MOD
                    
                    # 3. Append 'L': l increments, a remains same
                    if l < 2:
                        next_dp[a][l + 1] = (next_dp[a][l + 1] + count) % MOD
            
            dp = next_dp
            
        ans = 0
        for a in range(2):
            for l in range(3):
                ans = (ans + dp[a][l]) % MOD
                
        return ans
