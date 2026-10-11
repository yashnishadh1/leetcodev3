#include <vector>

class Solution {
public:
    std::vector<int> findEvenNumbers(std::vector<int>& digits) {
        std::vector<int> count(10, 0);
        for (int d : digits) {
            count[d]++;
        }
        
        std::vector<int> result;
        for (int num = 100; num < 1000; num += 2) {
            int d1 = num / 100;
            int d2 = (num / 10) % 10;
            int d3 = num % 10;
            
            count[d1]--;
            count[d2]--;
            count[d3]--;
            
            if (count[d1] >= 0 && count[d2] >= 0 && count[d3] >= 0) {
                result.push_back(num);
            }
            
            count[d1]++;
            count[d2]++;
            count[d3]++;
        }
        
        return result;
    }
};
