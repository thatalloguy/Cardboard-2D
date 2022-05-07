import pygame
from cardboard.Logger import *
try:
    pygame.init()
except:
    pass

class Entity:
    def __init__(self,WINDOW,name,x,y,sprite,width,height):
        self.logger = Logger()
        self.name = name
        self.window = WINDOW.screen
        self.x = x
        self.y = y
        self.sprite = sprite
        self.width = width
        self.height = height
        self.logger.send_info("Creating Entity: " + self.name)

        #Checking / Creating the Shape type

        try:
            self.shape_type = self.sprite.get_type()
        except:
            self.shape_type = self.sprite

        #Change the Image width and height
        if self.shape_type == "SPRITE":
            self.image = self.sprite.get_image()
            self.new_image = pygame.transform.scale(self.image, (self.width,self.height))
            self.sprite.set_image(self.new_image)

    def change_x(self,x):
        self.x = x

    def change_y(self,x):
        self.y = x

    def render(self):
        self.window.blit(self.new_image, (self.x,self.y))