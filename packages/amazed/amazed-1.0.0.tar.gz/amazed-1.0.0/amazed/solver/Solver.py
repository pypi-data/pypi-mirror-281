from amazed.maze import Maze

from PIL import ImageDraw

class Solver:
    '''
    Class-template depicting a maze-solving algorithm.
    Each object will hold one and ONLY one path from start to finish.
    By default, the maze starts at (0, 0) and ends at (rows-1, columns-1).
    '''

    def __init__(self, maze : Maze, start=None, end=None):
        self.maze = maze
        self.steps = []
        self.visited = []

        self.start = (0, 0) if start is None else start
        self.end = (maze.rows-1, maze.columns-1) if end is None else end

    def solve(self):
        '''
        Virtual function which needs to be overwritten by all solving methods that inherit this class.
        '''
        raise NameError("Calling <solve()> from a template object!")

    def score(self):
        '''
        Euristich function used to determine how hard a maze was to solve.
        '''
        assert len(self.steps) > 0
        return len(self.steps)

    def gif(self, path):
        '''
        Creates a GIF at path @path by solving the maze.
        '''
        
        if len(self.steps) == 0:
            self.solve()

        frames = []
        proc = 10
        cell_colors = dict()
        for i, step in enumerate(self.steps):
            if i >= len(self.steps) * (proc / 100):
                print(f"[GIF][Solver]Progress: {proc}%")
                proc += 10


            # Skip over the start and end steps
            if step == self.start or step == self.end:
                continue

            cell_colors[f"{step[0]}, {step[1]}"] = self.maze.CURRENT_CELL_COLOR
            frames.append(self.maze.export(show=False, cell_colors=cell_colors))
            cell_colors[f"{step[0]}, {step[1]}"] = self.maze.VISITED_CELL_COLOR

        frames[0].save(path, format="GIF", append_images=frames, save_all=True, duration=50)
        print(f"GIF created at {path}")

    def image(self, path, cell_colors=None):
        '''
        Creates a static image at path @path representing the calculated solution.
        '''

        if len(self.steps) == 0:
            self.solve()
        
        distance = 10

        # cell_colors = {
        #     f"{self.start[0]}, {self.start[1]}" : Maze.START_COLOR,
        #     f"{self.end[0]}, {self.end[1]}" : Maze.END_COLOR
        # }

        image = self.maze.export(show=False, distance=distance, cell_colors=cell_colors)
        draw_image = ImageDraw.Draw(image)

        # Convert the steps from cell indexes to actual pixel points
        for e, step in enumerate(self.steps):
            (x, y) = step

            # Comment from me to me:
            # I know it is weird, but here, the coordinates are switched and IT WORKS like this.
            # I think it has to do with how "images" are stored, but I won't bother.
            # Just don't change :) 
            # # self.steps[e] =  (x*distance + distance/2, y*distance + distance/2)
            self.steps[e] =  (y*distance + distance/2, x*distance + distance/2)
        

        for i in range(1, len(self.steps)):
            draw_image.line((self.steps[i-1], self.steps[i]), fill='red', width=1)        

        image.save(path)
        print(f"Image created at {path}")
