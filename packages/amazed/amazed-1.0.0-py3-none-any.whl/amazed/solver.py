from amazed.maze import Maze

import numpy as np
from random import shuffle
from PIL import ImageDraw

# from keras.models import Sequential

def standard_euclidian(start, end):
    (x, y) = start
    (endx, endy) = end
    return ((x-endx)**2 + (y-endy)**2) ** 0.5 

def modified_euclidian(start, end):
    (x, y) = start
    (endx, endy) = end
    return ((x-endx)**2 + (y-endy)**2)

def standard_manhattan(start, end):
    (x, y) = start
    (endx, endy) = end
    return abs(x-endx) + abs(y-endy)

def standard_minkowski(start, end, p=3):
    '''
    With p = 1, it's the same as Manhattan distance.\n
    With p = 2, it's the same as Euclidian distance.\n
    With p = inf, it's the same as Chebyshev distance.\n
    '''
    (x, y) = start
    (endx, endy) = end
    return (abs(x-endx)**p + abs(y-endy)**p) ** (1/p)

def flood_fill(maze : Maze) -> int:
    '''
    It is not indended to be used as a unique solver between START and FINISH.\n
    It counts the total number of separate areas in a maze.
    '''

    # Mark all cells as unvisited with -1.
    array = np.full((maze.rows, maze.columns), -1)

    areas = 0
    for i in range(maze.rows):
        for j in range(maze.columns):
            if array[i][j] == -1:
                areas += 1
                queue = [(i, j, areas)]

                while len(queue) != 0:

                    (x, y, area_value) = queue.pop(0)

                    array[x][y] = area_value

                    # North
                    if maze.is_valid_position(x-1, y) and not maze.is_wall(x, y, x-1, y) and array[x-1][y] == -1:
                        queue.append((x-1, y, area_value))
                
                    # East
                    if maze.is_valid_position(x, y+1) and not maze.is_wall(x, y, x, y+1) and array[x][y+1] == -1:
                        queue.append((x, y+1, area_value))

                    # South
                    if maze.is_valid_position(x+1, y) and not maze.is_wall(x, y, x+1, y) and array[x+1][y] == -1:
                        queue.append((x+1, y, area_value))

                    # West
                    if maze.is_valid_position(x, y-1) and not maze.is_wall(x, y, x, y-1) and array[x][y-1] == -1:
                        queue.append((x, y-1, area_value))

    return areas


class MazeSolver:
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
            draw_image.line((self.steps[i-1], self.steps[i]), fill='white', width=1)        

        image.save(path)
        print(f"Image created at {path}")



class DFS(MazeSolver):
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


class DFSRandom(MazeSolver):
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

    
class Lee(MazeSolver):
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


class AStar(MazeSolver):

    def solve(self, h = None):
        '''
        A* algorithm implementation using a BFS jumping method (the agent "jumps" from one known cell to another).
        G cost = distance from the starting node
        H cost (heuristic) = distance to the end node
        F cost = G+H
        selected new cell = min(F), if there are multiple of the same value, min(H) \n

        @h  : what heuristic function to use. Defaults to classical Euclidian distance.
        '''
        self.steps.clear()

        def _h(start, end):
            (x, y) = start
            (endx, endy) = end

            return ((x-endx)**2 + (y-endy)**2) ** (0.5)
        
        h = h or _h

        bfs = [
            {
                "node" : self.start,
                "gvalue": 0,
                "fvalue": h(self.start, self.end) + 0,
                "parent_index": -1,
                "closed": False
            }
        ]
        visited = []

        iter = 0
        while True:
            iter += 1
            # Select the node with the minimum F value
            curr_node = None
            for node_element in bfs:
                if node_element["closed"]:
                    continue
                if curr_node is None:
                    curr_node = node_element
                    continue
                fvalue = node_element["fvalue"]
                gvalue = node_element["gvalue"]

                if fvalue < curr_node["fvalue"]:
                    curr_node = node_element
                elif fvalue == curr_node["fvalue"] and gvalue < curr_node["gvalue"]:
                    curr_node = node_element
            
            if curr_node is None:
                print("current node is None!")
                print(f"END NODE: {self.end}")
                print(*bfs, sep='\n')

                cc = {}
                for node in bfs:
                    (x, y) = node["node"]
                    cc[f"{x}, {y}"] = (node["gvalue"]*1.5+100, 0, 0) 

                self.maze.export(output="tmp/astar_error.png", cell_colors=cc)
                raise ValueError("[AStar] Current node is None!")
            
            curr_node["closed"] = True

            visited.append(curr_node["node"])

            if curr_node["node"] == self.end:
                break
            
            # Check each neighbour and add it to the queue
            (x, y) = curr_node["node"]
            _list = self.maze.possible_actions(x, y)

            for move in _list:
                newx = x
                newy = y
                if move == Maze.NORTH: newx = x-1
                elif move == Maze.EAST: newy = y+1
                elif move == Maze.SOUTH: newx = x+1
                elif move == Maze.WEST: newy = y-1
                else:
                    raise ValueError(f"Unknown move type <{move}>")


                found = False
                for node_element in bfs:
                    # It already exists
                    if node_element["node"] == (newx, newy):
                        new_fvalue = curr_node["gvalue"] + 1 + h((newx, newy), self.end)
                        if node_element["fvalue"] > new_fvalue:
                            node_element["gvalue"] = curr_node["gvalue"] + 1
                            node_element["fvalue"] = new_fvalue

                            node_element["parent_index"] = bfs.index(curr_node)

                        found = True

                if not found:
                    bfs.append(
                        {
                            "node": (newx, newy),
                            "gvalue": curr_node["gvalue"] + 1,
                            "fvalue": curr_node["gvalue"] + 1 + h((newx, newy), self.end),
                            "parent_index": bfs.index(curr_node),
                            "closed":False
                        }
                    )
        
        node = bfs[-1]
        while node["parent_index"] != -1:
            self.steps.append(node["node"])
            node = bfs[node["parent_index"]]
        self.steps.append(self.start) 
        self.steps.reverse()         


class ReinforcementLearningSolver(MazeSolver):
    '''
    This class must use a pretrained agent.
    You can use different trained agents to solve the same maze multiple times. (But I advice agains it.)
    The training should be external in order to prevent too much coupling
    '''
    
    # def solve(self, model : Sequential, max_iter : int = None):
    def solve(self, model, max_iter : int = None):
        
        self.curr_cell = self.start

        arr = self.maze.array()
        state = np.zeros((4096 + 2,))
        state[0:4096] = arr
        
        max_iter = self.maze.rows * self.maze.columns if max_iter is None else max_iter

        while self.curr_cell != self.end and len(self.steps) < max_iter:

            self.steps.append(self.curr_cell)

            # Get the current state
            state[-2] = self.curr_cell[0]
            state[-1] = self.curr_cell[1]

            q_actions = model.predict(state)
            assert len(q_actions) == 4, f"[RLSolver][solve(model)] q_actions length is {len(q_actions)}"

            action = np.argmax(q_actions)

            (x, y) = self.curr_cell
            if action == 0: self.curr_cell = (x-1, y)       # North
            elif action == 1: self.curr_cell = (x, y+1)     # East
            elif action == 2: self.curr_cell = (x+1, y)     # South
            else: self.curr_cell = (x, y-1)                 # West

        if self.curr_cell == self.end:
            print(f"Solved the maze successfully in {len(self.steps)} steps!")
        else:
            print(f"Surpassed the maximum allowed number of iterations ({max_iter}).")
        
    
class DFSHeuristic(MazeSolver):
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