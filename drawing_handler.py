import pygame as pg


class Drawing_Handler:
    def __init__(self, state_manager, maze_manager, algorithm_manager, text):
        self.state_manager = state_manager
        self.maze_manager = maze_manager
        self.algorithm_manager = algorithm_manager
        self.text = text

    #Draw maze to correct dimensions
    def draw_maze(self):
        self.state_manager.cell_width = self.state_manager.screen_width/self.state_manager.maze_width
        self.state_manager.cell_height = self.state_manager.screen_height/self.state_manager.maze_height
        for row in range(self.maze_manager.height):
            for col in range(self.maze_manager.width):
                wall = pg.Rect(col*self.state_manager.screen_width/self.state_manager.maze_width, 
                               row*self.state_manager.screen_height/self.state_manager.maze_height, 
                               self.state_manager.cell_width, self.state_manager.cell_height)
                if self.maze_manager.maze[row][col] == self.maze_manager.obstacle:
                    pg.draw.rect(self.state_manager.screen, (0,0,0), wall)
                else:
                    pg.draw.rect(self.state_manager.screen, (255,255,255), wall, border_radius=0)

    #Based on mouse click, set the stop and stop points
    def place_endpoints(self, start_or_stop):
        x,y = self.algorithm_manager.get_mouse_position()

        if (self.maze_manager.maze[x][y]!=self.maze_manager.obstacle):
            if start_or_stop == 'start':
                self.state_manager.start = (x,y)
            elif start_or_stop == 'stop':
                self.state_manager.stop = (x,y)
            self.text.handle_text('New Endpoint (Recache)', 'New Endpoint Placed (re-run algorithm)', self.state_manager)
            self.state_manager.clear_path()

    #Draw walls
    def draw_walls(self):
        self.state_manager.clear_path()
        x,y = self.algorithm_manager.get_mouse_position()
        self.maze_manager.set_point((x,y), True)

    #Draw end goal
    def draw_stop(self):
            stop = pg.Rect(self.state_manager.stop[1]*self.state_manager.cell_width, 
                           self.state_manager.stop[0]*self.state_manager.cell_height, 
                           self.state_manager.cell_width, 
                           self.state_manager.cell_height)
            pg.draw.rect(self.state_manager.screen, (255,0,0), stop)

    #Draw start goal
    def draw_start(self):
            start = pg.Rect(self.state_manager.start[1]*self.state_manager.cell_width, 
                            self.state_manager.start[0]*self.state_manager.cell_height, 
                            self.state_manager.cell_width, 
                            self.state_manager.cell_height)
            pg.draw.rect(self.state_manager.screen, (0,255,0), start)

    #Draw the final solution
    def draw_solution(self):
        for point in self.state_manager.solution_path:
            solution_x = point[1]
            solution_y = point[0]

            if point!=self.state_manager.start and point!=self.state_manager.stop:
                solution_cell = pg.Rect(solution_x*self.state_manager.cell_width, 
                                        solution_y*self.state_manager.cell_height, 
                                        self.state_manager.cell_width, 
                                        self.state_manager.cell_height) 
              
                pg.draw.rect(self.state_manager.screen, (255, 200, 200), solution_cell)

     #Draw the step solution
    def draw_step_path(self):
        for point in self.state_manager.temp_step_path:
            if point['position']!=self.state_manager.start and point['position']!=self.state_manager.stop:
                step_cell = pg.Rect(point['position'][1]*self.state_manager.cell_width, 
                                        point['position'][0]*self.state_manager.cell_height, 
                                        self.state_manager.cell_width, 
                                        self.state_manager.cell_height)
                if point['type'] == 'parent':
                    pg.draw.rect(self.state_manager.screen, (0, 0, 255), step_cell)
                elif point['type'] == 'child':
                    pg.draw.rect(self.state_manager.screen, (100, 100, 200), step_cell)

    #Draw all messages in log
    def draw_log(self):
        #Console messages
        self.state_manager.screen.blit(self.text.stored_text['console_title'][0], self.text.stored_text['console_title'][1])
        for text in range(len(self.state_manager.console_log)):
            if text%2==0:
                color = (80,0,0)
            else:
                color = (0,0,0)
            console_text = self.state_manager.console_log[text]
            self.text.create_text(console_text, console_text, (self.state_manager.screen_width//2, (text*50)+100), 25, False, color, (0,0))
            self.state_manager.screen.blit(self.text.stored_text[console_text][0], self.text.stored_text[console_text][1])
   
        #Scrollbar
        if 100+(len(self.state_manager.paginated_log)*50) < self.state_manager.screen_height:
            sidebar_position = 95+(len(self.state_manager.paginated_log)*50)
        else:
            sidebar_position = self.state_manager.screen_height -55

        sidebar_rect = pg.Rect(self.state_manager.screen_width-20,sidebar_position, 10, 25)
        pg.draw.rect(self.state_manager.screen, (0,0,0), sidebar_rect)