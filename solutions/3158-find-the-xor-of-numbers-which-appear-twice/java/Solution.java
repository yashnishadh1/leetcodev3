import java.util.HashSet;
import java.util.Set;

class Solution {
    public int duplicateNumbersXOR(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        int ans = 0;
        for (int num : nums) {
            if (seen.contains(num)) {
                ans ^= num;
            } else {
                seen.add(num);
            }
        }
        return ans;
    }
}
