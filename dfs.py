import boundaries

class State_Manager:
    def __init__(self):
        self.stack = []
        self.visited = []
        self.path = {}
        self.drawing_path = []

class DFS_Pathfinding:
    def __init__(self, maze, start:tuple, stop:tuple, obstacle:str):
        self.maze = maze
        self.start = start
        self.stop = stop
        self.obstacle = obstacle

    #Backtrack and find final solution
    def backtrack(self):
        path = []

        temp_node = self.state_manager.path[self.stop]
        path.append(self.stop)

        while temp_node!=self.start:
            path.append(temp_node)
            temp_node = self.state_manager.path[temp_node]
        path.append(temp_node)

        return self.boundary_manager.reverse_path(path)

    #Main algorithm
    def find_path(self):
        self.state_manager = State_Manager()
        self.boundary_manager = boundaries.Boundaries(self.maze, self.obstacle)

        self.state_manager.stack.append(self.start)

        while self.state_manager.stack:

            #Remove node from stack
            node = self.state_manager.stack.pop()
            self.state_manager.visited.append(node)
            self.state_manager.drawing_path.append({'type':'parent','position':node})

            #Check end condition
            if node == self.stop:
                path = self.backtrack()
                return path, self.state_manager.drawing_path

            moves = self.boundary_manager.get_possible_moves(node)

            for move in moves:
                if move not in self.state_manager.visited:
                    self.state_manager.stack.append(move)
                    self.state_manager.path[move] = node
                    self.state_manager.drawing_path.append({'type':'child','position':move})

        return [], self.state_manager.drawing_path


