import random
import numpy as np

from amazed.maze import Maze
from amazed.builder.Builder import Builder

class AldousBroder(Builder):
    def __init__(self, maze: Maze, seed: int = None, gif: bool = False) -> None:
        super().__init__(maze, seed, gif)

        visited = np.full((maze.rows, maze.columns), False)

        # Random start position
        x = random.randint(0, maze.rows-1)
        y = random.randint(0, maze.columns-1)

        if gif:
            self.add_frame(x, y)
        while not np.all(visited):
            visited[x][y] = True

            possible_directions = []
            if maze.is_valid_position(x-1, y):
                possible_directions.append((x-1, y))
            if maze.is_valid_position(x, y+1):
                possible_directions.append((x, y+1))
            if maze.is_valid_position(x+1, y):
                possible_directions.append((x+1, y))
            if maze.is_valid_position(x, y-1):
                possible_directions.append((x, y-1))

            random.shuffle(possible_directions)
            found_dir = False
            for dir in possible_directions:
                if not visited[dir[0]][dir[1]]:
                    if gif:
                        self.add_frame(x, y)
                    maze.path_to_cell(x, y, dir[0], dir[1])
                    
                    x, y = dir
                    found_dir = True
                    break
            
            if not found_dir:
                if gif:
                    self.add_frame(x, y)
                x, y = possible_directions[0]
