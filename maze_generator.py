import boundaries
import random

class Maze:
    def __init__(self):
        pass

    #Create an empty maze
    def create_empty_maze(self, obstacle, cell, width, height, swap=False):
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

        self.maze=maze
        self.boundary_manager=boundaries.Boundaries(self.maze, self.obstacle)

    #Prints maze in the console
    def print_array_maze(self):
        for row in range(self.height):
            for col in range(self.width):
                print(self.maze[row][col], end='')
            print('')

    #Set an obstacle or cell in the maze depending on swap value
    def set_point(self, point:tuple, swap=False):
        x = point[0]
        y = point[1]
        
        #Set swap equal to true in order to create a blank maze
        if swap:
            self.maze[x][y]=self.obstacle
        else:
            self.maze[x][y]=self.cell

    #Generate random maze
    def generate_maze(self, position):
 
        moves=self.boundary_manager.get_possible_moves(position)
        moves=self.boundary_manager.check_connected_cells(moves, self.cell)
        while len(moves) > 0:
            move = moves.pop(random.randrange(0, len(moves)))
            move = self.boundary_manager.check_connected_cells([move], self.cell)
            if len(move) > 0:
                move = move[0]
                self.set_point(move)
                self.generate_maze(move)




