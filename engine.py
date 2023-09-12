import pygame as pg
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
        self.state_manager = state_manager.State_Manager()

        self.state_manager.screen_width=screen_width
        self.state_manager.screen_height=screen_height

        self.state_manager.screen=pg.display.set_mode((screen_width, screen_height))
        self.clock = pg.time.Clock()

        self.text = text.Text(self.state_manager)

        self.state_manager.last_time = pg.time.get_ticks()

        self.maze_manager = maze_generator.Maze()

        self.error_handler = error_handler.Error_Handler(self.state_manager, self.text)

        self.algorithm_manager = algorithm_manager.Algorithm_Manager(self.maze_manager, self.state_manager, self.text, self.error_handler)

        self.drawing_handler = drawing_handler.Drawing_Handler(self.state_manager, self.maze_manager, self.algorithm_manager, self.text)

        self.event_handler = event_handler.Event_Handler(self.state_manager, self.text, self.algorithm_manager, self.error_handler, self.drawing_handler)

        self.text.handle_text('Maze Generator + Solver', 'Maze Generator + Solver', self.state_manager)

    #Main driver code for pygame
    def run(self):

        BG_COLOR = (255,255,255)
        RECT_COLOR = (220, 220, 220)

        pg.init()
        bg = background.Background(self.state_manager.screen_width, self.state_manager.screen_height, 100)
        
        bg.draw_background(BG_COLOR, RECT_COLOR, 10, 250)

        self.text.initilize_text()

        while self.state_manager.running:
            self.clock.tick(60)

            self.state_manager.screen.fill(BG_COLOR)
            self.state_manager.screen.blit(bg.background, (0,0))

            self.event_handler.handle_input(pg.event.get())

            self.event_handler.handle_key_strokes(pg.key.get_pressed())
            
            if self.state_manager.draw_help:
                self.text.help_text()

            if self.state_manager.draw_menu:
                self.text.help_menu()

            if self.state_manager.draw_maze:
                self.drawing_handler.draw_maze()

            if self.state_manager.start!=None:
                self.drawing_handler.draw_start()

            if self.state_manager.stop!=None:
                self.drawing_handler.draw_stop()

            if self.state_manager.draw_step_path:
                self.drawing_handler.draw_step_path()

            if self.state_manager.draw_solution_path:
                self.drawing_handler.draw_solution()

            if self.state_manager.draw_log:
                self.drawing_handler.draw_log()

            pg.display.flip()