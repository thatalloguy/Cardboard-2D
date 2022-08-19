import pygame

class Text:
    def __init__(self,text,position,color1=(255,255,255),color2=(0,0,0),font="default",size=32):
        self.size = size
        if font == "default":
            self.font = pygame.font.Font('cardboard/fonts/mon.ttf', self.size)
        else:
            self.font = pygame.font.Font(font, self.size)
        self.text = text
        self.position = position
        self.color1 = color1
        self.color2 = color2

    def parent_draw(self):
        try:
            text = self.font.render(self.text, True, self.color1)
            textRect = text.get_rect()
            textRect.x = self.position[0]
            textRect.y = self.position[1]
            pygame.display.get_surface().blit(text, textRect)
        except:
            pass
