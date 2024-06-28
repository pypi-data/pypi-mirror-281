import random

from amazed.maze import Maze
from amazed.builder.Builder import Builder

class BinaryTree(Builder):
    def __init__(self, maze: Maze, seed: int = None, gif: bool = False) -> None:
        super().__init__(maze, seed, gif)

        if gif:
            self.add_frame(0, 0)
        
        for i in range(maze.rows):
            for j in range(maze.columns):
                # Carve North
                if random.random() < 0.5:
                    if maze.is_valid_position(i-1, j):
                        maze.path(i, j, Maze.NORTH)
                    # If the cell does not have a path to NORTH,
                    # instead carve a path to West
                    elif maze.is_valid_position(i, j-1):
                        maze.path(i, j, Maze.WEST)
                else:
                    if maze.is_valid_position(i, j-1):
                        maze.path(i, j, Maze.WEST)
                    # If the cell does not have a path to West,
                    # instead carve a path to NORTH
                    elif maze.is_valid_position(i-1, j):
                        maze.path(i, j, Maze.NORTH)
    
                if gif:
                    self.add_frame(i, j)