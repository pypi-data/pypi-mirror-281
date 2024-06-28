import random

from amazed.maze import Maze
from amazed.builder.Builder import Builder

class RandomKruskal(Builder):
    def __init__(self, maze: Maze, seed: int = None, gif: bool = False) -> None:
        super().__init__(maze, seed, gif)
        
        if gif:
            self.add_frame(0, 0)

        list_of_cells = []
        for i in range(maze.rows):
            for j in range(maze.columns):
                list_of_cells.append([ [i, j] ])
        
        list_of_edges = []
        for i in range(maze.rows):
            for j in range(maze.columns):
                if maze.is_valid_position(i-1, j):
                    list_of_edges.append((i, j, i-1, j))
                if maze.is_valid_position(i+1, j):
                    list_of_edges.append((i, j, i+1, j))
                if maze.is_valid_position(i, j-1):
                    list_of_edges.append((i, j, i, j-1))
                if maze.is_valid_position(i, j+1):
                    list_of_edges.append((i, j, i, j+1))
        
        random.shuffle(list_of_edges)
        for edge in list_of_edges:
            x1, y1, x2, y2 = edge

            # Find cell_set for (x1, y1)
            cell_set_1 = list_of_cells[0]
            for cell_set in list_of_cells:
                if [x1, y1] in cell_set:
                    cell_set_1 = cell_set
                    break
            # Find cell_set for (x2, y2)
            cell_set_2 = list_of_cells[0]
            for cell_set in list_of_cells:
                if [x2, y2] in cell_set:
                    cell_set_2 = cell_set
                    break
            
            
            if cell_set_1 != cell_set_2:
                new_cell_list = cell_set_1 + cell_set_2
                new_cell_list = new_cell_list.copy()
                list_of_cells.append(new_cell_list)
                list_of_cells.remove(cell_set_1)
                list_of_cells.remove(cell_set_2)

                maze.path_to_cell(x1, y1, x2, y2)
                if gif:
                    self.add_frame(x1, y1)
                    self.add_frame(x2, y2)

