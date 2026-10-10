import java.util.*;

class Solution {
    public int minReorder(int n, int[][] connections) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList<>());
        }
        
        for (int[] edge : connections) {
            int u = edge[0];
            int v = edge[1];
            adj.get(u).add(new int[]{v, 1}); // needs flip
            adj.get(v).add(new int[]{u, 0}); // already towards 0
        }
        
        int flips = 0;
        boolean[] visited = new boolean[n];
        Deque<Integer> stack = new ArrayDeque<>();
        
        stack.push(0);
        visited[0] = true;
        
        while (!stack.isEmpty()) {
            int curr = stack.pop();
            for (int[] next : adj.get(curr)) {
                int neighbor = next[0];
                int cost = next[1];
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    flips += cost;
                    stack.push(neighbor);
                }
            }
        }
        
        return flips;
    }
}
