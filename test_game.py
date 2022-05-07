import pygame.time
import pygame
from cardboard import *
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

window = Board(1280,720,fps=60,bg=(74, 255, 255))
window.update()
running = True
x = 0
y = -64
mountains = Entity(window,"Mountains",x,y,Sprite(path="images/mountains.png"),1280,720)
ground = Entity(window,"ground",0,720 - 64,Sprite(path="images/ground.png"),1280,64)
while running:
    window.loop_init()
    mountains.render()
    ground.render()





    #pygame.time.Clock.tick(60)
    window.update()

