import tkinter as tk
from tkinter import simpledialog
import heapq
import time

# ---------------- A* ALGORITHM ----------------
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    closed_set = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        # If already processed, skip
        if current in closed_set:
            continue

        # Goal reached
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        closed_set.add(current)

        # 4-direction movement
        directions = [(0,1), (1,0), (0,-1), (-1,0)]

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            # Check boundaries
            if not (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols):
                continue

            # Skip obstacle
            if grid[neighbor[0]][neighbor[1]] == 0:
                continue

            # Calculate cost
            tentative_g = g_score[current] + grid[neighbor[0]][neighbor[1]]

            # If better path found
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return None

# ---------------- GUI PART ----------------
root = tk.Tk()
root.title("A* Pathfinding using Tkinter")

rows = int(simpledialog.askstring("Input", "Enter number of rows:"))
cols = int(simpledialog.askstring("Input", "Enter number of columns:"))

grid = []
for i in range(rows):
    row_input = simpledialog.askstring("Grid Input", f"Enter row {i} values (space separated):")
    row = list(map(int, row_input.split()))
    grid.append(row)

start_input = simpledialog.askstring("Start", "Enter start position (row col):")
start = tuple(map(int, start_input.split()))

goal_input = simpledialog.askstring("Goal", "Enter goal position (row col):")
goal = tuple(map(int, goal_input.split()))

cell_size = 100
canvas = tk.Canvas(root, width=cols*cell_size, height=rows*cell_size)
canvas.pack()

rectangles = {}

def draw_grid():
    for i in range(rows):
        for j in range(cols):
            x1 = j * cell_size
            y1 = i * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            color = "gray"
            if grid[i][j] == (x1%2==0):
                color = "black"

            rect = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
            canvas.create_text(
                x1 + cell_size//2,
                y1 + cell_size//2,
                text=str(grid[i][j]),
                font=("itallic", int(cell_size/3), "underline")
            )

            rectangles[(i,j)] = rect

    canvas.itemconfig(rectangles[start], fill="pink")
    canvas.itemconfig(rectangles[goal], fill="green")

def animate_path(path):
    for node in path:
        if node != start and node != goal:
            canvas.itemconfig(rectangles[node], fill="lightblue")
            root.update()
            time.sleep(2)

draw_grid()

path = astar(grid, start, goal)

if path:
    animate_path(path)
else:
    print("No Path Found")

root.mainloop()
