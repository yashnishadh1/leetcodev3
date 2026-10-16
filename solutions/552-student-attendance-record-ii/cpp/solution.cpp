class Solution {
public:
    int checkRecord(int n) {
        const int MOD = 1000000007;
        
        // dp[a][l] -> a in {0, 1}, l in {0, 1, 2}
        vector<vector<long long>> dp(2, vector<long long>(3, 0));
        dp[0][0] = 1;
        
        for (int i = 0; i < n; ++i) {
            vector<vector<long long>> next_dp(2, vector<long long>(3, 0));
            
            for (int a = 0; a < 2; ++a) {
                for (int l = 0; l < 3; ++l) {
                    long long count = dp[a][l];
                    if (count == 0) continue;
                    
                    // Append 'P'
                    next_dp[a][0] = (next_dp[a][0] + count) % MOD;
                    
                    // Append 'A'
                    if (a == 0) {
                        next_dp[1][0] = (next_dp[1][0] + count) % MOD;
                    }
                    
                    // Append 'L'
                    if (l < 2) {
                        next_dp[a][l + 1] = (next_dp[a][l + 1] + count) % MOD;
                    }
                }
            }
            dp = std::move(next_dp);
        }
        
        long long total = 0;
        for (int a = 0; a < 2; ++a) {
            for (int l = 0; l < 3; ++l) {
                total = (total + dp[a][l]) % MOD;
            }
        }
        
        return total;
    }
};
