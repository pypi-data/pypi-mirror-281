import random
import numpy as np

from amazed.maze import Maze
from amazed.builder.Builder import Builder

class DepthFirstSearch(Builder):
    def __init__(self, maze: Maze, seed: int = None, gif: bool = False, x: int = 0, y: int = 0, randomized: bool = True, biased_dirs: list = None, biased_level: int = 0) -> None:
        super().__init__(maze, seed, gif)

        if gif:
            self.add_frame(x, y)

        visited = np.zeros((maze.rows, maze.columns))
        stack = list()

        stack.append((-1, -1, x, y))
        while len(stack) > 0:
            (from_x, from_y, x, y) = stack.pop()
            
            
            if visited[x][y] == 1:
                continue

            visited[x][y] = 1

            if from_x != -1 and from_y != -1:
                maze.path_to_cell(from_x, from_y, x, y)
                if gif:
                    self.add_frame(x, y)
            
            # Search for a valid next position
            possible_directions = []
            if maze.is_valid_position(x-1, y) and visited[x-1][y] == 0:

                # Bias control
                if biased_dirs is not None and biased_level > 0:
                    if Maze.NORTH in biased_dirs:
                        for _ in range(biased_level):
                            possible_directions.append((x-1, y))

                possible_directions.append((x-1, y))
            if maze.is_valid_position(x, y+1) and visited[x][y+1] == 0:
                
                # Bias control
                if biased_dirs is not None and biased_level > 0:
                    if Maze.EAST in biased_dirs:
                        for _ in range(biased_level):
                            possible_directions.append((x, y+1))

                possible_directions.append((x, y+1))
            if maze.is_valid_position(x+1, y) and visited[x+1][y] == 0:
                
                # Bias control
                if biased_dirs is not None and biased_level > 0:
                    if Maze.SOUTH in biased_dirs:
                        for _ in range(biased_level):
                            possible_directions.append((x+1, y))

                possible_directions.append((x+1, y))
            if maze.is_valid_position(x, y-1) and visited[x][y-1] == 0:
                
                # Bias control
                if biased_dirs is not None and biased_level > 0:
                    if Maze.WEST in biased_dirs:
                        for _ in range(biased_level):
                            possible_directions.append((x, y-1))

                possible_directions.append((x, y-1))

            # No more new directions available
            if len(possible_directions) == 0:
                continue

            if randomized:
                random.shuffle(possible_directions)

            for dir in possible_directions:
                (to_x, to_y) = dir
                stack.append((x, y, to_x, to_y))
                
        if gif:
            self.add_frame(0, 0)
 