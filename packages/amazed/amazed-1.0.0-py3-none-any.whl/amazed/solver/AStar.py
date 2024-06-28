from random import shuffle

from amazed.maze import Maze
from amazed.solver.Solver import Solver

class AStar(Solver):

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

