import random

from amazed.maze import Maze
from amazed.builder.Builder import Builder

class RandomCarving(Builder):
    def __init__(self, maze: Maze, seed: int = None, gif: bool = False, original_chance:int = 0.05, multicell:bool = True, adaptive:bool = True, adaptive_function = None) -> None:
        '''
        Break walls at random in the given @maze. Can be used as a method of creating multiple paths in a single-solution maze.

        @original_chance:   depicts how likely it is for a wall to be broken.
        @multicell: if set to True, will evaluate each individual wall in the current position. \n
                    Otherwise, will move on to the next wall after a successful break.
        @adaptive:  if set to True, the chance to break a wall will be influenced by the breaking of recent walls.\n
                    Otherwise, each wall will have the same chance to be broken.
        @adaptive_function: what function to use to update the chance after each unbroken wall. \n
                            MUST have the following signature: func (curr_chance, streak_number) -> float.\n
                            By default, it will increase by 0.3 for each consecutive unbreaked wall.\n
                            Works only if @adaptive is set to True.\n
        '''
        super().__init__(maze, seed, gif)

        
        adaptive_function = self.__adaptive_function__ if adaptive_function is None else adaptive_function

        if gif:
            self.add_frame(0, 0)

        chance = original_chance
        streak = 0

        for row in range(maze.rows):
            for col in range(maze.columns):
                valid_dir = []
                if gif:
                    self.add_frame(row, col)
                if maze.is_valid_position(row-1, col):
                    valid_dir.append(Maze.NORTH)
                if maze.is_valid_position(row, col+1):
                    valid_dir.append(Maze.EAST)
                if maze.is_valid_position(row+1, col):
                    valid_dir.append(Maze.SOUTH)
                if maze.is_valid_position(row, col-1):
                    valid_dir.append(Maze.WEST)

                assert len(valid_dir) >= 2
                
                if multicell:
                    for dir in valid_dir:
                        if random.random() < chance:
                            maze.path(row, col, dir)
                            streak = 0
                            chance = original_chance
                        else:
                            streak += 1
                            if adaptive:
                                chance = adaptive_function(original_chance, streak)

                else:
                    random.shuffle(valid_dir)
                    if random.random() < chance:
                        maze.path(row, col, valid_dir[0])
                        streak = 0
                        chance = original_chance
                    else:
                        streak += 1
                        if adaptive:
                            chance = adaptive_function(original_chance, streak)

    def __adaptive_function__(self, chance: float, streak: int) -> float:
        return chance + streak * 0.3
    