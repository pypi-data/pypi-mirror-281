from amazed.solver.Solver import Solver

class DFS(Solver):
    def solve(self):
        '''
        Uses the Depth-First search approach to find the shortes path from start to finish.
        It uses a deterministic approach to search for the next path (clock-wise).
        '''

        self.cells = [self.start]
        self.visited = [self.start]
        self.steps.clear()

        while self.cells[-1] != self.end:
            if len(self.cells) == 0:
                raise ValueError(f"Could not find a connected path from {self.start} to {self.finish}!")

            (x, y) = self.cells[-1]
            self.steps.append((x, y))

            # North
            if self.maze.is_valid_position(x-1, y) and not self.maze.is_wall(x, y, x-1, y) and not (x-1, y) in self.visited:
                self.cells.append((x-1, y))
                self.visited.append((x-1, y))
                continue
            
            # East
            if self.maze.is_valid_position(x, y+1) and not self.maze.is_wall(x, y, x, y+1) and not (x, y+1) in self.visited:
                self.cells.append((x, y+1))
                self.visited.append((x, y+1))
                continue

            # South
            if self.maze.is_valid_position(x+1, y) and not self.maze.is_wall(x, y, x+1, y) and not (x+1, y) in self.visited:
                self.cells.append((x+1, y))
                self.visited.append((x+1, y))
                continue
            
            # West
            if self.maze.is_valid_position(x, y-1) and not self.maze.is_wall(x, y, x, y-1) and not (x, y-1) in self.visited:
                self.cells.append((x, y-1))
                self.visited.append((x, y-1))
                continue

            self.cells.pop()
            
        self.steps.append(self.end)
        # # Deep copy the list
        # # This only shows the final steps (we want the FULL search.)
        # self.steps.clear()
        # for cell in self.cells:
        #     self.steps.append(cell)