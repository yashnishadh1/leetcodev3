#include <map>
#include <algorithm>

class CountIntervals {
private:
    std::map<int, int> intervals; // key: left, value: right
    int total_count;

public:
    CountIntervals() : total_count(0) {}
    
    void add(int left, int right) {
        // Find first interval with l > right
        auto it = intervals.upper_bound(right);
        
        // Walk backwards to find all intervals that overlap with [left, right]
        if (it != intervals.begin()) {
            --it;
            while (it->second >= left) {
                left = std::min(left, it->first);
                right = std::max(right, it->second);
                total_count -= (it->second - it->first + 1);
                it = intervals.erase(it);
                if (it == intervals.begin()) break;
                --it;
            }
        }
        
        intervals[left] = right;
        total_count += (right - left + 1);
    }
    
    int count() {
        return total_count;
    }
};

class Solution : public CountIntervals {
public:
    Solution() : CountIntervals() {}
};
