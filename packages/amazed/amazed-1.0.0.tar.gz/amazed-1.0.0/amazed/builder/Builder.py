import random
import threading
import time

from amazed.maze import Maze

class Builder():
    '''
    Default class for all maze generation classes.\n
    Carves a maze in-place.
    '''
    def __init__(self, maze: Maze, seed: int = None, gif: bool = False) -> None:
        self.maze = maze
        self.frames = []
        self.seed = random.random() if seed is None else seed
        random.seed(self.seed)

        self.cell_colors = {}

        if gif:
            self.progress_thread = threading.Thread(target=self.__progress__)
            self.progress_thread.daemon = True
            self.progress_thread.start()

    def add_frame(self, i, j):
        # Show the current cell as red
        self.cell_colors[f"{i}, {j}"] = self.maze.CURRENT_CELL_COLOR

        # Here you can modify the distance
        frame = self.maze.export(show=False, cell_colors=self.cell_colors)
        self.frames.append(frame)
        
        self.cell_colors[f"{i}, {j}"] = self.maze.VISITED_CELL_COLOR

    def export(self, path: str = "maze_carving_process.gif", speed=50, looping=False):
        '''
        Creates a GIF showing the carving process.
        '''
        if not path.endswith(".gif"):
            raise RuntimeError(f"'{path}' does not end with .gif")

        if len(self.frames) == 0:
            raise ValueError("\n\nNo frames available for GIF creation. Maybe you specified 'gif: False' when creating the object?")

        if looping:
            self.frames[0].save(path, format="GIF", append_images=self.frames, save_all=True, duration=speed, loop=1)
        else:
            # With no loop at all, it does not loop...
            self.frames[0].save(path, format="GIF", append_images=self.frames, save_all=True, duration=speed)

    def __progress__(self):
        '''
        Function used by the __init__ method for displaying a somewhat informative progress of the GIF creation.\n
        It takes into account an approximate amount of steps.\n
        It MUST NOT be called outside of __init__.
        '''
        total = self.maze.rows * self.maze.columns
        progress_steps = [0, 10, 25, 50, 75, 90, 100]
        while len(self.frames) <= total and len(progress_steps) > 0:
            actual_p = int(len(self.frames) / total * 100)
            
            if actual_p >= progress_steps[0]:
                print(f"GIF creation {actual_p}%")
                
                del progress_steps[0]
            time.sleep(0.1)
        
        if len(progress_steps) > 0:
            print(f"GIF creation 100%")