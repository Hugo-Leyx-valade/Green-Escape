import time
import heapq
from collections import deque

def solve_with_astar(grid, start, goal):
    start_time = time.perf_counter()

    def heuristic(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = current[0] + dx, current[1] + dy
            next_node = (nx, ny)

            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                if grid[ny][nx] == 1:  # mur
                    continue

                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

    end_time = time.perf_counter()
    return end_time - start_time

def solve_with_dijkstra(grid, start, goal):
    start_time = time.perf_counter()

    frontier = []
    heapq.heappush(frontier, (0, start))
    distances = {start: 0}

    while frontier:
        dist, current = heapq.heappop(frontier)

        if current == goal:
            break

        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)

            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                if grid[ny][nx] == 1:
                    continue

                new_dist = dist + 1
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(frontier, (new_dist, neighbor))

    end_time = time.perf_counter()
    return end_time - start_time

def solve_with_bfs(grid, start, goal):
    start_time = time.perf_counter()

    queue = deque([start])
    visited = set()
    visited.add(start)

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)

            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                if grid[ny][nx] == 1:
                    continue
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    end_time = time.perf_counter()
    return end_time - start_time
