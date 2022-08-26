import os.path

from cardboard import *

TITLE, BACKGROUND, FPS = "A working game (i hope)", (255, 255, 255), 60

import pygame, json, sys

if __name__ == '__main__':

    current_direct = os.getcwd()

    # os.chdir(Path(os.getcwd()).parent.parent)
    window = Board(pygame.display.Info().current_w, pygame.display.Info().current_h - 50,
                   title=TITLE, bg=BACKGROUND, fps=FPS)

    camera = Camera((0, 0), 100)

    entities = []

    with open(current_direct + "/projects/" + sys.argv[1] + "/game_data.json", "r") as file:
        data = json.load(file)
        file.close()

    with open(current_direct + "/projects/" + sys.argv[1] + "/data/camera_data.json", "r") as le_file:
        camera_data = json.load(le_file)
        le_file.close()

    with open(current_direct + "/projects/" + sys.argv[1] + "/data/script_data.json", "r") as le_file:
        script_data = json.load(le_file)
        le_file.close()

    camera.cam_x = camera_data["0"]
    camera.cam_y = camera_data["1"]
    all_scripts = []
    script_count = 0
    for i in script_data:
        try:
            all_scripts.append(script_data[str(script_count)])
        except:
            print("Oh NO")

    count = 0
    for i in data:
        new_x = data[str(count)][0]
        new_y = data[str(count)][1]
        new_path = data[str(count)][2]
        new_width = data[str(count)][3]
        new_height = data[str(count)][4]
        is_destroyed = data[str(count)][5]
        count += 1
        # add the offsetmonkey
        if not is_destroyed:
            new_entity = Entity(camera, (new_x - new_width / 2 - camera.cam_x, new_y - new_height / 2 - camera.cam_y),
                                Sprite(path=str(new_path)), new_width, new_height)
            new_entity.destroyed = is_destroyed
            entities.append(new_entity)

    # Game Loop
    for script in all_scripts:
        os.system("python projects/" + sys.argv[1] + "/scripts/" + script + ".py on_start")

    while True:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.clear(BACKGROUND[0], BACKGROUND[1], BACKGROUND[2])

        for entity in entities:
            entity.render()

        for script in all_scripts:
            os.system("python projects/" + sys.argv[1] + "/scripts/" + script + ".py on_tick")

        window.update()