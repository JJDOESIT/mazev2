import pygame as pg
import pygame.freetype
import state_manager
import text
import event_handler
import maze_generator
import background
import algorithm_manager
import error_handler
import drawing_handler

class Engine:
    def __init__(self, screen_width, screen_height):
        self.state_manager = state_manager.State_Manager(screen_width, screen_height)
        
        self.state_manager.screen = pg.display.set_mode((screen_width, screen_height))

        self.text = text.Text(self.state_manager)

        self.maze_manager = maze_generator.Maze()

        self.error_handler = error_handler.Error_Handler(self.state_manager, self.text)

        self.algorithm_manager = algorithm_manager.Algorithm_Manager(self.maze_manager, self.state_manager, self.text, self.error_handler)

        self.drawing_handler = drawing_handler.Drawing_Handler(self.state_manager, self.maze_manager, self.algorithm_manager, self.text)

        self.event_handler = event_handler.Event_Handler(self.state_manager, self.text, self.algorithm_manager, self.error_handler, self.drawing_handler)

    #Main driver code for pygame
    def run(self):

        #Changable colors for the background
        BG_COLOR = (255,255,255)
        RECT_COLOR = (220, 220, 220)

        pg.init()

        #Initialize some variables 
        self.text.handle_text('Maze Visualization', 'Maze Generator + Solver')
        self.state_manager.step_path_last_time = pg.time.get_ticks()
        self.state_manager.draw_maze_last_time = pg.time.get_ticks()
        self.clock = pg.time.Clock()

        #Store background in a cache
        bg = background.Background(self.state_manager.screen_width, self.state_manager.screen_height, 100)  
        bg.draw_background(BG_COLOR, RECT_COLOR, 10, 250)

        #Create and store all the text
        self.state_manager.title_font = pygame.font.Font(None, 48)
        self.state_manager.body_font = pygame.font.Font(None, 25)
        self.text.initilize_text()

        while self.state_manager.running:
            #Limit to 60 FPS
            self.clock.tick(60)

            #Load background first
            self.state_manager.screen.fill(BG_COLOR)
            self.state_manager.screen.blit(bg.background, (0,0))

            #Handle all user inputs
            self.event_handler.handle_input(pg.event.get())
            self.event_handler.handle_key_strokes(pg.key.get_pressed())
            
            #Draw everything to screen
            if self.state_manager.draw_help:
                self.text.help_text()

            if self.state_manager.draw_menu:
                self.text.admin_menu()
                self.drawing_handler.admin_menu()

            if self.state_manager.draw_maze:
                self.drawing_handler.draw_maze()

            if self.state_manager.draw_blank_maze:
                self.drawing_handler.draw_blank_maze()

            if self.state_manager.start != None:
                self.drawing_handler.draw_start()

            if self.state_manager.stop != None:
                self.drawing_handler.draw_stop()

            if self.state_manager.draw_step_path:
                self.drawing_handler.draw_step_path()

            if self.state_manager.draw_solution_path:
                self.drawing_handler.draw_solution()

            if self.state_manager.draw_log:
                self.drawing_handler.draw_log()
            
            #Create a copy of the regular screen, and zoom in the copy if the zoom scale is anything but 0
            zoomed_screen = pg.transform.smoothscale(self.state_manager.screen, 
                                                    ((self.state_manager.screen_width + self.state_manager.zoom_scale),
                                                    (self.state_manager.screen_height + self.state_manager.zoom_scale)))
            
            #Blit the zoomed screen on the regular screen, and adjust for the offsets
            self.state_manager.screen.blit(zoomed_screen, 
                                           (self.state_manager.zoom_offset_x,
                                            self.state_manager.zoom_offset_y))

            pg.display.flip()