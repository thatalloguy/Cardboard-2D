import pygame
from cardboard.Logger import *
import os
try:
    pygame.init()
except:
    pass

class Entity(pygame.sprite.Sprite):
    def __init__(self,camera,pos,sprite,width,height):
        pygame.sprite.Sprite.__init__(self)
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
        self.camera = camera
        #self.logger.send_info("Converting Sprite Image")


        try:
            self.image = pygame.image.load(str(self.cwd) + "/" +self.path)
        except:
            self.image = pygame.image.load(str(self.cwd) + "/" + "cardboard/images/missing_texture.png")
            self.logger.send_warning("Missing a texture!", type="MEDIUM",poppup=False)

        #self.logger.send_info("Scaling Sprite Image")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect(center=self.pos)

        #self.logger.send_info("Creating Entity")
        self.ground_y = self.pos[1]
        self.frame = 9
        self.last_update = pygame.time.get_ticks()



    def get_type(self):
        return "ENTITY"

    def render(self):
        self.image = pygame.transform.scale(self.image, (self.width * self.camera.get_zoom(), self.height * self.camera.get_zoom()))
        pygame.display.get_surface().blit(self.image, (self.rect.x + self.camera.get_pos()[0],self.rect.y + self.camera.get_pos()[1]))
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
