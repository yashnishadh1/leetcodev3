class Solution {
    public String smallestString(String s) {
        int n = s.length();
        String best = s;
        
        for (int k = 1; k <= n; k++) {
            // Reverse prefix of length k
            char[] arr1 = s.toCharArray();
            reverse(arr1, 0, k - 1);
            String cand1 = new String(arr1);
            if (cand1.compareTo(best) < 0) {
                best = cand1;
            }
            
            // Reverse suffix of length k
            char[] arr2 = s.toCharArray();
            reverse(arr2, n - k, n - 1);
            String cand2 = new String(arr2);
            if (cand2.compareTo(best) < 0) {
                best = cand2;
            }
        }
        
        return best;
    }
    
    private void reverse(char[] arr, int left, int right) {
        while (left < right) {
            char temp = arr[left];
            arr[left] = arr[right];
            arr[right] = temp;
            left++;
            right--;
        }
    }
}
