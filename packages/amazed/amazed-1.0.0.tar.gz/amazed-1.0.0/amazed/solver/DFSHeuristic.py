from amazed.maze import Maze
from amazed.solver.Solver import Solver
        
    
class DFSHeuristic(Solver):
    def solve(self, h=None):
        '''
        Adds to the stack based on a heuristic distance.
        '''
        self.steps.clear()

        def _h(start, end):
            (x, y) = start
            (endx, endy) = end

            return ((x-endx)**2 + (y-endy)**2) ** (0.5)
        
        h = _h if h is None else h
        self.cells = [self.start]

        while self.cells[-1] != self.end:
            (x, y) = self.cells[-1]
            self.visited.append((x, y))

            pqueue = []
            # North
            if self.maze.is_valid_position(x-1, y) and not self.maze.is_wall(x, y, x-1, y) and not (x-1, y) in self.visited:
                distance = h((x-1, y), self.end)
                pqueue.append((x-1, y, distance))
            
            # East
            if self.maze.is_valid_position(x, y+1) and not self.maze.is_wall(x, y, x, y+1) and not (x, y+1) in self.visited:
                distance = h((x, y+1), self.end)
                pqueue.append((x, y+1, distance))
            
            # South
            if self.maze.is_valid_position(x+1, y) and not self.maze.is_wall(x, y, x+1, y) and not (x+1, y) in self.visited:
                distance = h((x+1, y), self.end)
                pqueue.append((x+1, y, distance))
            
            # West
            if self.maze.is_valid_position(x, y-1) and not self.maze.is_wall(x, y, x, y-1) and not (x, y-1) in self.visited:
                distance = h((x, y-1), self.end)
                pqueue.append((x, y-1, distance))

            if len(pqueue) != 0:
                # Sort the queue based on distance
                pqueue.sort(key=lambda tup:tup[2])
                self.cells.append((pqueue[0][0], pqueue[0][1]))
            else:
                self.cells.pop()

            if len(self.cells) == 0:
                raise ValueError(f"Could not find a connected path from {self.start} to {self.end}!")
            
        # Deep copy the list
        for cell in self.cells:
            self.steps.append(cell)