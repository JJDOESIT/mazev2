import boundaries
import random

class State_Manager:
    def __init__(self):
        self.stack = []
        self.visited = []
        self.drawing_path = []

class Maze:
    def __init__(self):
        pass

    #Create an empty maze
    def create_empty_maze(self, obstacle:str, cell:str, width:int, height:int, swap = False):
        self.obstacle=obstacle
        self.cell=cell

        self.width = width
        self.height = height

        #Set to true in order to create a blank canvas
        if swap:
            self.obstacle = cell
            self.cell = obstacle
            
        maze=[]
        for row in range(height):
            maze.append([])
            for col in range(width):
                maze[row].append(obstacle)

        self.maze = maze
        self.boundary_manager = boundaries.Boundaries(self.maze, self.obstacle)

    #Prints maze in the console
    def print_array_maze(self):
        for row in range(self.height):
            for col in range(self.width):
                print(self.maze[row][col], end = '')
            print('')

    #Set an obstacle or cell in the maze depending on swap value
    def set_point(self, point:tuple, swap=False):
        x = point[0]
        y = point[1]
        
        #Set swap equal to true in order to create a blank maze
        if swap:
            self.maze[x][y] = self.obstacle
        else:
            self.maze[x][y] = self.cell

    #Generate random maze (Recursive)
    """def generate_maze(self, position:tuple):
 
        moves=self.boundary_manager.get_possible_moves(position)
        moves=self.boundary_manager.check_connected_cells(moves, self.cell)
        while len(moves) > 0:
            move = moves.pop(random.randrange(0, len(moves)))
            move = self.boundary_manager.check_connected_cells([move], self.cell)
            if len(move) > 0:
                move = move[0]
                self.set_point(move)
                self.generate_maze(move) """
    
    #Generate random maze (stack)
    def generate_maze(self, position:tuple):
        self.state_manager = State_Manager()

        self.state_manager.stack.append(position)
        self.state_manager.drawing_path.append(position)

        #While the stack is not empty, keep running
        while self.state_manager.stack:

            #Get a node off the stack
            node = self.state_manager.stack.pop(random.randint(0, len(self.state_manager.stack) - 1))

            #Check and see if the node is connected to only 1 cell (the one before it)
            valid_move = self.boundary_manager.check_connected_cells([node], self.cell)
            if valid_move:
                valid_move = valid_move.pop()

                if valid_move not in self.state_manager.visited:
                    self.state_manager.drawing_path.append(valid_move)

                self.set_point(valid_move)
                self.state_manager.visited.append(valid_move)
            
            #Get possible moves from the node
            moves = self.boundary_manager.get_possible_moves(node)
            valid_moves=self.boundary_manager.check_connected_cells(moves, self.cell)

            #Add the possible moves to the stack
            for move in valid_moves:
                self.state_manager.stack.append(move)
        
        




