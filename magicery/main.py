from cardboard import *


window = Board(pygame.display.Info().current_w,pygame.display.Info().current_h,resolution=pygame.Surface([1280, 720]),icon="images/other/logo.png",bg=(255,255,26))
window.set_font("PIXEL")
font = pygame.font.Font('cardboard/fonts/FFFFORWA.TTF', 32)
camera = Camera((0,0), 1)
bob = Entity(camera,(500,500),Sprite(path="WAD"),100,100)
scene = "MAIN_MENU"
# Main Menu Gui
start_button = Button(1280 / 2 + 250, 300, pygame.image.load("images/gui/start_button.png"), 10)
quit_button = Button(1280 / 2 + 250, 550, pygame.image.load("images/gui/quit_button.png"), 10)
Logo = Entity(camera, (1280 / 2 + 425,300), Sprite(path="images/other/logo.png"), 500, 500)
# Server Selection Menu Gui
#font = pygame.font.SysFont(None, 100)
button_1 = Button(1280 / 2 - 150, 300, pygame.image.load("images/gui/input/1.png"), 5)
button_2 = Button(1280 / 2, 300, pygame.image.load("images/gui/input/2.png"), 5)
button_3 = Button(1280 / 2 + 150, 300, pygame.image.load("images/gui/input/3.png"), 5)
button_4 = Button(1280 / 2 - 150, 450, pygame.image.load("images/gui/input/4.png"), 5)
button_5 = Button(1280 / 2, 450, pygame.image.load("images/gui/input/5.png"), 5)
button_6 = Button(1280 / 2 + 150, 450, pygame.image.load("images/gui/input/6.png"), 5)
button_7 = Button(1280 / 2 - 150, 600, pygame.image.load("images/gui/input/7.png"), 5)
button_8 = Button(1280 / 2, 600, pygame.image.load("images/gui/input/9.png"), 5)
button_9 = Button(1280 / 2 + 150, 600, pygame.image.load("images/gui/input/8.png"), 5)
button_0 = Button(1280 / 2, 750, pygame.image.load("images/gui/input/0.png"), 5)
button_quit = Button(1280 / 2 + 150, 750, pygame.image.load("images/gui/input/reset.png"), 5)
button_join = Button(1280 / 2 + 400, 350, pygame.image.load("images/gui/input/join.png"), 5)
button_host = Button(1280 / 2 + 400, 500, pygame.image.load("images/gui/input/host.png"), 5)
ip = ""

# Game loop
running = True
while running:

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

    pygame.display.get_surface().fill((255, 255, 255))

    # Main Menu
    if scene == "MAIN_MENU":
        Logo.render()

        if start_button.draw(pygame .display.get_surface()):
            scene = "SERVER"

        if quit_button.draw(pygame.display.get_surface()):
            running = False
    elif scene == "SERVER":
        text = font.render(ip, True, (255,0,255),(0,255,200))
        textRect = text.get_rect()
        textRect.x = 500
        textRect.y = 100
        pygame.display.get_surface().blit(text, textRect)
        print(ip)
        if button_1.draw(pygame.display.get_surface()):
            ip = str(ip + "1")
        if button_2.draw(pygame.display.get_surface()):
            ip = str(ip + "2")
        if button_3.draw(pygame.display.get_surface()):
            ip = str(ip + "3")
        if button_4.draw(pygame.display.get_surface()):
            ip = str(ip + "4")
        if button_5.draw(pygame.display.get_surface()):
            ip = str(ip + "5")
        if button_6.draw(pygame.display.get_surface()):
            ip = str(ip + "6")
        if button_7.draw(pygame.display.get_surface()):
            ip = str(ip + "7")
        if button_8.draw(pygame.display.get_surface()):
            ip = str(ip + "8")
        if button_9.draw(pygame.display.get_surface()):
            ip = str(ip + "9")
        if button_0.draw(pygame.display.get_surface()):
            ip = str(ip + "0")
        if button_quit.draw(pygame.display.get_surface()):
            ip = ""
        if button_join.draw(pygame.display.get_surface()):
            ip = ""
        if button_host.draw(pygame.display.get_surface()):
            ip = ""
    window.update()



