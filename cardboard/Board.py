from cardboard.Logger import *

import pygame
pygame.init()
import os

# Get the current working directory

class Board:
    def __init__(self,width,height,title=None,icon=None,fullscreen=None,fps=60,bg=None,resolution=None):
        self.logger = Logger()
        self.width = width
        self.is_sky = False
        self.resolution = resolution
        self.height = height
        self.title = title
        self.fps = fps
        self.icon = icon
        self.bg = bg
        self.cwd = os.getcwd()
        self.anlog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1}
        self.fullscreen = fullscreen


        self.entities = []

        self.clock = pygame.time.Clock()
        #Window Creation
        if self.fullscreen != None:
            infoObject = pygame.display.Info()
            self.screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
            self.logger.send_info("Creating window in fullscreen")

        elif self.fullscreen == None:
            if self.resolution != None:
                self.window = pygame.display.set_mode([self.width, self.height], pygame.RESIZABLE)
                self.screen = self.resolution
                self.logger.send_info("Creating window using custom resolution")
            else:
                self.screen = pygame.display.set_mode([self.width, self.height], pygame.RESIZABLE)
                self.logger.send_info("Creating window using custom resolution")

        if self.title != None:
            pygame.display.set_caption(self.title)
            self.logger.send_info("Setting the Title to Custom")

        elif self.title == None:
            self.logger.send_info("Setting the Title to template")
            pygame.display.set_caption("A CardBoard Application")

        if self.icon != None:
            self.icon_image = pygame.image.load(self.icon)
            pygame.display.set_icon(self.icon_image)
            self.logger.send_info("Using Custom Icon")

        elif self.icon == None:
            self.icon_image = pygame.image.load(("cardboard/images/logo.png"))
            pygame.display.set_icon(self.icon_image)
            self.logger.send_info("Using Template Icon")

        if self.fps == None:
            self.fps = 60

        if self.bg == None:
            self.bg = (0,0,0)

    def update(self):
        try:
            self.clock.tick(self.fps)

            pygame.display.flip()
            pygame.display.update()
        except:
            pass


    def clear(self,r,g,b):
        try:
            pygame.display.get_surface().fill((r,g,b))
        except:
            pass


    def get_fps(self):
        return str(self.clock.get_fps())
