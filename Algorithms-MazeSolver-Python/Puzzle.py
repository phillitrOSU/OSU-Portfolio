# Author: Trevor Phillips
# GitHub username: phillitrOSU
# Date: 11/19/2022
# Description: Finds the minimum length path through a puzzle of cells with obstacles.

import heapq

def find_neighbors(Board, cell, connection, cells):
    """
    Returns a list of valid path coordinates given a board of cells.
    :param Board: A list of lists where '-' is a passable and '#' is impassable.
    :param cell: A tuple representing the indices of the cell cell.
    :param Previous: A tuple representing the previous cell.
    :return find_neighbors: A list of tuples representing possible directions.
    """
    row, column = cell[0], cell[1]

    # Determine neighbor cells.
    left, right, up, down = (row, column - 1), (row, column + 1), (row - 1, column), (row + 1, column)
    neighbors = [(left, 'L'), (right, 'R'), (up, 'U'), (down, 'D')]

    # Remove out of bounds cells and already processed cells.
    for neighbor in neighbors[:]:
        if neighbor[0][0] < 0 or neighbor[0][0] >= len(Board):
            neighbors.remove(neighbor)
        elif neighbor[0][1] < 0 or neighbor[0][1] >= len(Board[row]):
            neighbors.remove(neighbor)
        elif Board[neighbor[0][0]][neighbor[0][1]] == "#":
            neighbors.remove(neighbor)
        elif neighbor[0] == connection:
            neighbors.remove(neighbor)
        elif cells[neighbor[0]][2] == True:
            neighbors.remove(neighbor)

    return neighbors

def solve_puzzle(Board, Source, Destination):
    """
    Returns the minimum length path from source to destination given a board of cells.
    :param Board: A list of lists where '-' is a passable and '#' is impassable.
    :param Source: A tuple representing the indices of the starting cell.
    :param Destination: A tuple representing the indices of the ending cell.
    :return path: A list of tuples representing the cells in the minimum length path.
    """
    # Initialize key/value pairs -- coordinates: [distance to destination, connection cell, visited, connect-direction, distance from source]
    cells = {(row, column): [abs(Destination[0] - row) + abs(Destination[1] - column), None, False, None, float('inf')] \
                for row in range(len(Board)) for column in range(len(Board[0]))}

    # Set source to visited (distance 0).
    cells[Source][2], cells[Source][4] = True, 0

    # Initialize min queue with Source neighbors.
    neighbors = find_neighbors(Board, Source, None, cells)
    neighbor_list = [(neighbor[0], Source, neighbor[1]) for neighbor in neighbors]

    while len(neighbor_list) > 0:
        # Pop the neighbor closest to the destination and mark visited.
        cell, connection, direction = neighbor_list.pop()
        cells[cell][2] = True

        # If the path is an improvement update connection, connect direction and total distance.
        if cells[cell][4] > cells[connection][4] + 1:
            cells[cell][1], cells[cell][3] = connection, direction
            cells[cell][4] = cells[connection][4] + 1

        # Push cell neighbors to the min queue.
        neighbors = find_neighbors(Board, cell, connection, cells)
        for neighbor in neighbors:
            neighbor_list.append((neighbor[0], cell, neighbor[1]))

    # If the destination was not visited, no path is possible.
    if cells[Destination][2] == False:
        return None

    # Traceback from Destination to Source to create directions.
    path, directions, current_cell = [Destination], [], Destination
    while current_cell != Source:
        connection, direction = cells[current_cell][1], cells[current_cell][3]
        directions.append(direction)
        path.append(connection)

        current_cell = connection

    # Reverse path from Destination to Source to find path from Source to Destination
    directions.reverse()
    directions = ''.join(directions)
    path.reverse()

    return (path, directions)



Puzzle = [
    ['-', '#', '-', '-'],
    ['-', '-', '-', '-'],
]

print(solve_puzzle(Puzzle, (0,0), (1,3)))