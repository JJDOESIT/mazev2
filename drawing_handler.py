import pygame as pg


class Drawing_Handler:
    def __init__(self, state_manager:object, maze_manager:object, algorithm_manager:object, text:object):
        self.state_manager = state_manager
        self.maze_manager = maze_manager
        self.algorithm_manager = algorithm_manager
        self.text = text

    #Draw a blank maze
    def draw_blank_maze(self):
        self.state_manager.cell_width = self.state_manager.screen_width / self.state_manager.maze_width
        self.state_manager.cell_height = self.state_manager.screen_height / self.state_manager.maze_height

        for row in range(self.maze_manager.height):
            for col in range(self.maze_manager.width):
                wall = pg.Rect(col * self.state_manager.screen_width / self.state_manager.maze_width,
                               row * self.state_manager.screen_height / self.state_manager.maze_height,
                               self.state_manager.cell_width + 1, 
                               self.state_manager.cell_height + 1)
                if self.maze_manager.maze[row][col] == self.maze_manager.obstacle:
                    pg.draw.rect(self.state_manager.screen, (0,0,0), wall)
                else:
                    pg.draw.rect(self.state_manager.screen, (255,255,255), wall)
    
    #Draws maze in accordance with the delay
    def draw_maze(self):
        self.state_manager.screen.fill((0,0,0))
        self.state_manager.cell_width = self.state_manager.screen_width / self.state_manager.maze_width
        self.state_manager.cell_height = self.state_manager.screen_height / self.state_manager.maze_height
        
        #We are indexing the array, so we only draw part of it at a time
        for cell in self.state_manager.drawing_maze[:self.state_manager.drawing_maze_index]:

            #Get the current time in ticks since the start of program
            time_now = pg.time.get_ticks()
            
            #Create wall
            wall = pg.Rect(cell[1] * self.state_manager.screen_width / self.state_manager.maze_width,
                            cell[0] * self.state_manager.screen_height / self.state_manager.maze_height, 
                            self.state_manager.cell_width + 1, 
                            self.state_manager.cell_height + 1)
            pg.draw.rect(self.state_manager.screen, (255,255,255), wall)
            
            #If the current time minus the delay is greater than the last time, increament index and set last time to current time
            if time_now - self.state_manager.maze_delay > self.state_manager.draw_maze_last_time:
                self.state_manager.draw_maze_last_time = time_now
                self.state_manager.drawing_maze_index += 1
        
        #If the maze is finished drawing, set maze_is_drawn to True
        if self.state_manager.drawing_maze_index >= len(self.state_manager.drawing_maze):
            self.state_manager.maze_is_drawn = True

    #Based on mouse click, set the stop and stop points
    def place_endpoints(self, start_or_stop:str):
    
        x, y = self.algorithm_manager.get_mouse_position(True)
        if (self.maze_manager.maze[x][y] != self.maze_manager.obstacle):
            if start_or_stop == 'start':
                self.state_manager.start = (x,y)
            elif start_or_stop == 'stop':
                self.state_manager.stop = (x,y)
            
            self.text.handle_text('New Endpoint (Recache)', 'New Endpoint Placed (re-run algorithm)')
            self.state_manager.clear_path()

    #Draw walls
    def draw_walls(self):
        self.state_manager.clear_path()
        x, y = self.algorithm_manager.get_mouse_position(True)
        self.maze_manager.set_point((x, y), True)

    #Draw end goal
    def draw_stop(self):
            stop = pg.Rect(self.state_manager.stop[1] * self.state_manager.cell_width, 
                           self.state_manager.stop[0] * self.state_manager.cell_height, 
                           self.state_manager.cell_width + 1, 
                           self.state_manager.cell_height + 1)
            pg.draw.rect(self.state_manager.screen, (255,0,0), stop)

    #Draw start goal
    def draw_start(self):
            start = pg.Rect(self.state_manager.start[1] * self.state_manager.cell_width, 
                            self.state_manager.start[0] * self.state_manager.cell_height, 
                            self.state_manager.cell_width + 1, 
                            self.state_manager.cell_height + 1)
            pg.draw.rect(self.state_manager.screen, (0,255,0), start)

    #Draw the final solution
    def draw_solution(self):
        for point in self.state_manager.solution_path:
            solution_x = point[1]
            solution_y = point[0]

            if point != self.state_manager.start and point != self.state_manager.stop:
                solution_cell = pg.Rect(solution_x * self.state_manager.cell_width, 
                                        solution_y * self.state_manager.cell_height, 
                                        self.state_manager.cell_width + 1, 
                                        self.state_manager.cell_height + 1) 
              
                pg.draw.rect(self.state_manager.screen, (255, 200, 200), solution_cell)

     #Draw the step solution
    def draw_step_path(self):
        for point in self.state_manager.step_path[:self.state_manager.step_index]:
            if point['position'] != self.state_manager.start and point['position'] != self.state_manager.stop:
                step_cell = pg.Rect(point['position'][1] * self.state_manager.cell_width, 
                                        point['position'][0] * self.state_manager.cell_height, 
                                        self.state_manager.cell_width + 1, 
                                        self.state_manager.cell_height + 1)
                if point['type'] == 'parent':
                    pg.draw.rect(self.state_manager.screen, (0, 0, 255), step_cell)
                elif point['type'] == 'child':
                    pg.draw.rect(self.state_manager.screen, (100, 100, 200), step_cell)

    #Draw all messages in log
    def draw_log(self):

        #Console messages
        self.text.blit_text('console_title')
        for text in range(len(self.state_manager.console_log)):
            if text % 2 == 0:
                color = (80,0,0)
            else:
                color = (0,0,0)

            console_text = self.state_manager.console_log[text]
            self.text.create_text(console_text, console_text, 'body', color, (text*50) + self.state_manager.body_y_offset)
            self.text.blit_text(console_text)

        #Scrollbar
        if 150 + (len(self.state_manager.paginated_log) * 50) < self.state_manager.screen_height:
            sidebar_position = self.state_manager.body_y_offset + (len(self.state_manager.paginated_log) * 50)
        else:
            sidebar_position = self.state_manager.screen_height - 55

        sidebar_rect = pg.Rect(self.state_manager.screen_width - 20,sidebar_position, 10, 25)
        pg.draw.rect(self.state_manager.screen, (0,0,0), sidebar_rect)

    def draw_maze_slider(self):
        #If the user is sliding the maze generation speed slider
        if self.state_manager.dragging_maze_slider:
            x = self.algorithm_manager.get_mouse_position(False)[0]
    
            #If the users mouse is within the circle coords, change the coords of the circle
            if x <= self.state_manager.maze_circle_start_x - self.state_manager.maze_circle_size and x >= self.state_manager.maze_circle_start_x - self.state_manager.maze_slider_width + 5:
                self.state_manager.maze_circle_x = x - self.state_manager.maze_circle_size/2

            #If the user is still dragging the slider, but it not hovering over it
            if not self.state_manager.maze_circle.collidepoint(self.algorithm_manager.get_mouse_position(False)):
                x = self.algorithm_manager.get_mouse_position(False)[0] - self.state_manager.maze_circle_size / 2

                x_r = x % 20
                if x_r >= 10:
                    x += 20-x_r
                else:
                    x -= x_r
        
                x = self.algorithm_manager.clamp(x, 
                                                 self.state_manager.maze_circle_start_x - self.state_manager.maze_slider_width -5 , 
                                                 self.state_manager.maze_circle_start_x)
                self.state_manager.dragging_maze_slider = False
                self.state_manager.maze_circle_x = x

        #If the user is still hovering over the slider, but is not dragging it
        if not self.state_manager.dragging_maze_slider:
            x_r = self.state_manager.maze_circle_x % 20
            if x_r >= 10:
                self.state_manager.maze_circle_x += 20 - x_r
            else:
                self.state_manager.maze_circle_x -= x_r
            self.state_manager.maze_circle_x = self.algorithm_manager.clamp(self.state_manager.maze_circle_x, 
                                                                            self.state_manager.maze_circle_start_x - self.state_manager.maze_slider_width -5 , 
                                                                            self.state_manager.maze_circle_start_x)

        #Create the slider and circle, and blit them to the screen
        self.state_manager.maze_slider = pg.Rect((self.state_manager.screen_width // 2) - (self.state_manager.maze_slider_width + 5) // 2, 
                                                 self.state_manager.maze_circle_y, 
                                                 self.state_manager.maze_slider_width, 
                                                 self.state_manager.maze_circle_size)
        self.state_manager.maze_circle = pg.Rect(self.state_manager.maze_circle_x, 
                                                 self.state_manager.maze_circle_y, 
                                                 self.state_manager.maze_circle_size, 
                                                 self.state_manager.maze_circle_size)
        pg.draw.rect(self.state_manager.screen, (0,0,0), self.state_manager.maze_slider, border_radius = 50)
        pg.draw.rect(self.state_manager.screen, (0,0,255), self.state_manager.maze_circle, border_radius = 50)
        self.algorithm_manager.calculate_delay('maze')

    def draw_step_slider(self):
        #If the user is sliding the step path speed slider
        if self.state_manager.dragging_step_slider:
            x = self.algorithm_manager.get_mouse_position(False)[0]
            
            #If the users mouse is within the circle coords, change the coords of the circle
            if x >= self.state_manager.step_path_circle_start_x + self.state_manager.step_circle_size / 2 and x <= self.state_manager.step_path_circle_start_x + self.state_manager.step_path_slider_width - self.state_manager.step_circle_size // 2:
                self.state_manager.step_path_circle_x = x - self.state_manager.step_circle_size / 2

            #If the user is still dragging the slider, but is not hovering over it
            if not self.state_manager.step_path_circle.collidepoint(self.algorithm_manager.get_mouse_position(False)):
                x = self.algorithm_manager.get_mouse_position(False)[0] - self.state_manager.step_circle_size / 2
                
                x_r = x % 20
                if x_r >= 10:
                    x += 20-x_r
                else:
                    x -= x_r
                
                x = self.algorithm_manager.clamp(x, 
                                                 self.state_manager.step_path_circle_start_x, 
                                                 self.state_manager.step_path_circle_start_x + self.state_manager.step_path_slider_width +5 )
    
                self.state_manager.dragging_step_slider = False
                self.state_manager.step_path_circle_x = x

        #If the user is still hovering over the slider, but it not dragging it
        if not self.state_manager.dragging_step_slider:
            x_r = self.state_manager.step_path_circle_x%20
            if x_r >= 10:
                self.state_manager.step_path_circle_x += 20 - x_r
            else:
                self.state_manager.step_path_circle_x -= x_r
            self.state_manager.step_path_circle_x = self.algorithm_manager.clamp(self.state_manager.step_path_circle_x, 
                                                                                 self.state_manager.step_path_circle_start_x, 
                                                                                 self.state_manager.step_path_circle_start_x + self.state_manager.step_path_slider_width + 5)

        #Create the slider and circle, and blit them to the screen
        self.state_manager.step_path_slider = pg.Rect((self.state_manager.screen_width // 2) - (self.state_manager.step_path_slider_width + 5) // 2, 
                                                      self.state_manager.step_path_circle_y, 
                                                      self.state_manager.step_path_slider_width, 
                                                      self.state_manager.step_circle_size)
        self.state_manager.step_path_circle = pg.Rect(self.state_manager.step_path_circle_x, 
                                                      self.state_manager.step_path_circle_y, 
                                                      self.state_manager.step_circle_size, 
                                                      self.state_manager.step_circle_size)
        pg.draw.rect(self.state_manager.screen, (0,0,0), self.state_manager.step_path_slider, border_radius = 50)
        pg.draw.rect(self.state_manager.screen, (0,0,255), self.state_manager.step_path_circle, border_radius = 50)
        self.algorithm_manager.calculate_delay('step_path')

    #Admin sliders
    def admin_menu(self):
        self.draw_step_slider()
        self.draw_maze_slider()
        
        