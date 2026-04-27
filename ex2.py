import heapq

# -------------------------------
# GRAPH (Weighted)
# -------------------------------
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 2), ('E', 5)],
    'C': [('F', 1)],
    'D': [],
    'E': [('F', 1)],
    'F': []
}

# -------------------------------
# HEURISTIC VALUES (h(n))
# -------------------------------
heuristic = {
    'A': 5,
    'B': 3,
    'C': 2,
    'D': 6,
    'E': 1,
    'F': 0
}

# -------------------------------
# GREEDY BEST-FIRST SEARCH
# -------------------------------
def greedy_bfs(graph, start, goal, h):
    visited = set()
    pq = [(h[start], start)]  # (heuristic, node)

    print("\nGreedy Best-First Search:")

    while pq:
        h_val, node = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)
        print(node, end=" ")

        if node == goal:
            print("\nGoal reached!")
            return

        for neighbor, _ in graph[node]:
            if neighbor not in visited:
                heapq.heappush(pq, (h[neighbor], neighbor))


# -------------------------------
# A* SEARCH
# -------------------------------
def a_star(graph, start, goal, h):
    pq = [(0 + h[start], 0, start)]  # (f, g, node)
    visited = set()

    print("\nA* Search:")

    while pq:
        f, g, node = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)
        print(f"{node}(f={f})", end=" ")

        if node == goal:
            print("\nGoal reached! Cost =", g)
            return g

        for neighbor, cost in graph[node]:
            if neighbor not in visited:
                new_g = g + cost
                new_f = new_g + h[neighbor]
                heapq.heappush(pq, (new_f, new_g, neighbor))


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    start = 'A'
    goal = 'F'

    greedy_bfs(graph, start, goal, heuristic)
    a_star(graph, start, goal, heuristic)