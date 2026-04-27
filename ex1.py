from collections import deque
import heapq

# -------------------------------
# GRAPH DEFINITIONS
# -------------------------------

# Unweighted graph (for BFS & DFS)
graph_unweighted = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

# Weighted graph (for UCS)
graph_weighted = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 2), ('E', 5)],
    'C': [('F', 1)],
    'D': [],
    'E': [('F', 1)],
    'F': []
}

# -------------------------------
# BFS FUNCTION
# -------------------------------
def bfs(graph, start):
    visited = set()
    queue = deque([start])

    visited.add(start)

    print("\nBFS Traversal:")
    while queue:
        node = queue.popleft()
        print(node, end=" ")

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# -------------------------------
# DFS FUNCTION
# -------------------------------
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()

    visited.add(node)
    print(node, end=" ")

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

# -------------------------------
# UCS FUNCTION
# -------------------------------
def ucs(graph, start, goal):
    visited = set()
    pq = [(0, start)]  # (cost, node)

    print("\nUCS Traversal:")
    while pq:
        cost, node = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)
        print(f"{node}(cost={cost})", end=" ")

        if node == goal:
            print("\nGoal reached!")
            return cost

        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                heapq.heappush(pq, (cost + weight, neighbor))

    return None

# -------------------------------
# MAIN EXECUTION
# -------------------------------
if __name__ == "__main__":
    start_node = 'A'
    goal_node = 'F'

    # BFS
    bfs(graph_unweighted, start_node)

    # DFS
    print("\nDFS Traversal:")
    dfs(graph_unweighted, start_node)

    # UCS
    ucs(graph_weighted, start_node, goal_node)