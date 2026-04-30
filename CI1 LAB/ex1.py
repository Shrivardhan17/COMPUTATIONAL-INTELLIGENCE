from collections import deque

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    # ---------- CREATE GRAPH ----------
    def create_graph(self):
        n = int(input("Enter number of nodes: "))
        e = int(input("Enter number of edges: "))

        print("Enter node labels:")
        for _ in range(n):
            self.add_node(input().strip())

        print("Enter edges (u v):")
        for _ in range(e):
            u, v = input().split()
            self.add_edge(u, v)

        print("Graph created successfully!\n")

    # ---------- ADD NODE ----------
    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
        else:
            print(f"Node '{node}' already exists")

    # ---------- ADD EDGE ----------
    def add_edge(self, u, v, cost=1):
        if u not in self.adjacency_list or v not in self.adjacency_list:
            print("Invalid nodes")
            return
        for neigh, _ in self.adjacency_list[u]:
            if neigh == v:
                print(f"Error: Edge {u}-{v} already exists")
                return
        if [v, cost] not in self.adjacency_list[u]:
            self.adjacency_list[u].append([v, cost])
        if [u, cost] not in self.adjacency_list[v]:
            self.adjacency_list[v].append([u, cost])
        print(f"Edge {u}-{v} added successfully")

    # ===== GET EDGE COSTS FOR UCS =====
    def get_costs_for_ucs(self):
        print("\nEnter edge costs for UCS:")
        visited = set()

        for u in self.adjacency_list:
            for edge in self.adjacency_list[u]:
                v = edge[0]

            # avoid asking twice for undirected edge
                if (u, v) in visited or (v, u) in visited:
                    continue

                cost = int(input(f"Cost for edge {u} - {v}: "))

            # update both directions
                for e in self.adjacency_list[u]:
                    if e[0] == v:
                        e[1] = cost
                for e in self.adjacency_list[v]:
                    if e[0] == u:
                        e[1] = cost

                visited.add((u, v))

    # ---------- DELETE EDGE ----------
    def delete_edge(self, u, v):
        if u not in self.adjacency_list or v not in self.adjacency_list:
            print("Error: One or both nodes do not exist")
            return


        edge_exists = False
        for neigh, _ in self.adjacency_list[u]:
            if neigh == v:
                edge_exists = True
                break

        if not edge_exists:
            print(f"Error: Edge {u}-{v} does not exist")
            return

    # Delete edge (undirected)
        self.adjacency_list[u] = [x for x in self.adjacency_list[u] if x[0] != v]
        self.adjacency_list[v] = [x for x in self.adjacency_list[v] if x[0] != u]

        print(f"Edge {u}-{v} deleted successfully")


    # ---------- DELETE NODE ----------
    def delete_node(self, node):
        if node not in self.adjacency_list:
            print(f"Error: Node '{node}' does not exist")
            return

    # Delete all edges connected to this node
        for neigh, _ in self.adjacency_list[node][:]:   # copy to avoid runtime error
            self.delete_edge(node, neigh)

        del self.adjacency_list[node]
        print(f"Node '{node}' deleted successfully")


    # ---------- DISPLAY ----------
    def display_graph(self):
        for node in sorted(self.adjacency_list):
            print(f"{node} -> {self.adjacency_list[node]}")

    def display_adjacency(self, node):
        print(f"{node} -> {self.adjacency_list.get(node, 'Not Found')}")

    # ================= BFS =================
    def bfs(self, start, goal):
        if not self.adjacency_list:
            print("Error: Graph is empty")
            return None
        if start not in self.adjacency_list:
            print(f"Error: Start Node '{start}'not found!")
            return None
        if goal not in self.adjacency_list:
            print(f"Error:Goal nod '{goal}'not found!")
            return None
        if start==goal:
            return start
        frontier = deque([start])
        explored = []
        count=1
        print("Iter_count\tfringe\texplored_set")
        print(f"{count}\t\t{frontier}\t\t{explored}")
        while frontier:
            count=count+1
            current = frontier.popleft()
            explored.append(current)

            if current == goal:
                print(f"{count}\t\t{frontier}\t\t{explored}")
                return explored

            for neigh, _ in self.adjacency_list[current]:
                if neigh not in explored and neigh not in frontier:
                    frontier.append(neigh)
                    print(f"{count}\t\t{frontier}\t\t{explored}")
        return None

    # ========== BFS REVERSE ==========
    def bfs_reverse_add_order(self, start, goal):
        if not self.adjacency_list:
            print("Error: Graph is empty")
            return None
        if start not in self.adjacency_list:
            print(f"Error: Start Node '{start}'not found!")
            return None
        if goal not in self.adjacency_list:
            print(f"Error:Goal nod '{goal}'not found!")
            return None
        if start==goal:
            return start
        frontier = deque([start])
        explored = []
        count=1
        print("Iter_count\tfringe\texplored_set")
        print(f"{count}\t\t{frontier}\t\t{explored}")
        while frontier:
            current = frontier.popleft()
            explored.append(current)

            if current == goal:
                print(f"{count}\t\t{frontier}\t\t{explored}")
                return explored

            for neigh, _ in reversed(self.adjacency_list[current]):
                if neigh not in explored and neigh not in frontier:
                    frontier.append(neigh)
                    print(f"{count}\t\t{frontier}\t\t{explored}")
        return None

    # ================= DFS using DEQUE =================
    def dfs_deque(self, start, goal):
        if not self.adjacency_list:
            print("Error: Graph is empty")
            return None
        if start not in self.adjacency_list:
            print(f"Error: Start Node '{start}'not found!")
            return None
        if goal not in self.adjacency_list:
            print(f"Error:Goal nod '{goal}'not found!")
            return None
        frontier = deque([start])   # DFS fringe
        explored = []
        count=1
        print("Iter_count\tfringe\texplored_set")
        print(f"{count}\t\t{frontier}\t\t{explored}")

        while frontier:
            count+=1
            current = frontier.pop()

            if current not in explored:
                explored.append(current)

                if current == goal:
                    print(f"{count}\t\t{frontier}\t\t{explored}")
                    return explored

                # normal order
                for neigh, _ in reversed(self.adjacency_list[current]):
                    if neigh not in explored:
                        frontier.append(neigh)
                        print(f"{count}\t\t{frontier}\t\t{explored}")
        return None

    # ========== DFS REVERSE using DEQUE ==========
    def dfs_deque_reversed(self, start, goal):
        if not self.adjacency_list:
            print("Error: Graph is empty")
            return None
        if start not in self.adjacency_list:
            print(f"Error: Start Node '{start}'not found!")
            return None
        if goal not in self.adjacency_list:
            print(f"Error:Goal nod '{goal}'not found!")
            return None
        frontier = deque([start])
        explored = []
        count=1
        print("Iter_count\tfringe\texplored_set")
        print(f"{count}\t\t{frontier}\t\t{explored}")
        while frontier:
            count+=1
            current = frontier.pop()

            if current not in explored:
                explored.append(current)

                if current == goal:
                    print(f"{count}\t\t{frontier}\t\t{explored}")
                    return explored

                # reverse order
                for neigh, _ in self.adjacency_list[current]:
                    if neigh not in explored:
                        frontier.append(neigh)
                        print(f"{count}\t\t{frontier}\t\t{explored}")
        return None
    # ================= UCS (Queue + Sorting) =================
    # ========== UCS (Sort by Cost & Path) ==========
    def ucs_sort_cost_path(self, start, goal):
        if not self.adjacency_list:
            print("Error: Graph is empty")
            return None
        if start not in self.adjacency_list:
            print(f"Error: Start Node '{start}'not found!")
            return None
        if goal not in self.adjacency_list:
            print(f"Error:Goal nod '{goal}'not found!")
            return None
        frontier = [(0, [start])]
        explored = {}   # node -> minimum cost
        count = 0

        print("Iter\tFringe\t\t\tExplored")


        while frontier:
        # Sort by cost, then path
            frontier.sort(key=lambda x: (x[0], x[1]))
            count += 1
            print(f"{count}\t{frontier}\n\t{explored}")

            cost, path = frontier.pop(0)
            current = path[-1]

        # If explored with lower cost, skip
            if current in explored and explored[current] <= cost:
                continue

            explored[current] = cost

        # Goal check
            if current == goal:
                count+=1
                print(f"{count}\t\t{frontier}\n\t{explored}")
                return path, cost

        # Expand neighbors
            for neigh, weight in self.adjacency_list[current]:
                if neigh in path:   # avoid cycles
                    continue

                new_cost = cost + weight
                new_path = path + [neigh]

                replaced = False

            # REMOVE higher-cost path if same node exists
                for i, (fcost, fpath) in enumerate(frontier):
                    if fpath[-1] == neigh:
                        if new_cost < fcost:
                            frontier[i] = (new_cost, new_path)  # replace
                        replaced = True
                        break

            # If node not in frontier, add it
                if not replaced:
                    frontier.append((new_cost, new_path))

        return None


