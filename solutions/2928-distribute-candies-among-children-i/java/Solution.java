class Solution {
    public int distributeCandies(int n, int limit) {
        int ans = 0;
        int maxFirst = Math.min(n, limit);
        for (int i = 0; i <= maxFirst; i++) {
            int maxSecond = Math.min(n - i, limit);
            for (int j = 0; j <= maxSecond; j++) {
                int k = n - i - j;
                if (k >= 0 && k <= limit) {
                    ans++;
                }
            }
        }
        return ans;
    }
}
