import pygame as pg
import ptext

class Text:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.stored_text = {}

    #Create a text surface and store it
    def create_text(self, name:str, text:str, position:tuple, fontsize:int, underline:bool, color:tuple, shadow:tuple):
        surface, position = ptext.draw(text, midbottom = position, fontsize = fontsize, underline = underline, color=color, shadow=shadow)
        self.stored_text[name] = (surface, position)

    #Change screen caption and add text to console log
    def handle_text(self,caption_text, log_text, state_manager):
        pg.display.set_caption(caption_text)
        state_manager.console_log.append(log_text)

    #Store text in state
    def initilize_text(self):

        #Help Menu Text
        self.create_text('help_title', 'Help Menu', (self.state_manager.screen_width//2, 50), 48, True, (100,100,255), (0.3,0.3))
        self.create_text('help_text','-Press G to Generate a Maze\n-Press D to Draw a Maze\n(hold shift while dragging mouse to draw walls)\n\n-Left Click to Place Start\n-Right Click to Place End\n\n-Press A for A*\n-Press B for BFS\n\n-Press P to Show Solution\n-Press Right Arrow For Step Path\n-Press C to Clear Paths\n-Press H for Help', (self.state_manager.screen_width//2, (self.state_manager.screen_height//2)+100), 25, False, (0,0,0), (0,0))

        #Admin Menu Text
        self.create_text('admin_title', 'Admin Panel', (self.state_manager.screen_width//2, 50), 48, True, (100,100,255), (0.3,0.3))
        self.create_text('admin_text_header', '-Enter Maze Width and Hit Enter\n-Enter Maze Height and Hit Enter', (self.state_manager.screen_width//2, (self.state_manager.screen_height//2)-100), 25, False, (0,0,0), (0,0))
        
        #Console Log
        self.create_text('console_title', 'Console Log', (self.state_manager.screen_width//2, 50), 48, True, (100,100,255), (0.3,0.3))

    #Blit Help text
    def help_text(self):
        self.state_manager.screen.blit(self.stored_text['help_title'][0], self.stored_text['help_title'][1])
        self.state_manager.screen.blit(self.stored_text['help_text'][0], self.stored_text['help_text'][1])
            
    #Blit Admin text
    def help_menu(self):
        self.create_text('admin_text_width_height', f'Width: {self.state_manager.maze_width}\nHeight: {self.state_manager.maze_height}', (self.state_manager.screen_width//2, (self.state_manager.screen_height//2)-50), 25, False, (0,0,0), (0,0))
        self.state_manager.screen.blit(self.stored_text['admin_title'][0], self.stored_text['admin_title'][1])
        self.state_manager.screen.blit(self.stored_text['admin_text_header'][0], self.stored_text['admin_text_header'][1])
        self.state_manager.screen.blit(self.stored_text['admin_text_width_height'][0], self.stored_text['admin_text_width_height'][1])

        #Arrow
        pg.draw.polygon(self.state_manager.screen, (0, 0, 0),(
                                                (340,self.state_manager.arrow_y+3),
                                                (340,self.state_manager.arrow_y+3),
                                                (320,self.state_manager.arrow_y+3),
                                                (320,self.state_manager.arrow_y-7),
                                                (300, self.state_manager.arrow_y),
                                                (320, self.state_manager.arrow_y+7),
                                                (320, self.state_manager.arrow_y-3),
                                                (340, self.state_manager.arrow_y-3),
                                                (340,self.state_manager.arrow_y-3)
                                                ))


    