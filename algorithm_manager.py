import pygame as pg
import a_star
import bfs
import dfs
import random
import time

class Algorithm_Manager:
    def __init__(self, maze_manager, state_manager, text, error_handler):
        self.maze_manager = maze_manager
        self.state_manager = state_manager
        self.text = text
        self.error_handler = error_handler

    #Gets a list of all border coords in the maze
    def get_border_coords(self):
        border_coords=[]
        for row in range(self.maze_manager.width):
            for col in range(self.maze_manager.height):
                if row == 0:
                    border_coords.append((col,row))
                elif col == 0:
                    border_coords.append((col,row))
                elif row == row-1:
                    border_coords.append((col,row))
                elif row == col-1:
                    border_coords.append((col,row))
        return border_coords
    
    #Get mouse position relative to the maze coords
    def get_mouse_position(self, relative_to_grid:bool):
        x,y = pg.mouse.get_pos()
        
        #Calculates the x and y coords relative to the zoom and offset positions
        scale_width = self.state_manager.screen_width/(self.state_manager.screen_width + self.state_manager.zoom_scale)
        scale_height = self.state_manager.screen_height/(self.state_manager.screen_height + self.state_manager.zoom_scale)

        x *= scale_width
        y *= scale_height

        x -= self.state_manager.zoom_offset_x * scale_width
        y -= self.state_manager.zoom_offset_y * scale_height

        if not relative_to_grid:
            return x,y
        else:
            x_remainder = x % self.state_manager.cell_width 
            y_remainder = y % self.state_manager.cell_height 

            x -= x_remainder
            y -= y_remainder  

            x = int(x/self.state_manager.cell_width)
            y = int(y/self.state_manager.cell_height)

            return y,x
    
    #Generate maze using maze class
    def generate_maze(self):
        self.maze_manager.create_empty_maze('1','o', self.state_manager.maze_width, self.state_manager.maze_height, False)
        border_coords = self.get_border_coords()
        random_point = border_coords[random.randrange(0, len(border_coords))]
        self.maze_manager.set_point(random_point)
        self.maze_manager.generate_maze(random_point)
        self.state_manager.maze_is_drawn = False
        self.state_manager.drawing_maze = self.maze_manager.state_manager.drawing_path
        

    #Using the A* class, generate the solution given a maze
    def a_star_path(self):
        if self.error_handler.check_algorithm_error():
            algorithm_start_time = time.time()
            self.state_manager.clear_path()

            self.text.handle_text('Loading ...', 'A* Algorithm Loading')

            a_star_manager = a_star.A_Star_Pathfidning(self.maze_manager.maze, 
                                                    self.state_manager.start, 
                                                    self.state_manager.stop, 
                                                    self.maze_manager.obstacle)
            self.state_manager.solution_path, self.state_manager.step_path = a_star_manager.find_path()

            algorithm_final_time = time.time() - algorithm_start_time
            self.text.handle_text(f'A* Algorithm Cached ({round(algorithm_final_time,6)} milliseconds)','A* Algorithm Successfully Ran')

    #Using the BFS algorithm, generate the solution given a maze
    def bfs_path(self):
        if self.error_handler.check_algorithm_error():
            algorithm_start_time = time.time()
            self.state_manager.clear_path()

            self.text.handle_text('Loading ...', 'BFS Algorithm Loading')

            bfs_manager = bfs.BFS_Pathfinding(self.maze_manager.maze, 
                                            self.state_manager.start, 
                                            self.state_manager.stop, 
                                            self.maze_manager.cell)
            
            self.state_manager.solution_path, self.state_manager.step_path = bfs_manager.find_path()
            algorithm_final_time = time.time() - algorithm_start_time
            self.text.handle_text(f'BFS Algorithm Cached ({round(algorithm_final_time,6)} milliseconds)','BFS Algorithm Successfully Ran')

    #Using the DFS algorithm, generate the solution given a maze
    def dfs_path(self):
        if self.error_handler.check_algorithm_error():
            algorithm_start_time = time.time()
            self.state_manager.clear_path()

            self.text.handle_text('Loading ...', 'DFS Algorithm Loading')

            dfs_manager = dfs.DFS_Pathfinding(self.maze_manager.maze, 
                                            self.state_manager.start, 
                                            self.state_manager.stop, 
                                            self.maze_manager.cell)
            
            self.state_manager.solution_path, self.state_manager.step_path = dfs_manager.find_path()
            algorithm_final_time = time.time() - algorithm_start_time
            self.text.handle_text(f'DFS Algorithm Cached ({round(algorithm_final_time,6)} milliseconds)','DFS Algorithm Successfully Ran')

    #Create blank maze
    def create_blank_maze(self):
        self.maze_manager.create_empty_maze('1','o', self.state_manager.maze_width, self.state_manager.maze_height, True)

    #Clamp to a certain value
    def clamp(self, value:float, low_end:float, high_end:float):
        if value < low_end:
            value = low_end
        elif value > high_end:
            value = high_end
        return value
    
    #Calculate the delay given their positions
    def calculate_delay(self, name:str):
        if name == 'maze':
            x_value = self.state_manager.maze_circle_x
            denominator = self.state_manager.maze_circle_start_x - self.state_manager.maze_slider_width - 5
        elif name == 'step_path':
            x_value = self.state_manager.step_path_circle_x
            denominator = self.state_manager.step_path_circle_start_x

        if x_value % denominator == 0:
            match name:
                case 'maze':
                    self.state_manager.maze_delay = 40
                case 'step_path':
                    self.state_manager.step_delay = 40
        elif x_value % denominator == 20:
            match name:
                case 'maze':
                    self.state_manager.maze_delay = 20
                case 'step_path':
                    self.state_manager.step_delay = 20
        elif x_value % denominator == 40:
            match name:
                case 'maze':
                    self.state_manager.maze_delay = 5
                case 'step_path':
                    self.state_manager.step_delay = 10
        elif x_value % denominator == 60:
            match name:
                case 'maze':
                    self.state_manager.maze_delay = 0
                case 'step_path':
                    self.state_manager.step_delay = 5
        elif x_value % denominator == 80:
            match name:
                case 'maze':
                    self.state_manager.maze_delay = -1
                case 'step_path':
                    self.state_manager.step_delay = -1
