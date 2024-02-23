import pygame as pg

class Text:
    def __init__(self, state_manager:object):
        self.state_manager = state_manager
        self.stored_text = {}

    def create_text(self, name:str, text:str, size:str, color:tuple, y_position:float):
        if size == 'title':
            text_surface = self.state_manager.title_font.render(text, True, color)
        elif size == 'body':
             text_surface = self.state_manager.body_font.render(text, True, color)
        text_position = ((self.state_manager.screen_width // 2) - text_surface.get_size()[0] // 2, y_position)
        self.stored_text[name] = (text_surface, text_position)

    def blit_text(self, name:str):
        surface = self.stored_text[name][0]
        position = self.stored_text[name][1]
        self.state_manager.screen.blit(surface, position)
        
    #Change screen caption and add text to console log
    def handle_text(self,caption_text:str, log_text:str):
        pg.display.set_caption(caption_text)
        self.state_manager.console_log.append(log_text)

    #Store text in state
    def initilize_text(self):

        #Help Menu Text
        self.create_text('help_title', 'Help Menu', 'title', (100,100,255), self.state_manager.title_y_offset)

        self.create_text('help_text_1', '-Press G to Generate a Maze', 'body', (0,0,0), self.state_manager.body_y_offset)
        self.create_text('help_text_2', '-Press M to Make a Maze', 'body', (0,0,0), self.state_manager.body_y_offset + 20)
        self.create_text('help_text_3', '(hold LSHIFT while dragging mouse to draw walls)', 'body', (0,0,0), self.state_manager.body_y_offset + 40)
        self.create_text('help_text_4', '-Left Click to Place Start', 'body', (0,0,0), self.state_manager.body_y_offset + 80)
        self.create_text('help_text_5', '-Right Click to Place End', 'body', (0,0,0), self.state_manager.body_y_offset + 100)
        self.create_text('help_text_6', '-Press A for A*', 'body', (0,0,0), self.state_manager.body_y_offset + 140)
        self.create_text('help_text_7', '-Press B for BFS', 'body', (0,0,0), self.state_manager.body_y_offset + 160)
        self.create_text('help_text_8', '-Press D for DFS', 'body', (0,0,0), self.state_manager.body_y_offset + 180)
        self.create_text('help_text_9', '-Press P to Show Solution', 'body', (0,0,0), self.state_manager.body_y_offset + 220)
        self.create_text('help_text_10', '-Press Right Shift For Step Path', 'body', (0,0,0), self.state_manager.body_y_offset + 240)
        self.create_text('help_text_11', '-Press C to Clear Paths', 'body', (0,0,0), self.state_manager.body_y_offset + 260)
        self.create_text('help_text_12', '-Press Z to Zoom (Arrow Keys to Move)', 'body', (0,0,0), self.state_manager.body_y_offset + 300)
        self.create_text('help_text_13', '-Press H for Help', 'body', (0,0,0), self.state_manager.body_y_offset + 320)
        self.create_text('help_text_14', '-Press L for Log', 'body', (0,0,0), self.state_manager.body_y_offset + 340)
        self.create_text('help_text_15', '-Press LCTRL for Admin Panel', 'body', (0,0,0), self.state_manager.body_y_offset + 360)

        #Admin Menu Text
        self.create_text('admin_title', 'Admin Panel', 'title', (100,100,255), self.state_manager.title_y_offset)

        self.create_text('admin_text_1', '-Enter Maze Width and Hit Enter', 'body', (0,0,0), self.state_manager.body_y_offset + 20)
        self.create_text('admin_text_2', '-Enter Maze Height and Hit Enter', 'body', (0,0,0), self.state_manager.body_y_offset + 40)
        self.create_text('admin_text_3', 'Step Path Speed:', 'body', (0,0,0), self.state_manager.step_path_circle_y - 20)
        self.create_text('admin_text_4', '1  2  3  4  5', 'body', (0,0,0), self.state_manager.step_path_circle_y + 20)
        self.create_text('admin_text_5', 'Maze Generation Speed:', 'body', (0,0,0), self.state_manager.maze_circle_y - 20)
        self.create_text('admin_text_6', '1  2  3  4  5', 'body', (0,0,0), self.state_manager.maze_circle_y + 20)

        self.state_manager.arrow_y = 200 + 5
        
        #Console Log
        self.create_text('console_title', 'Console Log', 'title', (100,100,255), self.state_manager.title_y_offset)

    #Blit Help text
    def help_text(self):
        self.blit_text('help_title')
        self.blit_text('help_text_1')
        self.blit_text('help_text_2')
        self.blit_text('help_text_3')
        self.blit_text('help_text_4')
        self.blit_text('help_text_5')
        self.blit_text('help_text_6')
        self.blit_text('help_text_7')
        self.blit_text('help_text_8')
        self.blit_text('help_text_9')
        self.blit_text('help_text_10')
        self.blit_text('help_text_11')
        self.blit_text('help_text_12')
        self.blit_text('help_text_13')
        self.blit_text('help_text_14')
        self.blit_text('help_text_15')
            
    #Blit Admin text
    def admin_menu(self):
        self.create_text('admin_text_width', f'Width: {self.state_manager.maze_width}', 'body', (0,0,0), self.state_manager.body_y_offset + 100)
        self.create_text('admin_text_height', f'Height: {self.state_manager.maze_height}', 'body', (0,0,0), self.state_manager.body_y_offset + 120)

        self.blit_text('admin_title')
        self.blit_text('admin_text_1')
        self.blit_text('admin_text_2')
        self.blit_text('admin_text_width')
        self.blit_text('admin_text_height')
        self.blit_text('admin_text_3')
        self.blit_text('admin_text_4')
        self.blit_text('admin_text_5')
        self.blit_text('admin_text_6')

        #Arrow
        pg.draw.polygon(self.state_manager.screen, (0, 0, 0),(
                                                (self.state_manager.screen_width // 2 + 100,self.state_manager.arrow_y + 3),
                                                (self.state_manager.screen_width// 2 + 100,self.state_manager.arrow_y + 3),
                                                ((self.state_manager.screen_width // 2) + 80,self.state_manager.arrow_y + 3),
                                                ((self.state_manager.screen_width // 2) + 80,self.state_manager.arrow_y - 7),
                                                ((self.state_manager.screen_width // 2) + 60, self.state_manager.arrow_y),
                                                ((self.state_manager.screen_width // 2) + 80, self.state_manager.arrow_y + 7),
                                                ((self.state_manager.screen_width // 2) + 80, self.state_manager.arrow_y - 3),
                                                (self.state_manager.screen_width // 2 + 100, self.state_manager.arrow_y - 3),
                                                (self.state_manager.screen_width // 2 + 100,self.state_manager.arrow_y - 3)
                                                ))
        
        


    