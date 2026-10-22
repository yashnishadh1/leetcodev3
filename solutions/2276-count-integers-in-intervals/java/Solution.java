import java.util.TreeMap;
import java.util.Map;

class CountIntervals {
    private TreeMap<Integer, Integer> intervals;
    private int totalCount;

    public CountIntervals() {
        intervals = new TreeMap<>();
        totalCount = 0;
    }
    
    public void add(int left, int right) {
        // Find overlapping intervals
        // An interval [l, r] overlaps if l <= right && r >= left
        Map.Entry<Integer, Integer> entry = intervals.floorEntry(right);
        while (entry != null && entry.getValue() >= left) {
            int l = entry.getKey();
            int r = entry.getValue();
            left = Math.min(left, l);
            right = Math.max(right, r);
            totalCount -= (r - l + 1);
            intervals.remove(l);
            entry = intervals.floorEntry(right);
        }
        
        intervals.put(left, right);
        totalCount += (right - left + 1);
    }
    
    public int count() {
        return totalCount;
    }
}

class Solution extends CountIntervals {
    public Solution() {
        super();
    }
}
