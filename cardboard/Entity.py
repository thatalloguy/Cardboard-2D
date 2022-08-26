import pygame
from cardboard.Logger import *
import os
try:
    pygame.init()
except:
    pass

class Entity(pygame.sprite.Sprite):
    def __init__(self,camera,pos,sprite,width,height,debug_rendering=False,debug_color=(255,0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.logger = Logger()
        self.cwd = os.getcwd()
        self.window = pygame.display.get_surface()
        self.monitor_width = pygame.display.get_window_size()[0]
        self.monitor_height = pygame.display.get_window_size()[1]
        self.x = round(pos[0])
        self.y = round(pos[1])
        self.pos = pos
        self.sprite = sprite.get_path()
        self.width = width
        self.path = self.sprite
        self.old_path = self.path
        self.height = height
        self.camera = camera
        self.id = 0
        self.destroyed = False
        self.debug_rendering = debug_rendering
        self.debug_color = debug_color
        self.zoom = self.camera.zoom
        #self.logger.send_info("Converting Sprite Image")


        try:
            self.image = pygame.image.load(self.path)
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

        self.string = str(self.x) + "|" + str(self.y) + "|" +  str(self.path) + "|" + str(self.width) + "|" + str(self.height) + "$"
    def get_type(self):
        return "ENTITY"

    def render(self):
        #self.image = pygame.transform.scale(self.image, (self.width * self.camera.get_zoom(), self.height * self.camera.get_zoom()))
        if not self.destroyed:
            self.rect.x = self.camera.cam_x + self.x# + self.monitor_width / 2
            self.rect.y = self.camera.cam_y + self.y# + self.monitor_height / 2
            #self.x, self.y = self.rect.x,self.rect.y
            if self.rect.w != self.width:
                self.image = pygame.transform.scale(self.image, (self.width, self.height))

            if self.rect.h != self.height:
                self.image = pygame.transform.scale(self.image, (self.width, self.height))

            if self.old_path != self.path:
                self.old_path = self.path
                try:
                    self.image = pygame.image.load(self.path)
                    self.image = pygame.transform.scale(self.image, (self.width, self.height))
                except:
                    self.image = pygame.image.load(str(self.cwd) + "/" + "cardboard/images/missing_texture.png")
                    self.image = pygame.transform.scale(self.image, (self.width, self.height))
                    self.logger.send_warning("Missing a texture!", type="MEDIUM", poppup=False)

            self.rect.w = self.width
            self.rect.h = self.height
            pygame.display.get_surface().blit(self.image, (self.rect.x,self.rect.y))
            if self.debug_rendering:
                pygame.draw.rect(self.window,self.debug_color,self.rect,4)
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

    def destroy(self):
        self.destroyed = True
