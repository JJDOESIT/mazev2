import pygame as pg

class Event_Handler():
    def __init__(self, state_manager:object, text:object, algorithm_manager:object, error_handler:object, drawing_handler:object):
        self.state_manager = state_manager
        self.text = text
        self.algorithm_manager = algorithm_manager
        self.error_handler = error_handler
        self.drawing_handler = drawing_handler

    #Handle all single click events
    def handle_input(self, event_queue:list):
        for event in event_queue:
            if event.type == pg.QUIT:
                self.state_manager.running = False

            if event.type == pg.KEYUP:

                #Help menu
                if event.key == pg.K_h:
                    self.text.handle_text('Help Menu', 'Help Menu Page Visited')
                    self.state_manager.draw_help = True
                    self.state_manager.hide_all_except(['draw_help'])

                #Admin menu
                if event.key == pg.K_LCTRL:
                    self.text.handle_text('Admin Panel', 'Admin Panel Page Visited')
                    self.state_manager.draw_menu = True
                    self.state_manager.hide_all_except(['draw_menu'])
                
                #Maze generation
                if event.key == pg.K_g:
                    self.text.handle_text('New Maze', 'Random Maze Generated')
                    self.state_manager.hide_all_except(['draw_maze'])
                    self.algorithm_manager.generate_maze()
                    
                    self.state_manager.draw_maze = True

                #Make custom maze
                if event.key == pg.K_m:
                    self.text.handle_text('Draw Maze', 'Draw Maze Page Visited')
                    self.algorithm_manager.create_blank_maze()
                    self.state_manager.hide_all_except(['draw_blank_maze'])

                    self.state_manager.draw_blank_maze = True
                
                #A*
                if event.key == pg.K_a:
                    self.algorithm_manager.a_star_path()

                #BFS
                if event.key == pg.K_b:
                    self.algorithm_manager.bfs_path()

                #DFS
                if event.key == pg.K_d:
                    self.algorithm_manager.dfs_path()

                #Solution path
                if event.key == pg.K_p:
                    if self.error_handler.check_for_errors():
                        if not self.state_manager.solution_path:
                            self.text.handle_text('No Solution Path', 'Error: No Solution Has Been Found')
                        else:
                            self.text.handle_text('Solution Path', 'Solution Path Drawn')
                            self.state_manager.draw_solution_path = True 
                
                #Clear paths
                if event.key == pg.K_c:
                    if self.state_manager.draw_maze or self.state_manager.draw_blank_maze:
                        self.text.handle_text('Path Cleared', 'Paths Have Been Cleared')
                        self.state_manager.clear_path()
                    elif self.state_manager.draw_log:
                        self.state_manager.clear_console_log()

                #Console log
                if event.key == pg.K_l:
                    self.text.handle_text('Console Log', 'Console Page Visited')
                    self.state_manager.hide_all_except(['console_log'])
                    self.state_manager.draw_log = True

                #Move console log down
                if event.key == pg.K_DOWN:
                    if self.state_manager.draw_log:
                        self.move_page_down()

                #Move console log up
                if event.key == pg.K_UP:
                    if self.state_manager.draw_log:
                        self.move_page_up()

                #Zoom
                if event.key == pg.K_z:
                    self.handle_zoom()

                #Key inputs for admin menu
                if self.state_manager.draw_menu:
                    if event.key == pg.K_0:
                        self.handle_user_input(0)
                    if event.key == pg.K_1:
                        self.handle_user_input(1)
                    if event.key == pg.K_2:
                        self.handle_user_input(2)
                    if event.key == pg.K_3:
                        self.handle_user_input(3)
                    if event.key == pg.K_4:
                        self.handle_user_input(4)
                    if event.key == pg.K_5:
                        self.handle_user_input(5)
                    if event.key == pg.K_6:
                        self.handle_user_input(6)
                    if event.key == pg.K_7:
                        self.handle_user_input(7)
                    if event.key == pg.K_8:
                        self.handle_user_input(8)
                    if event.key == pg.K_9:
                        self.handle_user_input(9)
                    if event.key == pg.K_RETURN:
                        self.switch_turn()  

            if event.type == pg.MOUSEBUTTONUP:
                if (self.state_manager.draw_maze or self.state_manager.draw_blank_maze) and self.state_manager.maze_is_drawn:

                    #Place start (left click)
                    if event.button == 1 and (self.state_manager.draw_maze or self.state_manager.draw_blank_maze): 
                        self.drawing_handler.place_endpoints('start')

                    #Place end (right click)
                    if event.button == 3 and (self.state_manager.draw_maze or self.state_manager.draw_blank_maze): 
                        self.drawing_handler.place_endpoints('stop')

                #Set dragging to false
                if self.state_manager.draw_menu:
                    self.state_manager.dragging_step_slider = False
                    self.state_manager.dragging_maze_slider = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if self.state_manager.draw_menu:

                    #Step path speed slider
                    if self.state_manager.step_path_circle.collidepoint(self.algorithm_manager.get_mouse_position(False)):
                        self.state_manager.dragging_step_slider = True

                    #Maze speed slider
                    if self.state_manager.maze_circle.collidepoint(self.algorithm_manager.get_mouse_position(False)):
                        self.state_manager.dragging_maze_slider = True

    #Zoom the screen by a factor of 100 pixels
    def handle_zoom(self):
        if (self.state_manager.zoom_scale) < 500:
            self.state_manager.zoom_scale += 100
        else:
            self.state_manager.zoom_offset_x = 0
            self.state_manager.zoom_offset_y = 0
            self.state_manager.zoom_scale = 0
                        
    #Handles user input within the admin panel to switch between width and height
    def handle_user_input(self, key_number:int):
        if self.state_manager.turn == 0:
            self.state_manager.temp_width += str(key_number)
            self.state_manager.maze_width = int(self.state_manager.temp_width)
        else:
            self.state_manager.temp_height += str(key_number)
            self.state_manager.maze_height = int(self.state_manager.temp_height)
        
    #Move the console page up
    def move_page_up(self):
        if self.state_manager.paginated_log:
            self.state_manager.console_log.insert(0, self.state_manager.paginated_log.pop(0))

    #Move the console page down
    def move_page_down(self):
        if len(self.state_manager.console_log) > 10:
            self.state_manager.paginated_log.append(self.state_manager.console_log.pop(0))

    #When return is pressed, switch between width and height
    def switch_turn(self):
        if self.state_manager.draw_menu:
            if self.state_manager.turn == 0:
                try:
                    if int(self.state_manager.temp_width) >= 150:
                        self.state_manager.maze_width = 150
                    elif int(self.state_manager.temp_width) <= 2:
                        self.state_manager.maze_width = 2
                    else:
                        self.state_manager.maze_width = int(self.state_manager.temp_width)
                except:
                    print('Skip')
                self.state_manager.turn += 1
                self.state_manager.temp_width = ''
                self.state_manager.arrow_y += 20
            else:
                try:
                    if int(self.state_manager.temp_height) >= 150:
                        self.state_manager.maze_height = 150
                    elif int(self.state_manager.temp_height) <= 2:
                        self.state_manager.maze_height = 2
                    else:
                        self.state_manager.maze_height = int(self.state_manager.temp_height)
                except:
                    print('Skip')
                self.state_manager.turn -= 1
                self.state_manager.temp_height = ''
                self.state_manager.arrow_y -= 20

    #When right shift is pressed, increament the step path
    def handle_key_strokes(self, key_queue:list):
        time_now = pg.time.get_ticks()

        #Step path
        keys = key_queue

        if keys[pg.K_RSHIFT]:
            if time_now - self.state_manager.step_path_last_time > self.state_manager.step_delay:
                if self.error_handler.check_for_errors():
                    self.text.handle_text('Step Path', 'Step Path Drawn')
                    self.state_manager.draw_step_path = True

                    #Adjust the step path speed accordingly
                    if self.state_manager.step_delay == -1:
                        step_increament = 10
                    elif self.state_manager.step_delay == 5:
                        step_increament = 2
                    else:
                        step_increament = 1

                    self.state_manager.step_index += step_increament
                    self.state_manager.step_path_last_time = time_now

        #Draw walls
        if keys[pg.K_LSHIFT]:
            if self.state_manager.draw_blank_maze:
                self.drawing_handler.draw_walls()

        #Zoom offset
        if self.state_manager.zoom_scale > 0:
            if keys[pg.K_RIGHT]:
                if self.state_manager.screen_width + self.state_manager.zoom_scale + self.state_manager.zoom_offset_x > self.state_manager.screen_width:
                    self.state_manager.zoom_offset_x -= 1
            if keys[pg.K_UP]:
                if self.state_manager.zoom_offset_y < 0:
                    self.state_manager.zoom_offset_y += 1
            if keys[pg.K_LEFT]:
                if self.state_manager.zoom_offset_x < 0:
                    self.state_manager.zoom_offset_x += 1
            if keys[pg.K_DOWN]:
                if self.state_manager.screen_height + self.state_manager.zoom_scale + self.state_manager.zoom_offset_y > self.state_manager.screen_height:
                    self.state_manager.zoom_offset_y -= 1
    