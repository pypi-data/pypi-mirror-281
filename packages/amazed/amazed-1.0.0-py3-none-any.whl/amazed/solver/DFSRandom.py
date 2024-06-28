from amazed.solver.Solver import Solver

from random import shuffle

class DFSRandom(Solver):
    def solve(self):
        '''
        Uses the Depth-First search approach to find the shortes path from start to finish.
        It uses a random approach to search for the next path.
        '''

        self.cells = [self.start]
        self.visited = [self.start]

        while self.cells[-1] != self.end:
            if len(self.cells) == 0:
                raise ValueError(f"Could not find a connected path from {self.start} to {self.finish}!")

            (x, y) = self.cells[-1]

            order = ["North", "East", "South", "West"]
            shuffle(order)

            direction_set = False
            for dir in order:
                if dir == "North":
                    if self.maze.is_valid_position(x-1, y) and not self.maze.is_wall(x, y, x-1, y) and not (x-1, y) in self.visited:
                        self.cells.append((x-1, y))
                        self.visited.append((x-1, y))
                        direction_set = True
                        break
                
                if dir == "East":
                    if self.maze.is_valid_position(x, y+1) and not self.maze.is_wall(x, y, x, y+1) and not (x, y+1) in self.visited:
                        self.cells.append((x, y+1))
                        self.visited.append((x, y+1))
                        direction_set = True
                        break

                if dir == "South":
                    if self.maze.is_valid_position(x+1, y) and not self.maze.is_wall(x, y, x+1, y) and not (x+1, y) in self.visited:
                        self.cells.append((x+1, y))
                        self.visited.append((x+1, y))
                        direction_set = True
                        break
                
                if dir == "West":
                    if self.maze.is_valid_position(x, y-1) and not self.maze.is_wall(x, y, x, y-1) and not (x, y-1) in self.visited:
                        self.cells.append((x, y-1))
                        self.visited.append((x, y-1))
                        direction_set = True
                        break
            
            if direction_set:
                continue

            self.cells.pop()
            
        # Deep copy the list
        for cell in self.cells:
            self.steps.append(cell)