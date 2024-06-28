import numpy as np

from amazed.solver.Solver import Solver

class Lee(Solver):
    '''
    Used to find the shortest possible path from start to finish.
    '''
    
    def solve(self):
        '''
        Applies the Lee Traversal Algorithm on the given maze.
        '''
        queue = [(self.start[0], self.start[1], 0)]

        # Mark all cells as unvisited with -1.
        self.array = np.full((self.maze.rows, self.maze.columns), -1)

        while len(queue) != 0:

            (x, y, current_value) = queue.pop(0)

            self.array[x][y] = current_value

            # North
            if self.maze.is_valid_position(x-1, y) and not self.maze.is_wall(x, y, x-1, y) and self.array[x-1][y] == -1:
                queue.append((x-1, y, current_value+1))
        
            # East
            if self.maze.is_valid_position(x, y+1) and not self.maze.is_wall(x, y, x, y+1) and self.array[x][y+1] == -1:
                queue.append((x, y+1, current_value+1))

            # South
            if self.maze.is_valid_position(x+1, y) and not self.maze.is_wall(x, y, x+1, y) and self.array[x+1][y] == -1:
                queue.append((x+1, y, current_value+1))

            # West
            if self.maze.is_valid_position(x, y-1) and not self.maze.is_wall(x, y, x, y-1) and self.array[x][y-1] == -1:
                queue.append((x, y-1, current_value+1))

        if self.array[self.maze.rows-1][self.maze.columns-1] == -1:
            # self.maze.export(output=None)
            raise RuntimeError(f"Could not find a path from start {self.start} to finish {self.end}!")

        # Start from the end point and go to a position that is always LOWER
        self.steps.append(self.end)
        while self.steps[-1] != self.start:
            (row, col) = self.steps[-1]

            # Find a suitable position to go towards
            if self.maze.is_valid_position(row-1, col) and not self.maze.is_wall(row, col, row-1, col) and self.array[row][col] - 1 == self.array[row-1][col]:
                self.steps.append((row-1, col))
                continue
            if self.maze.is_valid_position(row, col+1) and not self.maze.is_wall(row, col, row, col+1) and self.array[row][col] - 1 == self.array[row][col+1]:
                self.steps.append((row, col+1))
                continue
            if self.maze.is_valid_position(row+1, col) and not self.maze.is_wall(row, col, row+1, col) and self.array[row][col] - 1 == self.array[row+1][col]:
                self.steps.append((row+1, col))
                continue
            if self.maze.is_valid_position(row, col-1) and not self.maze.is_wall(row, col, row, col-1) and self.array[row][col] - 1 == self.array[row][col-1]:
                self.steps.append((row, col-1))
                continue

        self.steps.reverse()

    def is_connected(self):
        '''
        A maze is connected if all cells are accessible.
        '''

        for i in range(self.maze.rows):
            for j in range(self.maze.columns):
                if self.array[i][j] == -1:
                    return False
        return True

    def score(self):
        return self.array[self.end[0]][self.end[1]]
