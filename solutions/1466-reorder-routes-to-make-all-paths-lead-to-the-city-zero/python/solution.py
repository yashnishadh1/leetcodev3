class Solution:
    def minReorder(self, n: int, connections: list[list[int]]) -> int:
        adj = [[] for _ in range(n)]
        for u, v in connections:
            adj[u].append((v, 1))  # original direction: needs flip if traversed
            adj[v].append((u, 0))  # reverse direction: already correct
        
        flips = 0
        visited = [False] * n
        visited[0] = True
        stack = [0]
        
        while stack:
            curr = stack.pop()
            for neighbor, cost in adj[curr]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    flips += cost
                    stack.append(neighbor)
                    
        return flips
