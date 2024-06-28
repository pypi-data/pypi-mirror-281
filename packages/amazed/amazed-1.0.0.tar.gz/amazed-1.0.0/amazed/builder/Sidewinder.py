import random

from amazed.maze import Maze
from amazed.builder.Builder import Builder

class Sidewinder(Builder):
    def __init__(self, maze: Maze, seed: int = None, gif: bool = False) -> None:
        super().__init__(maze, seed, gif)

        if gif:
            self.add_frame(0, 0)

        
        # The first row needs to be fully carved to the east
        for i in range(maze.columns):
            if maze.is_valid_position(0, i+1):
                maze.path(0, i, Maze.EAST)
            if gif:
                self.add_frame(0, i)


        run = []
        for i in range(1, maze.rows):
            run.clear()
            for j in range(maze.columns):
                run.append((i, j))
                
                # Can we carve EAST?
                if maze.is_valid_position(i, j+1) and random.random() > 0.5:
                        maze.path(i, j, Maze.EAST)
                else:
                    cell = random.choice(run)
                    maze.path(cell[0], cell[1], Maze.NORTH)
                    run.clear()
                
                if gif:
                    self.add_frame(i, j)
