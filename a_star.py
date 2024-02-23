import boundaries

class State_Manager:
    def __init__(self):
        self.open_list = []
        self.closed_list = []
        self.path = []
        self.drawing_path = []

class Node:
    def __init__(self, parent:object = None, position:tuple = None, end_goal:tuple = None):
        self.parent = parent
        self.position = position

        self.h = self.get_euclidean_distance(end_goal)
        self.g = 0
        self.f = 0

    #Gets euclidean distance based on the current node and end node
    def get_euclidean_distance(self, end_position:tuple):
        x_length = abs(end_position[0] - self.position[0])
        y_length = abs(end_position[1] - self.position[1])

        return ((x_length ** 2) + (y_length ** 2))
    
    #Determines whether the child node is in the list, and if we need to swap it's value 
    def evaluate_child_nodes(self, open_list_node:object):
        in_list = False
        swap_values = False
        if (self.position == open_list_node.position):
            in_list = True
            if (self.g < open_list_node.g):
                swap_values = True
        return in_list, swap_values

class A_Star_Pathfidning:
    def __init__(self, maze:list, start:tuple, stop:tuple, obstacle:str):
        self.maze = maze
        self.start = start
        self.stop = stop
        self.obstacle = obstacle

    #Creates a path based on backtracking parent nodes
    def backtrack(self, end_node:object, state_manager:object):
        temp_node = end_node
        
        while temp_node.position != self.start:
            state_manager.path.append(temp_node.position)
            temp_node = temp_node.parent
        state_manager.path.append(temp_node.position)
        return self.boundary_manager.reverse_path(state_manager.path)
    
    def find_path(self):
        state_manager = State_Manager()
        
        self.boundary_manager = boundaries.Boundaries(self.maze, self.obstacle)

        start_node = Node(position = self.start, end_goal = self.stop)
        state_manager.open_list.append(start_node)

        while (len(state_manager.open_list) > 0):

            #Get current node based on lowest f score. If equal, resort to lowest h score. 
            count=0
            current_node_index=0
            current_node = state_manager.open_list[count]
            for node in state_manager.open_list:
                if node.f < current_node.f:
                    current_node = node
                    current_node_index = count
                elif node.h < current_node.h:
                    current_node = node
                    current_node_index = count
                count += 1

            #Remove the current node from the open list and add it to the closed list
            state_manager.open_list.pop(current_node_index)
            state_manager.closed_list.append(current_node.position)
            state_manager.drawing_path.append({'type':'parent','position':current_node.position})

            #Check end condition
            if current_node.position == self.stop:
                path = self.backtrack(current_node, state_manager)
                return path, state_manager.drawing_path

            #Get available adjacent moves
            neighbors = self.boundary_manager.get_neighbors(current_node, state_manager.closed_list)

            #Only add node to open list if it's not already in there
            add_to_open_list = True

            #Create a new node for all neighbors
            for neighbor in neighbors:
                neighbor_node = Node(parent=current_node, position=neighbor, end_goal=self.stop)
                neighbor_node.g = current_node.g + 1
                neighbor_node.f = neighbor_node.g+neighbor_node.h

                #Loop throguh all nodes in the open list
                for open_node in state_manager.open_list:

                    #Check if neighbor node is in open list, and if we need to swap the g values
                    in_list, swap_values = neighbor_node.evaluate_child_nodes(open_node)
                    if in_list:
                        add_to_open_list = False
                        if swap_values:
                            open_node.g = neighbor_node.g
                            open_node.f = open_node.g + open_node.h

                if add_to_open_list:
                    state_manager.open_list.append(neighbor_node)
                    state_manager.drawing_path.append({'type':'child','position':neighbor_node.position})
        return [], state_manager.drawing_path

