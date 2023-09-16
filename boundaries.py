class Boundaries:
    def __init__(self, maze:list, obstacle:str):
        self.maze = maze
        self.width = len(maze)
        self.height = len(maze[0])
        self.obstacle = obstacle

    #Catches out of bounds error
    def check_if_valid(self, position:tuple):
        return (position[0] >= 0 and position[0] < self.width and position[1] >= 0 and position[1] < self.height)

    #Gets neighbors in A* algorithm
    def get_neighbors(self, node:object, closed_list:list):
        neighbors = []

        x = node.position[0]
        y = node.position[1]

        possible_moves = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]

        for move in possible_moves:
            if (self.check_if_valid(move) and move not in closed_list):
                if (self.maze[move[0]][move[1]] != self.obstacle):
                    neighbors.append(move)
        return neighbors
    
    #Gets possible moves (U/R/L/D) in an array
    def get_possible_moves(self, point:tuple):
        moves=[]

        x = point[0]
        y = point[1]

        possible_moves = [(x - 1, y), (x, y - 1),(x, y + 1),(x + 1, y)]

        for move in possible_moves:
            if (self.check_if_valid(move)):
                if (self.maze[move[0]][move[1]] == self.obstacle):
                    moves.append(move)
        return moves
    
    #For each move in list, check if it will be connected to only one cell
    def check_connected_cells(self, moves:list, cell:str):
        valid_moves=[]

        for move in moves:
            connected_count = 0
            x = move[0]
            y = move[1]
            possible_moves = [(x ,y + 1), (x , y - 1), (x + 1, y), (x - 1, y)]
            for future_move in possible_moves:
                if (self.check_if_valid(future_move)):
                    future_x = future_move[0]
                    future_y = future_move[1]
                    if self.maze[future_x][future_y] == cell:
                        connected_count += 1
            if connected_count == 1:
                valid_moves.append(move)
        return valid_moves
    
    #Reverse an array
    def reverse_path(self, path:list):
        start_index = 0
        end_index = len(path) - 1
        while (start_index < end_index / 2):
            path[start_index], path[end_index] = path[end_index], path[start_index]
            start_index += 1
            end_index -= 1
        return path