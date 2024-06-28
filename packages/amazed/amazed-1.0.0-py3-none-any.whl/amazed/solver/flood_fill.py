import numpy as np

from amazed.maze import Maze

def flood_fill(maze : Maze) -> int:
    '''
    It is not indended to be used as a unique solver between START and FINISH.\n
    It counts the total number of separate areas in a maze.
    '''

    # Mark all cells as unvisited with -1.
    array = np.full((maze.rows, maze.columns), -1)

    areas = 0
    for i in range(maze.rows):
        for j in range(maze.columns):
            if array[i][j] == -1:
                areas += 1
                queue = [(i, j, areas)]

                while len(queue) != 0:

                    (x, y, area_value) = queue.pop(0)

                    array[x][y] = area_value

                    # North
                    if maze.is_valid_position(x-1, y) and not maze.is_wall(x, y, x-1, y) and array[x-1][y] == -1:
                        queue.append((x-1, y, area_value))
                
                    # East
                    if maze.is_valid_position(x, y+1) and not maze.is_wall(x, y, x, y+1) and array[x][y+1] == -1:
                        queue.append((x, y+1, area_value))

                    # South
                    if maze.is_valid_position(x+1, y) and not maze.is_wall(x, y, x+1, y) and array[x+1][y] == -1:
                        queue.append((x+1, y, area_value))

                    # West
                    if maze.is_valid_position(x, y-1) and not maze.is_wall(x, y, x, y-1) and array[x][y-1] == -1:
                        queue.append((x, y-1, area_value))

    return areas