import pygame as pg
import random

class Background:
    def __init__(self, screen_width:float, screen_height:float, cell_amount:int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_amount = cell_amount
        self.background = pg.Surface((screen_width, screen_height))

    #Clamps random value to the range of 0-255
    def clamp(self, number:float):
        if number > 255:
            return 255
        elif number < 0:
            return 0
        return number

    #Generate a random alpha value in a descending order of darkness
    def random_bg_value(self, col:int, RECT_COLOR:tuple, noise_range:int, distribution:int):
        noise = random.randint(-noise_range,noise_range)
        noise += col * 3 + random.randint(-distribution, distribution)
        random_value_a = self.clamp(noise)

        return (RECT_COLOR[0], RECT_COLOR[1], RECT_COLOR[2], random_value_a)

    #Create a surface and blit the rectangles onto the surface
    def draw_background(self, BG_COLOR:tuple, RECT_COLOR:tuple, noise_range:int, distribution:int):
        self.background.fill(BG_COLOR)
        bg_cell_width = self.screen_width // self.cell_amount
        bg_cell_height = self.screen_height // self.cell_amount

        for row in range(self.cell_amount // 2):
            for col in range(self.cell_amount // 2):
                surface = pg.Surface((bg_cell_width, bg_cell_height)).convert_alpha()
                surface.fill(self.random_bg_value(col, RECT_COLOR, noise_range, distribution))
                self.background.blit(surface, 
                                    (row*bg_cell_width + (bg_cell_width*row) + bg_cell_width,
                                    col*bg_cell_height + (bg_cell_height*col) + bg_cell_height))
                