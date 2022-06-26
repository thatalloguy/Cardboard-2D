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


    def get_path(self):
        return self.path

    def get_image(self):
        return self.image

    def get_type(self):
        return "SPRITE"

    def set_image(self,image):
        self.image = image
