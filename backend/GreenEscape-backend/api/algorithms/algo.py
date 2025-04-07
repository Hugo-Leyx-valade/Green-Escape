import random

WIDTH = 59  # Largeur du labyrinthe (doit être impair)
HEIGHT = 29  # Hauteur du labyrinthe (doit être impair)
assert WIDTH % 2 == 1 and WIDTH >= 3
assert HEIGHT % 2 == 1 and HEIGHT >= 3

EMPTY = ' '
WALL = chr(9608)  # █
NORTH, SOUTH, EAST, WEST = 'n', 's', 'e', 'w'

# Fonctions internes --------------------------------------------------

def printMaze(maze, entrance=None, exit=None):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if entrance and entrance[0] == x and entrance[1] == y:
                print('@', end='')
            elif exit and exit[0] == x and exit[1] == y:
                print('#', end='')
            else:
                print(maze[(x, y)], end='')
        print()

def isIntersection(x, y, maze):
    directions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    empty_neighbors = 0
    for dx, dy in directions:
        if 0 <= dx < WIDTH and 0 <= dy < HEIGHT and maze[(dx, dy)] == EMPTY:
            empty_neighbors += 1
    return empty_neighbors > 2

def visit(x, y, maze, hasVisited):
    maze[(x, y)] = EMPTY
    while True:
        unvisitedNeighbors = []
        if y > 1 and (x, y - 2) not in hasVisited:
            unvisitedNeighbors.append(NORTH)
        if y < HEIGHT - 2 and (x, y + 2) not in hasVisited:
            unvisitedNeighbors.append(SOUTH)
        if x > 1 and (x - 2, y) not in hasVisited:
            unvisitedNeighbors.append(WEST)
        if x < WIDTH - 2 and (x + 2, y) not in hasVisited:
            unvisitedNeighbors.append(EAST)

        if len(unvisitedNeighbors) == 0:
            return
        else:
            nextDirection = random.choice(unvisitedNeighbors)
            if nextDirection == NORTH:
                nextX, nextY = x, y - 2
                maze[(x, y - 1)] = EMPTY
            elif nextDirection == SOUTH:
                nextX, nextY = x, y + 2
                maze[(x, y + 1)] = EMPTY
            elif nextDirection == WEST:
                nextX, nextY = x - 2, y
                maze[(x - 1, y)] = EMPTY
            elif nextDirection == EAST:
                nextX, nextY = x + 2, y
                maze[(x + 1, y)] = EMPTY

            hasVisited.append((nextX, nextY))
            visit(nextX, nextY, maze, hasVisited)

def createEntranceAndExit(maze, width, height):
    entrance_candidates = [(0, y) for y in range(1, height - 1, 2)] + [(width - 1, y) for y in range(1, height - 1, 2)]
    exit_candidates = [(x, 0) for x in range(1, width - 1, 2)] + [(x, height - 1) for x in range(1, width - 1, 2)]

    entrance = random.choice(entrance_candidates)
    exit_point = random.choice(exit_candidates)

    while entrance == exit_point:
        exit_point = random.choice(exit_candidates)

    maze[entrance] = EMPTY
    maze[exit_point] = EMPTY
    return entrance, exit_point

def mazeToArrayWithIntersections(maze):
    array = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            if maze[(x, y)] == WALL:
                row.append(1)
            else:
                row.append(0)
        array.append(row)
    return array


def generate_maze(seed):
    random.seed(seed)

    maze = {}
    for x in range(WIDTH):
        for y in range(HEIGHT):
            maze[(x, y)] = WALL

    hasVisited = [(1, 1)]
    visit(1, 1, maze, hasVisited)

    entrance, exit_point = createEntranceAndExit(maze, WIDTH, HEIGHT)
    maze_array = mazeToArrayWithIntersections(maze)

    return {
        "maze": maze_array,
        "entrance": entrance,
        "exit": exit_point,
        "seed": seed
    }
