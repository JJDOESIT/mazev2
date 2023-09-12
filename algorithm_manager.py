import pygame as pg
import a_star
import bfs
import dfs
import random

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
                if row==0:
                    border_coords.append((col,row))
                elif col==0:
                    border_coords.append((col,row))
                elif row==row-1:
                    border_coords.append((col,row))
                elif row==col-1:
                    border_coords.append((col,row))
        return border_coords
    
    #Get mouse position relative to the maze coords
    def get_mouse_position(self):
        x,y = pg.mouse.get_pos()
        
        x_remainder = x%self.state_manager.cell_width
        y_remainder = y%self.state_manager.cell_height

        x -= x_remainder
        y -= y_remainder

        x = int(x//self.state_manager.cell_width)
        y = int(y//self.state_manager.cell_height)

        return y,x
    
    #Generate maze using maze class
    def generate_maze(self):
        self.maze_manager.create_empty_maze('1','o', self.state_manager.maze_width, self.state_manager.maze_height, False)
        border_coords = self.get_border_coords()
        random_point = border_coords[random.randrange(0, len(border_coords))]
        self.maze_manager.set_point(random_point)
        self.maze_manager.generate_maze(random_point)

    #Using the A* class, generate the solution given a maze
    def a_star_path(self):    
        if self.error_handler.check_algorithm_error():
            self.state_manager.clear_path()
            self.text.handle_text('A* Algorithm Cached','A* Algorithm Successfully Ran', self.state_manager)
            a_star_manager = a_star.A_Star_Pathfidning(self.maze_manager.maze, 
                                                    self.state_manager.start, 
                                                    self.state_manager.stop, 
                                                    self.maze_manager.obstacle)
            self.state_manager.solution_path, self.state_manager.step_path = a_star_manager.find_path()

    #Using the BFS algorithm, generate the solution given a maze
    def bfs_path(self):
        if self.error_handler.check_algorithm_error():
            self.state_manager.clear_path()
            self.text.handle_text('BFS Algorithm Cached','BFS Algorithm Successfully Ran', self.state_manager)
            bfs_manager = bfs.BFS_Pathfinding(self.maze_manager.maze, 
                                            self.state_manager.start, 
                                            self.state_manager.stop, 
                                            self.maze_manager.cell)
            
            self.state_manager.solution_path, self.state_manager.step_path = bfs_manager.find_path()

    #Using the DFS algorithm, generate the solution given a maze
    def dfs_path(self):
        if self.error_handler.check_algorithm_error():
            self.state_manager.clear_path()
            self.text.handle_text('DFS Algorithm Cached','DFS Algorithm Successfully Ran', self.state_manager)
            dfs_manager = dfs.DFS_Pathfinding(self.maze_manager.maze, 
                                            self.state_manager.start, 
                                            self.state_manager.stop, 
                                            self.maze_manager.cell)
            
            self.state_manager.solution_path, self.state_manager.step_path = dfs_manager.find_path()


    #Create blank maze
    def create_blank_maze(self):
        self.maze_manager.create_empty_maze('1','o', self.state_manager.maze_width, self.state_manager.maze_height, True)