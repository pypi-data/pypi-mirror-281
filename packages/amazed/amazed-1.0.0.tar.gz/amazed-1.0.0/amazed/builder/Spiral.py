import random

from amazed.maze import Maze
from amazed.builder.Builder import Builder

class Spiral(Builder):
    def __init__(self, maze: Maze, seed: int = None, gif: bool = False, x:int = 0, y:int = 0, max_len:int = 10) -> None:
        '''
        Inspired by hunt and kill.
        Select the starting node as (x, y)\n.
        While the current node is NOT visited or NOT outside the maze, select a random direction and follow it until you end up
        with a visited cell or you run out of the maze. Next, starting from (0, 0), perform a grid search and select the next
        unvisited cell and repeat.\n
        can be paired nicely with RandomCarving object.

        @max_len    : represents how long a hallway can be
        '''
        super().__init__(maze, seed, gif)


        if gif:
            self.add_frame(x, y)

        visited = set()
        last_dir = None
        last_selected_position = 0
        while len(visited) != maze.rows * maze.columns:

            possible_directions = []
            if maze.is_valid_position(x-1, y) and (x-1, y) not in visited: possible_directions.append(Maze.NORTH)
            if maze.is_valid_position(x, y+1) and (x, y+1) not in visited: possible_directions.append(Maze.EAST)
            if maze.is_valid_position(x+1, y) and (x+1, y) not in visited: possible_directions.append(Maze.SOUTH)
            if maze.is_valid_position(x, y-1) and (x, y-1) not in visited: possible_directions.append(Maze.WEST)
            

            if len(possible_directions) == 0:
                visited.add((x, y))

                # Select the next unvisited cell
                i = last_selected_position // maze.columns
                j = last_selected_position % maze.columns
                while maze.columns * i + j < maze.rows * maze.columns:
                    if (i, j) not in visited:
                        x = i
                        y = j
                        if gif:
                            self.add_frame(x, y)
                        last_selected_position = i * maze.columns + j
                        break
                    j += 1
                    if j >= maze.columns:
                        j = 0
                        i += 1
                

                continue
            

            # Increase chances to not follow the same direction
            if last_dir is not None:
                aux = possible_directions
                for _ in aux:
                    if _ != last_dir:
                        possible_directions.append(_)
            _dir = random.choice(possible_directions)
            length = 0
            while True:

                # Calculate the next move
                x_next = x
                y_next = y
                if _dir == Maze.NORTH: x_next = x - 1
                elif _dir == Maze.EAST: y_next = y + 1
                elif _dir == Maze.SOUTH: x_next = x + 1
                else: y_next = y - 1

                if length + 1 == max_len:
                    break
                if not maze.is_valid_position(x_next, y_next):
                    break
                if (x_next, y_next) in visited:
                    break
                
                visited.add((x, y))
                maze.path(x, y, _dir)
                length += 1

                x = x_next
                y = y_next
                if gif:
                    self.add_frame(x, y)

            # If there is no other cell unvisted adjaced to the current position, then search for a new start position.
            if maze.is_valid_position(x-1, y) and (x-1, y) not in visited or \
                maze.is_valid_position(x, y+1) and (x, y+1) not in visited or \
                maze.is_valid_position(x+1, y) and (x+1, y) not in visited or \
                maze.is_valid_position(x, y-1) and (x, y-1) not in visited:
                continue
            

            # Select the next unvisited cell
            i = last_selected_position // maze.columns
            j = last_selected_position % maze.columns
            while maze.columns * i + j < maze.rows * maze.columns:
                if (i, j) not in visited:
                    x = i
                    y = j
                    last_selected_position = i * maze.columns + j
                    if gif:
                        self.add_frame(x, y)
                    break
                j += 1
                if j >= maze.columns:
                    j = 0
                    i += 1
