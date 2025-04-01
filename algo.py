import random

WIDTH = 15  # Largeur du labyrinthe (doit être impair).
HEIGHT = 15  # Hauteur du labyrinthe (doit être impair).
assert WIDTH % 2 == 1 and WIDTH >= 3
assert HEIGHT % 2 == 1 and HEIGHT >= 3
SEED = 3
random.seed(SEED)

# Utiliser ces caractères pour afficher le labyrinthe :
EMPTY = ' '
MARK = '@'
WALL = chr(9608)  # Caractère 9608 est '█'
NORTH, SOUTH, EAST, WEST = 'n', 's', 'e', 'w'

# Créer la structure de données du labyrinthe remplie au début :
maze = {}
for x in range(WIDTH):
    for y in range(HEIGHT):
        maze[(x, y)] = WALL  # Chaque espace est un mur au début.

def printMaze(maze, entreance=None, exit=None):
    """Affiche la structure de données du labyrinthe dans l'argument maze. Les
    arguments markX et markY sont les coordonnées de l'emplacement actuel
    '@' de l'algorithme lorsqu'il génère le labyrinthe."""

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if entrance[0] == x and entrance[1] == y:
                # Afficher le marqueur '@' ici :
                print(MARK, end='')
            if exit[0] == x and exit[1] == y:
                # Afficher le marqueur '#' ici :
                print('#', end='')
            else:
                # Afficher le mur ou l'espace vide :
                print(maze[(x, y)], end='')
        print()  # Imprimer une nouvelle ligne après avoir imprimé la rangée.

def isIntersection(x, y, maze):
    """Vérifie si la cellule donnée (x, y) est une intersection."""
    directions = [
        (x - 1, y),  # Ouest
        (x + 1, y),  # Est
        (x, y - 1),  # Nord
        (x, y + 1)   # Sud
    ]
    empty_neighbors = 0
    for dx, dy in directions:
        if 0 <= dx < WIDTH and 0 <= dy < HEIGHT and maze[(dx, dy)] == EMPTY:
            empty_neighbors += 1
    return empty_neighbors > 2

def visit(x, y):
    """"Creuse" des espaces vides dans le labyrinthe à x, y puis
    se déplace de manière récursive vers les espaces voisins non visités. Cette
    fonction revient en arrière lorsque le marqueur a atteint une impasse."""
    maze[(x, y)] = EMPTY  # "Creuse" l'espace à x, y.

    while True:
        # Vérifier quels espaces voisins adjacents
        # au marqueur n'ont pas encore été visités :
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
            # CAS DE BASE
            # Tous les espaces voisins ont été visités, donc c'est une
            # impasse. Revenir à un espace précédent :
            return
        else:
            # CAS RÉCURSIF
            # Choisir aléatoirement un voisin non visité à visiter :
            nextIntersection = random.choice(unvisitedNeighbors)

            # Déplacer le marqueur vers un espace voisin non visité :
            if nextIntersection == NORTH:
                nextX = x
                nextY = y - 2
                maze[(x, y - 1)] = EMPTY  # Couloir de connexion.
            elif nextIntersection == SOUTH:
                nextX = x
                nextY = y + 2
                maze[(x, y + 1)] = EMPTY  # Couloir de connexion.
            elif nextIntersection == WEST:
                nextX = x - 2
                nextY = y
                maze[(x - 1, y)] = EMPTY  # Couloir de connexion.
            elif nextIntersection == EAST:
                nextX = x + 2
                nextY = y
                maze[(x + 1, y)] = EMPTY  # Couloir de connexion.

            hasVisited.append((nextX, nextY))  # Marquer comme visité.
            visit(nextX, nextY)  # Visiter cet espace de manière récursive.

def mazeToArrayWithIntersections(maze):
    """Convertit le dictionnaire du labyrinthe en un tableau 2D avec des 1 pour les murs, des 0 pour les espaces vides, et des 2 pour les intersections."""
    array = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            if maze[(x, y)] == WALL:
                row.append(1)
            else:
                # Vérifier si l'espace vide actuel est une intersection
                if isIntersection(x, y, maze):
                    row.append(2)
                else:
                    row.append(0)
        array.append(row)
    return array

def createEntranceAndExit(maze, width, height):
    """Crée une entrée et une sortie dans le labyrinthe sur les bordures."""
    # Définir les points d'entrée et de sortie possibles sur les bordures
    entrance_candidates = [(0, y) for y in range(1, height - 1)] + [(width - 1, y) for y in range(1, height - 1)]
    exit_candidates = [(x, 0) for x in range(1, width - 1)] + [(x, height - 1) for x in range(1, width - 1)]

    # Choisir aléatoirement une entrée et une sortie parmi les candidats
    entrance = random.choice(entrance_candidates)
    exit_point = random.choice(exit_candidates)

    # S'assurer que l'entrée et la sortie ne sont pas le même point
    while entrance == exit_point:
        exit_point = random.choice(exit_candidates)

    # Creuser l'entrée et la sortie dans le labyrinthe
    maze[entrance] = EMPTY
    maze[exit_point] = EMPTY

    return entrance, exit_point

# Creuser les chemins dans la structure de données du labyrinthe :
hasVisited = [(1, 1)]  # Commencer par visiter le coin supérieur gauche.
visit(1, 1)

# Créer une entrée et une sortie dans le labyrinthe
entrance, exit_point = createEntranceAndExit(maze, WIDTH, HEIGHT)

# Afficher la structure de données du labyrinthe final avec l'entrée marquée
printMaze(maze, entrance,exit_point)

# Convertir le labyrinthe en un tableau 2D avec les intersections marquées
mazeArrayWithIntersections = mazeToArrayWithIntersections(maze)

# Afficher le tableau 2D avec les intersections
for row in mazeArrayWithIntersections:
    print(row)

# Afficher les coordonnées de l'entrée et de la sortie
print("Entrée :", entrance)
print("Sortie :", exit_point)
