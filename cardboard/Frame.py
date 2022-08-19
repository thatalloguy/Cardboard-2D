import pygame

class Frame:
    def __init__(self,pos,width,height,color=(0,255,0),image=None):
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height
        self.color = color
        self.image = image
        self.children = []
        self.disable_children = False
        if self.image != None:
            self.image = pygame.image.load(self.image)
            self.image = pygame.transform.scale(self.image, (self.width,self.height))

    def render(self):
        #determines if its a sprite or rect
        if self.image == None:
            try:
                pygame.draw.rect(pygame.display.get_surface(), self.color, pygame.Rect(self.x, self.y,self.width,self.height))
            except:
                pass
        else:
            pygame.display.get_surface().blit(self.image, (self.x,self.y))

        #draw ma kids
        for child in self.children:
            try:
                if not self.disable_children:
                    child.parent_draw()
            except:
                pass


    def add_child(self,child):
        self.children.append(child)