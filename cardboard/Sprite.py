from cardboard.Logger import *
import pygame
try:
    pygame.init()
except:
    pass


class Sprite:
    def __init__(self,path=None):
        self.path = path
        self.logger = Logger()
        if self.path == None:
            self.logger.send_error("Missing -Path in Sprite")
        elif self.path != None:
            self.image = pygame.image.load(self.path)

    def get_path(self):
        return self.path

    def get_image(self):
        return self.image

    def get_type(self):
        return "SPRITE"

    def set_image(self,image):
        self.image = image
