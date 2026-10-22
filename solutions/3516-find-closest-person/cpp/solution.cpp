#include <cstdlib>

class Solution {
public:
    int findClosestPerson(int x, int y, int z) {
        int dist1 = std::abs(x - z);
        int dist2 = std::abs(y - z);
        
        if (dist1 < dist2) {
            return 1;
        } else if (dist2 < dist1) {
            return 2;
        } else {
            return 0;
        }
    }
};
