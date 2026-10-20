class Solution:
    def duplicateNumbersXOR(self, nums: list[int]) -> int:
        seen = set()
        ans = 0
        for num in nums:
            if num in seen:
                ans ^= num
            else:
                seen.add(num)
        return ans
