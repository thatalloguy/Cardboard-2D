import pygame

class Tool:
    def __init__(self,x,y,width,height,image=None,color=(255,0,0),debug_rendering=False,debug_color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.debug_rendering = debug_rendering
        self.debug_color = debug_color
        self.screen = pygame.display.get_surface()
        self.color = color
        if self.image != None:
            self.image = pygame.image.load(self.image)
            self.image = pygame.transform.scale(self.image,(self.width,self.height))
            self.rect = self.image.get_rect()
        else:
            self.rect = pygame.rect.Rect((self.x,self.y,self.width,self.height))

        self.rect.x = self.x
        self.rect.y = self.y

    def render(self):
        if self.debug_rendering:
            pygame.draw.rect(self.screen,self.debug_color,self.rect,2)
        if self.image != None:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(self.screen,self.color,self.rect)