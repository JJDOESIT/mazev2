class State_Manager:
    def __init__(self):
        self.screen_width = 500
        self.screen_height = 500

        self.screen = None

        self.running=True

        self.start=None
        self.stop=None

        self.maze_width = 20
        self.maze_height = 20

        self.path=[]

        self.draw_maze=False
        self.draw_end=False
        self.draw_start=False
        self.draw_path=False
        self.draw_error=False
        self.draw_help = True
        self.draw_menu = False
        self.draw_solution_path = False
        self.draw_step_path = False
        self.draw_blank_maze = False
        self.draw_log = False

        self.turn = 0

        self.start = None
        self.stop = None

        self.solution_path = []
        self.step_path = []
        self.temp_step_path = []
        self.step_count = 0

        self.temp_width = ''
        self.temp_height = ''

        self.arrow_y = 172

        self.console_log = []
        self.paginated_log = []

    #Clear everything on the screen except whatever is excluded
    def hide_all_except(self, exclude):
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

    #Clears the console log page
    def clear_console_log(self):
        self.console_log = []
        self.paginated_log = []