import pygame as pg

class State_Manager:
    def __init__(self, screen_width:float, screen_height:float):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.zoom_scale = 0
        self.zoom_offset_x = 0
        self.zoom_offset_y = 0

        self.screen = None
        self.picture = None

        self.running = True

        self.start = None
        self.stop=None

        self.maze_width = 20
        self.maze_height = 20

        self.path=[]

        self.draw_maze = False
        self.draw_end = False
        self.draw_start = False
        self.draw_path = False
        self.draw_error = False
        self.draw_help = True
        self.draw_menu = False
        self.draw_solution_path = False
        self.draw_step_path = False
        self.draw_blank_maze = False
        self.draw_log = False

        self.maze_is_drawn = False

        self.turn = 0

        self.start = None
        self.stop = None

        self.solution_path = []
        self.step_path = []
        self.step_index = 1
        self.step_delay = 40

        self.temp_width = ''
        self.temp_height = ''

        self.arrow_y = 0

        self.title_y_offset = 50
        self.body_y_offset = 100

        self.console_log = []
        self.paginated_log = []

        self.drawing_maze = []
        self.drawing_maze_index = 1
        self.maze_delay = -1

        self.dragging_step_slider = False
        self.step_path_slider_width = 95
        self.step_circle_size = 15
        self.step_path_circle_start_x = (self.screen_width // 2) - ((self.step_path_slider_width + 5 ) // 2)
        self.step_path_circle_x = self.step_path_circle_start_x
        self.step_path_circle_y = 270

        self.dragging_maze_slider = False
        self.maze_slider_width = 95
        self.maze_circle_size = 15
        self.maze_circle_start_x = (self.screen_width // 2) + ((self.maze_slider_width + 5) // 2)
        self.maze_circle_x = self.maze_circle_start_x - self.maze_circle_size
        self.maze_circle_y = 350
        
    #Clear everything on the screen except whatever is excluded
    def hide_all_except(self, exclude:list):
        if 'draw_maze' not in exclude:
            self.draw_maze = False
        if 'draw_help' not in exclude:
            self.draw_help = False
        if 'draw_menu' not in exclude:
            self.draw_menu = False
        if 'draw_solution_path' not in exclude:
            self.draw_solution_path = False
            self.solution_path = []
        if 'draw_step_path' not in exclude:
            self.draw_step_path = False
            self.step_path = []
            self.temp_step_path = []
            self.step_count = 0
        if 'draw_blank_maze' not in exclude:
            self.draw_blank_maze = False
        if 'console_log' not in exclude:
            self.draw_log = False

        #Reset the drawing index back to 1
        self.drawing_maze_index = 1

        #Remove start and stop positions
        self.start = None
        self.stop = None

    #Clear path
    def clear_path(self):
        self.solution_path = []
        self.step_path = []
        self.temp_step_path = []
        self.step_count = 0
        self.draw_solution_path = False
        self.draw_step_path = False
        self.step_index = 1

    #Clears the console log page
    def clear_console_log(self):
        self.console_log = []
        self.paginated_log = []