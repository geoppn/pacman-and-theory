import heapq
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Representation of the grid
grid = [
    ['S', 'R', 'R', 'R', 'B', 'W', 'R', 'H', 'H', 'H'],
    ['R', 'B', 'B', 'R', 'H', 'H', 'R', 'R', 'B', 'H'],
    ['R', 'P', 'P', 'R', 'B', 'R', 'R', 'R', 'B', 'R'],
    ['R', 'R', 'R', 'R', 'W', 'R', 'P', 'P', 'R', 'R'],
    ['R', 'R', 'B', 'R', 'R', 'R', 'H', 'H', 'R', 'B'],
    ['B', 'W', 'R', 'P', 'P', 'R', 'B', 'R', 'R', 'R'],
    ['P', 'P', 'R', 'R', 'R', 'R', 'R', 'R', 'B', 'B'],
    ['R', 'B', 'R', 'R', 'R', 'W', 'H', 'H', 'R', 'R'],
    ['R', 'R', 'R', 'R', 'B', 'R', 'R', 'R', 'B', 'R'],
    ['H', 'H', 'H', 'B', 'B', 'R', 'R', 'G', 'R', 'R']
]

# Cost definition for each terrain type
costs = {
    'S': 0,
    'G': 0,
    'R': 1,
    'H': 0.5,
    'B': float('inf'),
    'P': 2,
    'W': float('inf')
}

# Start and goal coordinates
start = (0, 0)
goal = (9, 7)

# Corrected heuristic function (Manhattan distance divided by 2)
def heuristic(a, b):
    return (abs(a[0] - b[0]) + abs(a[1] - b[1])) / 2

# A* algorithm
def a_star_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    expanded_nodes = 0
    fringe_order = []
    energy_per_node = []

    while frontier:
        current_priority, current = heapq.heappop(frontier)
        fringe_order.append(current)
        expanded_nodes += 1
        energy_per_node.append((current, cost_so_far[current]))

        if current == goal:
            break

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next = (current[0] + dx, current[1] + dy)
            if 0 <= next[0] < rows and 0 <= next[1] < cols:
                new_cost = cost_so_far[current] + costs[grid[next[0]][next[1]]]
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current

    # Reconstruct the path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
        if current is None:  # If there is no path
            return float('inf'), expanded_nodes, fringe_order, energy_per_node, []
    path.append(start)
    path.reverse()

    return cost_so_far[goal], expanded_nodes, fringe_order, energy_per_node, path

# Execute the A* algorithm
total_cost, expanded_nodes, fringe_order, energy_per_node, path = a_star_search(grid, start, goal)

print("Total cost:", total_cost)
print("Number of expanded nodes:", expanded_nodes)
print("Fringe order:", fringe_order)
print("Energy per node:", energy_per_node)
print("Path:", path)