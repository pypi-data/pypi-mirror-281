import random
import numpy as np

from amazed.maze import Maze
from amazed.builder.Builder import Builder

class HuntAndKill(Builder):
    def __init__(self, maze: Maze, seed: int = None, gif: bool = False, x: int = 0, y: int = 0) -> None:
        super().__init__(maze, seed, gif)

        visited = np.zeros((maze.rows, maze.columns))
        
        unvisited_row = 0
        unvisited_column = 0
        self.add_frame(x, y)
        for iter in range(maze.rows * maze.columns + 1):
            visited[x][y] = 1

            possible_directions = []
            if maze.is_valid_position(x-1, y) and visited[x-1][y] == 0:
                possible_directions.append(Maze.NORTH)
            if maze.is_valid_position(x, y+1) and visited[x][y+1] == 0:
                possible_directions.append(Maze.EAST)
            if maze.is_valid_position(x+1, y) and visited[x+1][y] == 0:
                possible_directions.append(Maze.SOUTH)
            if maze.is_valid_position(x, y-1) and visited[x][y-1] == 0:
                possible_directions.append(Maze.WEST)
            
            # Perform grid search in order to update x, y
            if len(possible_directions) == 0:

                found_unvisited = False
                while unvisited_row < maze.rows:
                    while unvisited_column < maze.columns:
                        # Make a wall in a random (valid) direction (of an already visited cell) from the first unvisited cell found
                        if visited[unvisited_row][unvisited_column] == 0:
                            possible_directions = []
                            if maze.is_valid_position(unvisited_row-1, unvisited_column) and visited[unvisited_row-1][unvisited_column] == 1:
                                possible_directions.append(Maze.NORTH)
                            if maze.is_valid_position(unvisited_row, unvisited_column+1) and visited[unvisited_row][unvisited_column+1] == 1:
                                possible_directions.append(Maze.EAST)
                            if maze.is_valid_position(unvisited_row+1, unvisited_column) and visited[unvisited_row+1][unvisited_column] == 1:
                                possible_directions.append(Maze.SOUTH)
                            if maze.is_valid_position(unvisited_row, unvisited_column-1) and visited[unvisited_row][unvisited_column-1] == 1:
                                possible_directions.append(Maze.WEST)
                            
                            random.shuffle(possible_directions)

                            # Update the current position
                            # if gif: 
                            #     self.add_frame(x, y)
                            x = unvisited_row
                            y = unvisited_column

                            maze.path(x, y, possible_directions[0])
                            if gif:
                                self.add_frame(x, y)

                            found_unvisited = True
                            break

                        unvisited_column += 1

                    if unvisited_column == maze.columns:
                        unvisited_row += 1
                        unvisited_column = 0

                    if found_unvisited:
                        break
                        
                    
            else:
                random.shuffle(possible_directions)
                maze.path(x, y, possible_directions[0])

                if gif:
                    self.add_frame(x, y)

                # Update current position
                if possible_directions[0] == Maze.NORTH:
                    x = x - 1
                elif possible_directions[0] == Maze.EAST:
                    y = y + 1
                elif possible_directions[0] == Maze.SOUTH:
                    x = x + 1
                else:
                    y = y - 1
        
        if gif:
            self.add_frame(x, y)