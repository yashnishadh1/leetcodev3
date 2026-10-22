#include <vector>
#include <unordered_set>

class Solution {
public:
    int duplicateNumbersXOR(std::vector<int>& nums) {
        std::unordered_set<int> seen;
        int ans = 0;
        for (int num : nums) {
            if (seen.count(num)) {
                ans ^= num;
            } else {
                seen.insert(num);
            }
        }
        return ans;
    }
};
