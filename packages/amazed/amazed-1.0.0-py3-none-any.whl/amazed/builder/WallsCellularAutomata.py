import random

from amazed.maze import Maze
from amazed.builder.Builder import Builder

class WallsCellularAutomata(Builder):
    '''
    CA that evolves the maze, starting from the initial state for X generations.\n
    It uses a 3-neighbors rule. By default it uses Rule 110:\n
    '111': '0',\n
    '110': '1',\n
    '101': '1',\n
    '100': '0',\n
    '011': '1',\n
    '010': '1',\n
    '001': '1',\n
    '000': '0'
    '''
    def __init__(self, maze: Maze, seed: int = None, gif: bool = False, generations:int=10, rules:dict=None) -> None:

        super().__init__(maze, seed, gif)

        if rules is None:
            rules = {
                '111': '0',
                '110': '1',
                '101': '1',
                '100': '0',
                '011': '1',
                '010': '1',
                '001': '1',
                '000': '0'
            }

        if gif:
            self.add_frame()

        bitstring = maze.get_wall_bitstring()
        new_bitstring = []
        for gen in range(generations):
            bitstring = ["1" if random.random() > 0.5 else "0"] + bitstring + ["1" if random.random() > 0.5 else "0"]
            new_bitstring.clear()

            for i in range(len(bitstring) - 2):
                neighbors = "".join([bitstring[1+i+j] for j in (-1, 0, 1)])
                new_bitstring += rules[neighbors]
            
            bitstring = new_bitstring
            self.maze.reset()
            self.maze.set_wall_bitstring(bitstring)
            if gif:
                self.add_frame()

    def add_frame(self):

        # Here you can modify the distance
        frame = self.maze.export(show=False)
        self.frames.append(frame)
