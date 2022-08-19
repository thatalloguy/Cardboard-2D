import pygame

class Entry():
    def __init__(self, x, y, width,height,border_width=2,color_active=(255,255,255),color_passive=(102, 102, 102),text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_width = border_width
        self.color_active = color_active
        self.color_passive = color_passive
        self.user_text = text
        self.input_rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.active = False
        self.screen = pygame.display.get_surface()
        self.base_font = pygame.font.Font(None,self.height)
        self.color = self.color_passive

    def handle(self,events):
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.active = True
                    self.color = self.color_active
                else:
                    self.active = False
                    self.color = self.color_passive

            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        self.user_text += event.unicode



        pygame.draw.rect(self.screen, self.color, self.input_rect, 2)

        text_surface = self.base_font.render(self.user_text, True, self.color)
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        self.input_rect.w = max(self.width, text_surface.get_width() + 10)


