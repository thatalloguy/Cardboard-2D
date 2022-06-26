import pygame, random
from cardboard.Logger import Logger

particles = []

class Particle(pygame.sprite.Sprite):
    def __init__(self,group,preset=None,loc=None,vel=None,lifespan=None,color=None):
        super().__init__(group)
        global particles
        self.color = None
        self.particles = particles
        self.preset = preset
        self.loc = loc
        self.vel = vel
        self.ls = lifespan
        self.color = color
        self.screen = pygame.display.get_surface()
        self.use_preset = False
        if self.ls == None and self.vel == None and self.preset != None:
            self.use_preset = True

        if self.use_preset == True:
            Logger.send_info(self, "USING PRESET " + self.preset)
            if self.preset == "simple":
                self.vel = [random.randint(0, 20) / 10 - 1, -2]
                self.ls = random.randint(4, 16)

        self.particles.append([self.loc, self.vel, self.ls])
        self.render(0,0)

    def render(self,x,y):
        print("RENDER")
        if self.preset == "simple":
            self.vel = [random.randint(0, 20) / 10 - 1, -2]
            self.ls = random.randint(4, 16)

        for particle in self.particles:
            particle[0][0] = x + particle[1][0]
            particle[0][1] = y + particle[1][1]
            particle[2] -= 0.1  # lifespan
            particle[1][1] += 0.03  # gravity
            pygame.draw.circle(self.screen, (255, 255, 255), particle[0], particle[2])
            self.rect = pygame.rect.Rect((particle[0][1] + particle[2], particle[0][0] + particle[2], particle[0][0], particle[0][1]))
            if particle[2] <= 0:
                self.particles.remove(particle)
    def get_type(self):
        return "PARTICLE"