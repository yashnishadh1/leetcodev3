#include <vector>

class Solution {
public:
    int minReorder(int n, std::vector<std::vector<int>>& connections) {
        std::vector<std::vector<std::pair<int, int>>> adj(n);
        for (const auto& edge : connections) {
            int u = edge[0];
            int v = edge[1];
            adj[u].push_back({v, 1}); // needs reorder if traversed
            adj[v].push_back({u, 0}); // already incoming
        }
        
        int flips = 0;
        std::vector<bool> visited(n, false);
        std::vector<int> stack = {0};
        visited[0] = true;
        
        while (!stack.empty()) {
            int curr = stack.back();
            stack.pop_back();
            
            for (const auto& [neighbor, cost] : adj[curr]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    flips += cost;
                    stack.push_back(neighbor);
                }
            }
        }
        
        return flips;
    }
};
