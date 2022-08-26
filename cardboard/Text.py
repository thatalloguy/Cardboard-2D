import pygame

class Text:
    def __init__(self,text,x,y,color1=(255,255,255),color2=(0,0,0),font="default",size=32):
        self.size = size
        if font == "default":
            self.font = pygame.font.Font('cardboard/fonts/mon.ttf', self.size)
        else:
            self.font = pygame.font.Font(font, self.size)
        self.text = text
        self.x= x
        self.y  =y
        self.color1 = color1
        self.color2 = color2

    def parent_draw(self):
        try:
            text = self.font.render(self.text, True, self.color1)
            self.textRect = text.get_rect()
            self.textRect.x = self.x
            self.textRect.y = self.y
            pygame.display.get_surface().blit(text, self.textRect)
        except:
            pass
