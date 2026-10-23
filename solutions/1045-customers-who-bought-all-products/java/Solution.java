import java.util.*;

class Solution {
    public List<Integer> findCustomers(int[][] customer, int[] product) {
        Set<Integer> allProducts = new HashSet<>();
        for (int p : product) {
            allProducts.add(p);
        }
        Map<Integer, Set<Integer>> customerProducts = new HashMap<>();
        for (int[] c : customer) {
            customerProducts.computeIfAbsent(c[0], k -> new HashSet<>()).add(c[1]);
        }
        List<Integer> result = new ArrayList<>();
        for (Map.Entry<Integer, Set<Integer>> entry : customerProducts.entrySet()) {
            if (entry.getValue().size() == allProducts.size()) {
                result.add(entry.getKey());
            }
        }
        return result;
    }
}
