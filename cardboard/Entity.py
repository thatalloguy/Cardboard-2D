import pygame
from cardboard.Logger import *
import os
try:
    pygame.init()
except:
    pass

class Entity(pygame.sprite.Sprite):
    def __init__(self,camera,pos,sprite,width,height):
        super().__init__(camera)
        self.logger = Logger()
        self.cwd = os.getcwd()
        self.window = pygame.display.get_surface()
        self.x = pos[0]
        self.y = pos[1]
        self.pos = pos
        self.sprite = sprite.get_path()
        self.width = width
        self.path = self.sprite
        self.height = height
        self.logger.send_info("Converting Sprite Image")


        try:
            self.image = pygame.image.load(str(self.cwd) + "/" +self.path)
        except:
            self.image = pygame.image.load(str(self.cwd) + "/" + "cardboard/images/missing_texture.png")
            self.logger.send_warning("Missing a texture!", type="MEDIUM",poppup=False)

        self.logger.send_info("Scaling Sprite Image")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect(center=self.pos)

        self.logger.send_info("Creating Entity")
        self.camera = camera
        self.frame = 9
        self.last_update = pygame.time.get_ticks()



    def get_type(self):
        return "ENTITY"


    def play_animation(self,animation,speed):
        
        self.current_animation = animation

        self.current_sprite = speed

        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_update >= speed:
            self.frame += 1

            self.last_update = self.current_time
            if self.frame >= len(animation):
                self.frame = 0
            else:
                self.image = self.current_animation[self.frame]

        #print(str(self.frame))
        #if self.frame < len(animation) or self.frame == len(animation):
        #    self.image = self.current_animation[self.frame]
