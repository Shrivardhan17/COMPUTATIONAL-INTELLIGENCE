    import heapq
    def __init__(self):
        self.adjacency_list = {}
        self.heuristics = {}

    def set_heuristics(self):
        print("\nEnter heuristics for each node (h(n)):")
        for node in self.adjacency_list:
            self.heuristics[node] = int(input(f"Heuristic for {node}: "))

    def a_star(self, start, goal):
        # priority_queue stores (f_cost, current_node, path, g_cost)
        frontier = [(self.heuristics[start], start, [start], 0)]
        explored = {} # stores node: min_g_cost

        print("\nIter\tFringe (f, node, g)\tExplored")
        count = 0

        while frontier:
            count += 1
            f, current, path, g = heapq.heappop(frontier)

            if current == goal:
                print(f"{count}\tGoal Found!\t\t{list(explored.keys())}")
                return path, g

            if current in explored and explored[current] <= g:
                continue
            
            explored[current] = g

            for neighbor, cost in self.adjacency_list[current]:
                new_g = g + cost
                new_f = new_g + self.heuristics.get(neighbor, 0)
                heapq.heappush(frontier, (new_f, neighbor, path + [neighbor], new_g))
            
            print(f"{count}\t{[(x[0], x[1], x[3]) for x in frontier]}\t{list(explored.keys())}")

        return None
