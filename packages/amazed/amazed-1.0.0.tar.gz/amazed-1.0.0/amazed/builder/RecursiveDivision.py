import random

from amazed.maze import Maze
from amazed.builder.Builder import Builder

class RecursiveDivision(Builder):
    def __init__(self, maze: Maze, seed: int = None, gif: bool = False) -> None:
        super().__init__(maze, seed, gif)

        self.__recursive_division__(0, maze.rows-1, 0, maze.columns-1)
        
        # Because the algorithm work by adding walls, we toggle them at the end
        maze.toggle()

    def __recursive_division__(self, start_row, end_row, start_column, end_column):
        '''
        row \\in [start_row, end_row] (INCLUSIVE)\n
        column \\in [start_column, end_column] (INCLUSIVE)\n
        The rows & columns are for cells in the maze. However, the algorithm works with wall lines, not cell lines.
        '''

        # Base case
        if end_row - start_row == 0 and end_column - start_column == 0:
            return

        # There is always one more wall
        walls_row = end_row - start_row + 1
        walls_column = end_column - start_column + 1

        if walls_row > walls_column:
            wall_index = walls_row // 2 + start_row

            # This is the wall that will "remain", later being turn into a path by .toggle()
            random_wall_column = random.randint(start_column, end_column)
            for i in range(start_column, end_column+1):
                if i != random_wall_column:
                    self.maze.path(wall_index-1, i, Maze.SOUTH)
            
            self.__recursive_division__(start_row, wall_index-1, start_column, end_column)
            self.__recursive_division__(wall_index, end_row, start_column, end_column)
        
        else:
            wall_index = walls_column // 2 + start_column

            random_wall_row = random.randint(start_row, end_row)
            for i in range(start_row, end_row+1):
                if i != random_wall_row:
                    self.maze.path(i, wall_index-1, Maze.EAST)

            self.__recursive_division__(start_row, end_row, start_column, wall_index-1)
            self.__recursive_division__(start_row, end_row, wall_index, end_column)
