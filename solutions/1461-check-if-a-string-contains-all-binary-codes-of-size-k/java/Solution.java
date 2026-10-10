class Solution {
    public boolean hasAllCodes(String s, int k) {
        int need = 1 << k;
        if (s.length() < need + k - 1) {
            return false;
        }
        
        boolean[] seen = new boolean[need];
        int count = 0;
        int val = 0;
        int mask = need - 1;
        
        for (int i = 0; i < s.length(); i++) {
            val = ((val << 1) & mask) | (s.charAt(i) - '0');
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
}
