class Solution {
public:
    string smallestString(string s) {
        int n = s.length();
        string best = s;
        
        for (int k = 1; k <= n; ++k) {
            // Reverse prefix of length k
            string s1 = s;
            reverse(s1.begin(), s1.begin() + k);
            if (s1 < best) {
                best = s1;
            }
            
            // Reverse suffix of length k
            string s2 = s;
            reverse(s2.end() - k, s2.end());
            if (s2 < best) {
                best = s2;
            }
        }
        
        return best;
    }
};
