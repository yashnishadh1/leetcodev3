import bisect

class CountIntervals:

    def __init__(self):
        self.intervals = []  # sorted list of [left, right]
        self.total_count = 0

    def add(self, left: int, right: int) -> None:
        # Find the first interval that could potentially overlap
        # Overlapping condition: l <= right and r >= left
        idx = bisect.bisect_left(self.intervals, [left, 0])
        if idx > 0 and self.intervals[idx - 1][1] >= left:
            idx -= 1
        
        # Merge all overlapping intervals
        merged_l = left
        merged_r = right
        remove_count = 0
        
        i = idx
        while i < len(self.intervals) and self.intervals[i][0] <= right:
            merged_l = min(merged_l, self.intervals[i][0])
            merged_r = max(merged_r, self.intervals[i][1])
            self.total_count -= (self.intervals[i][1] - self.intervals[i][0] + 1)
            remove_count += 1
            i += 1
        
        # Replace removed intervals with the merged interval
        self.intervals[idx : idx + remove_count] = [[merged_l, merged_r]]
        self.total_count += (merged_r - merged_l + 1)

    def count(self) -> int:
        return self.total_count

class Solution(CountIntervals):
    pass
