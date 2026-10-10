class Solution {
public:
    bool hasAllCodes(string s, int k) {
        int need = 1 << k;
        if (s.length() < (size_t)(need + k - 1)) {
            return false;
        }
        
        vector<bool> seen(need, false);
        int count = 0;
        int val = 0;
        int mask = need - 1;
        
        for (int i = 0; i < s.length(); i++) {
            val = ((val << 1) & mask) | (s[i] - '0');
            if (i >= k - 1) {
                if (!seen[val]) {
                    seen[val] = true;
                    count++;
                    if (count == need) {
                        return true;
                    }
                }
            }
        }
        
        return false;
    }
};
