# Wumpus World Implementation (Simple Version)

SIZE = 4

# -------------------------------
# WORLD SETUP
# -------------------------------
world = [['' for _ in range(SIZE)] for _ in range(SIZE)]

# Place elements
world[1][2] = 'P'   # Pit
world[2][2] = 'W'   # Wumpus
world[3][3] = 'G'   # Gold

# -------------------------------
# FUNCTION TO GET PERCEPTS
# -------------------------------
def get_percepts(x, y):
    percepts = []

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE:
            if world[nx][ny] == 'P':
                percepts.append("Breeze")
            if world[nx][ny] == 'W':
                percepts.append("Stench")

    if world[x][y] == 'G':
        percepts.append("Glitter")

    return percepts

# -------------------------------
# SIMPLE AGENT
# -------------------------------
def agent():
    x, y = 0, 0
    visited = set()

    print("Agent starting at (0,0)\n")

    while True:
        print(f"Agent at ({x},{y})")

        if world[x][y] == 'P':
            print("Fell into Pit! Game Over ❌")
            break

        if world[x][y] == 'W':
            print("Eaten by Wumpus! Game Over ❌")
            break

        if world[x][y] == 'G':
            print("Gold found! You Win 🏆")
            break

        percepts = get_percepts(x, y)
        print("Percepts:", percepts)

        visited.add((x, y))

        # Simple movement (right → down → left → up)
        moves = [(0,1),(1,0),(0,-1),(-1,0)]

        moved = False
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < SIZE and 0 <= ny < SIZE and (nx, ny) not in visited:
                x, y = nx, ny
                moved = True
                break

        if not moved:
            print("No safe moves left! Stopping.")
            break

        print()

# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    agent()