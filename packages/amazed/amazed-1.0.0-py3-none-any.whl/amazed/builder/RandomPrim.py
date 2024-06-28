import random

from amazed.maze import Maze
from amazed.builder.Builder import Builder


class RandomPrim(Builder):
    def __init__(self, maze: Maze, seed: int = None, gif: bool = False, x: int = None, y: int = None) -> None:
        '''
        If @x and @y are left as None, they start off from the center of the maze.
        '''
        super().__init__(maze, seed, gif)

        x = maze.rows // 2 if x is None else x
        y = maze.columns // 2 if y is None else y

        if gif:
            self.add_frame(x, y)

        visited = set()
        
        visited.add((x, y))
        frontier = []
        while len(visited) != maze.rows * maze.columns:
            # Iterate through the visited array and add all cells that have an unvisited neighbor
            for (x, y) in visited:
                # Check all neighbors of (x, y)
                if (x-1, y) not in visited and maze.is_valid_position(x-1, y) and (x, y, x-1, y) not in frontier:
                    frontier.append((x, y, x-1, y))
                if (x, y+1) not in visited and maze.is_valid_position(x, y+1) and (x, y, x, y+1) not in frontier:
                    frontier.append((x, y, x, y+1))
                if (x+1, y) not in visited and maze.is_valid_position(x+1, y) and (x, y, x+1, y) not in frontier:
                    frontier.append((x, y, x+1, y))
                if (x, y-1) not in visited and maze.is_valid_position(x, y-1) and (x, y, x, y-1) not in frontier:
                    frontier.append((x, y, x, y-1))

            if len(frontier) == 0:
                raise ValueError(f"It seems that frontier has a length of 0. Here is what I known.\nvisited = {visited}")

            # Find a pair of visited_cell and unvisited_cell in frontier
            random.shuffle(frontier)

            for x1, y1, x2, y2 in frontier:
                if (x2, y2) not in visited:
                    break

            if gif:
                self.add_frame(x1, y1)

            maze.path_to_cell(x1, y1, x2, y2)
            visited.add((x2, y2))

            if gif:
                self.add_frame(x2, y2)
