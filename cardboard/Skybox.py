import pygame
from cardboard.Board import Board
from cardboard.Logger import *

class SkyBox():
    def __init__(self,sprite):

        self.logger = Logger()


        self.sprite = sprite
        self.path = self.sprite.get_path()
        self.w, self.h = pygame.display.get_surface().get_size()
        try:
            self.image = pygame.image.load(self.path)
        except:
            self.image = pygame.image.load("cardboard/images/missing_texture.png")
            self.logger.send_warning("Missing a texture!", type="MEDIUM",poppup=False)
        self.logger.send_info("Scaling Sprite Image")
        self.image = pygame.transform.scale(self.image, (self.w, self.h))


    def render(self):
        pygame.display.get_surface().blit(self.image, (0, 0))
    def get_type(self):
        return "ENTITY"