# ================= MAIN =================
if __name__ == "__main__":
    g = Graph()
    g.create_graph()
    print("\n=== Graph Menu ===")
    print("1. Add Node")
    print("2. Add Edge")
    print("3. Delete Node")
    print("4. Delete Edge")
    print("5. Display Graph")
    print("6. Display Adjacency")
    print("7. BFS")
    print("8. BFS Reverse Order")
    print("9. DFS (Deque)")
    print("10. DFS Reverse (Deque)")
    print("11. UCS (Queue + Sorting)")
    print("12. Exit")

    while True:

        ch = input("Enter choice: ")

        if ch == "1":
            g.add_node(input("Node: "))
        elif ch == "2":
            g.add_edge(input("U: "), input("V: "))
        elif ch == "3":
            g.delete_node(input("Node: "))
        elif ch == "4":
            g.delete_edge(input("U: "), input("V: "))
        elif ch == "5":
            g.display_graph()
        elif ch == "6":
            g.display_adjacency(input("Node: "))
        elif ch == "7":
            print("BFS:", g.bfs(input("Start: "), input("Goal: ")))
        elif ch == "8":
            print("BFS Reverse:", g.bfs_reverse_add_order(input("Start: "), input("Goal: ")))
        elif ch == "9":
            print("DFS:", g.dfs_deque(input("Start: "), input("Goal: ")))
        elif ch == "10":
            print("DFS Reverse:", g.dfs_deque_reversed(input("Start: "), input("Goal: ")))
        elif ch == "11":
            g.get_costs_for_ucs()
            result = g.ucs_sort_cost_path(input("Start: "), input("Goal: "))
            if result:
                path, cost = result
                print("UCS Path:", path)
                print("Total Cost:", cost)
            else:
                print("No path found")
        elif ch == "12":
            print("Exiting...")
            break
        else:
            print("Invalid choice")