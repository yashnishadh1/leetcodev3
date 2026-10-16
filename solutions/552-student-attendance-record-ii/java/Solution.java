class Solution {
    public int checkRecord(int n) {
        int MOD = 1_000_000_007;
        
        // dp[a][l] -> a in {0, 1}, l in {0, 1, 2}
        long[][] dp = new long[2][3];
        dp[0][0] = 1;
        
        for (int i = 0; i < n; i++) {
            long[][] nextDp = new long[2][3];
            
            for (int a = 0; a < 2; a++) {
                for (int l = 0; l < 3; l++) {
                    long count = dp[a][l];
                    if (count == 0) continue;
                    
                    // Append 'P'
                    nextDp[a][0] = (nextDp[a][0] + count) % MOD;
                    
                    // Append 'A'
                    if (a == 0) {
                        nextDp[1][0] = (nextDp[1][0] + count) % MOD;
                    }
                    
                    // Append 'L'
                    if (l < 2) {
                        nextDp[a][l + 1] = (nextDp[a][l + 1] + count) % MOD;
                    }
                }
            }
            dp = nextDp;
        }
        
        long total = 0;
        for (int a = 0; a < 2; a++) {
            for (int l = 0; l < 3; l++) {
                total = (total + dp[a][l]) % MOD;
            }
        }
        
        return (int) total;
    }
}
