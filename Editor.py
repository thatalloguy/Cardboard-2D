import pygame.mouse

from cardboard import *
import json
import random
from bisect import bisect_left
# import pygame
def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before

class Ecs:
    def __init__(self):


        self.data = {}

        self.x = []
        self.y = []
        self.sprites = []
        self.width = []
        self.heights = []
        self.id = 0
        self.ids = []
        self.entities = []

    def get(self,id):
        return self.data[str(id)]

    def add_entity(self, entity):
        self.x.append(entity.x)
        self.y.append(entity.y)
        self.sprites.append(entity.path)
        self.width.append(entity.width)
        self.heights.append(entity.height)
        self.data[self.id] = [entity.x,entity.y,entity.path,entity.width,entity.height]
        self.id += 1
        self.entities.append(entity)
        return self.id

    def render(self):
        for entity in self.entities:
            entity.render()
    def get_all(self):
        #self.all_entities = []
        #self.all_entities.append(self.x)
        #self.all_entities.append(self.y)
        ##self.all_entities.append(self.sprites)
        #self.all_entities.append(self.width)
        #self.all_entities.append(self.heights)

        return self.data

    def get_closest(self,position):
        self.all_x = []
        self.all_y = []
        count = 0
        for entity in self.entities:
            self.all_x.append(entity.x)
            self.all_y.append(entity.y)
        self.closest_x = take_closest(self.all_x,position[0])
        self.closest_y = take_closest(self.all_y, position[1])
        for entity in self.entities:
            if entity.x == self.closest_x and entity.y == self.closest_y:
                self.closest_entity = count
                print("Closest X: " + str(entity.x))
                print("closest id: " + str(self.closest_entity))
                return entity, count
            count += 1



class Editor:
    def __init__(self):
        self.main_window = Board(pygame.display.Info().current_w, pygame.display.Info().current_h - 50,
                                 title="A editor maybe??")

        # Setup Gui frames
        self.entity_frame = Frame((5, 5), 400, 300, color=(128, 128, 128))
        self.info_frame = Frame((pygame.display.Info().current_w - 500, 5), 500, pygame.display.Info().current_h - 5,
                                color=(128, 128, 128))
        self.toggle_frame = Frame((0, 0), 0, 0)
        self.toggle_button = Button(self.entity_frame.x, self.entity_frame.y, 50, 50, ">", toggle=True,
                                    command=self.hide_main_menus)
        self.toggle_button.text_object.position = (self.toggle_button.x + 15, self.toggle_button.y + 5)
        self.toggle_button.text_object.color1 = (0, 0, 0)
        self.toggle_frame.add_child(self.toggle_button)
        # Editor Variables
        self.hidden = False
        self.extra_menus = False
        self.run = True
        self.id = 0
        self.Ecs = Ecs()
        self.speed = 2
        self.all_entities = []
        self.monitor_height = pygame.display.Info().current_h - 5
        self.monitor_width = pygame.display.Info().current_w - 5
        self.camera = Camera((0, 0), 100)
        # Toolssss
        self.main_arrow = Entity(self.camera, (-10000, -1000), Sprite(path="editor_gui/main_move.png"), 50, 50)
        self.x_arrow = Entity(self.camera,(-10000,-1000),Sprite(path="editor_gui/arrow_left.png"),200,100)
        self.y_arrow = Entity(self.camera, (-10000, -1000), Sprite(path="editor_gui/arrow_up.png"), 50, 150)

        # MORE UI
        # CreateButton
        self.createbutton = Button(self.entity_frame.x + 175, self.entity_frame.y, 50, 50, "+",
                                   command=self.Create_test_entity)
        self.createbutton.text_object.position = (self.createbutton.x + 15, self.createbutton.y + 5)
        self.createbutton.text_object.color1 = (0, 0, 0)
        self.entity_frame.add_child(self.createbutton)
        # Extra Menu Button
        self.extra_menu_button = Button(self.entity_frame.x + 350, self.entity_frame.y, 50, 50, "=", toggle=True,
                                        command=self.hide_extra_menus)
        self.extra_menu_button.text_object.position = (self.extra_menu_button.x + 15, self.extra_menu_button.y + 5)
        self.extra_menu_button.text_object.color1 = (0, 0, 0)
        self.entity_frame.add_child(self.extra_menu_button)

        # -- Extra Menu Frame
        self.extra_menu = Frame((405, 5), 0, 0, color=(51, 51, 51))
        self.save_button = Button(self.extra_menu.x - 5, self.extra_menu.y, 205, 50, "Save Project",
                                  command=self.save_project)
        self.save_button.text_object.size = 128
        self.save_button.text_object.position = (self.save_button.x + 5, self.save_button.y)
        self.save_button.text_object.color1 = (0, 0, 0)
        self.extra_menu.add_child(self.save_button)
        # Open button
        self.open_button = Button(self.extra_menu.x - 5, self.extra_menu.y + 55, 205, 50, "Open Project",
                                  command=self.open_project)
        self.open_button.text_object.size = 128
        self.open_button.text_object.position = (self.open_button.x, self.open_button.y)
        self.open_button.text_object.color1 = (0, 0, 0)
        self.extra_menu.add_child(self.open_button)

        # Entity Info
        self.x_text = Text("HEllo world",(self.info_frame.x+ 10,self.info_frame.y + 10),color1=(0,0,0),size=64)
        self.y_text = Text("HEllo world", (self.info_frame.x + 10, self.info_frame.y + 65), color1=(0, 0, 0), size=64)
        self.sprite_text = Text("HEllo world", (self.info_frame.x + 10, self.info_frame.y + 120), color1=(0, 0, 0), size=64)
        self.width_text = Text("HEllo world", (self.info_frame.x + 10, self.info_frame.y + 180), color1=(0, 0, 0), size=64)
        self.height_text = Text("HEllo world", (self.info_frame.x + 10, self.info_frame.y + 235), color1=(0, 0, 0), size=64)
        self.show_info = False
        self.changing = False
        self.moving = False
        self.x_moving = False
        self.y_moving = False
        # The Actaul game


    def save_project(self):

        with open("data_file.json", "w") as write_file:
            write_file.write(json.dumps(self.Ecs.data, sort_keys=True, indent=2, ensure_ascii=True))

    def open_project(self):
        print("TEST")
        with open("data_file.json", "r") as file:
            data = json.load(file)
        self.Ecs.data = data
        self.Create_new_entity_from_data(data)

    def Create_new_entity_from_data(self,data):
        count  = 0
        for i in range(10):
            new_x = data[str(count)][0]
            new_y = data[str(count)][1]
            new_path = data[str(count)][2]
            new_width = data[str(count)][3]
            new_height = data[str(count)][4]

            self.new_entity = Entity(self.camera, (new_x,new_y),Sprite(path=new_path), new_width, new_height)
            self.Ecs.add_entity(self.new_entity)
            count += 1
      #data = int(data)


    def hide_main_menus(self):
        if self.hidden:
            self.hidden = False
        else:
            self.hidden = True

    def hide_extra_menus(self):
        if self.extra_menus:
            self.extra_menus = False
        else:
            self.extra_menus = True

    def Create_test_entity(self):
        self.new_entity = Entity(self.camera, (random.randint(int(self.monitor_width / 2), int(self.monitor_width / 2 + 200)), random.randint(int(self.monitor_height / 2),int(self.monitor_height / 2 + 100))), Sprite(path="awda"),100, 100)
        self.stringed_entity = self.new_entity.string
        print("New Entity : " + self.stringed_entity)
        self.Ecs.add_entity(self.new_entity)

        self.id += 1


    def view_entity_info(self,pos):
        found = True
        try:
            self.selected_entity = self.Ecs.get_closest(pos)[0]
        except:
            found = False
        if found:
            print(str(self.selected_entity.x))
            self.x_text.text = "X: " + str(self.selected_entity.x)
            self.y_text.text = "Y: " + str(self.selected_entity.y)
            self.sprite_text.text = "Sprite: " + str(self.selected_entity.path)
            self.width_text.text = "Width: " + str(self.selected_entity.width)
            self.height_text.text = "Height: " + str(self.selected_entity.height)
            self.show_info = True
            self.x_arrow.rect.x = self.selected_entity.x
            self.x_arrow.rect.y = self.selected_entity.y - 25
            self.y_arrow.rect.x = self.selected_entity.x - 30
            self.y_arrow.rect.y = self.selected_entity.y -130
            self.main_arrow.rect.x = self.selected_entity.x - 30
            self.main_arrow.rect.y = self.selected_entity.y

    def main_move_entity_to(self, pos):
        self.move_entity[0].rect.x = pos[0] - self.move_entity[0].width /2
        self.move_entity[0].rect.y = pos[1] - self.move_entity[0].height /2
        self.main_arrow.rect.x = pos[0] - 30
        self.main_arrow.rect.y = pos[1]
        self.x_arrow.rect.x = pos[0]
        self.x_arrow.rect.y = pos[1] - 25
        self.y_arrow.rect.x = pos[0] - 30
        self.y_arrow.rect.y = pos[1] -130

    def x_move_entity_to(self, pos):
        self.move_entity[0].rect.x = pos - self.move_entity[0].width / 2 - 50
        self.main_arrow.rect.x = pos - 30 - 50
        self.x_arrow.rect.x = pos - 50
        self.y_arrow.rect.x = pos- 30 - 50

    def y_move_entity_to(self, pos):
        self.move_entity[0].rect.y = pos# - self.move_entity[0].height - 50
        self.main_arrow.rect.y = pos + 30
        self.x_arrow.rect.y = pos
        self.y_arrow.rect.y = pos - 100


    def mainloop(self):
        while self.run:

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.run = False
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.y_moving = False
                    self.x_moving = False
                    self.moving = False

                    pos = pygame.mouse.get_pos()
                    if pos[0] > 610 and pos[0] < pygame.display.Info().current_w - 500:

                        if not self.main_arrow.rect.collidepoint(pos) and not self.y_arrow.rect.collidepoint(pos) and not self.x_arrow.rect.collidepoint(pos):
                            self.view_entity_info(pos)
                        else:
                            if self.main_arrow.rect.collidepoint(pos):
                                self.moving = False
                            if self.x_arrow.rect.collidepoint(pos):
                                self.x_moving = False
                            if self.y_arrow.rect.collidepoint(pos):
                                self.y_moving = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if not self.hidden:
                        if self.main_arrow.rect.collidepoint(pos):
                            self.moving = True
                            self.move_entity = self.Ecs.get_closest(pos)

                        if self.x_arrow.rect.collidepoint(pos):
                            self.x_moving = True
                            self.move_entity = self.Ecs.get_closest(pos)

                        if self.y_arrow.rect.collidepoint(pos):
                            self.y_moving = True
                            self.move_entity = self.Ecs.get_closest(pos)

            if self.moving:
                posit = pygame.mouse.get_pos()
                self.main_move_entity_to(posit)

            if self.x_moving:
                posit = pygame.mouse.get_pos()
                self.x_move_entity_to(posit[0])

            if self.y_moving:
                posit = pygame.mouse.get_pos()
                self.y_move_entity_to(posit[1])

            # Clearing
            self.main_window.clear(255, 255, 255)
            # Rendering
            # Entity rendering go here
            self.Ecs.render()
            # Entity Info


            # Gui layout
            if not self.entity_frame.disable_children:
                self.extra_menu.render()
            self.entity_frame.render()
            self.toggle_frame.render()
            self.info_frame.render()
            # UI RENDER
            if self.show_info:
                self.x_text.parent_draw()
                self.y_text.parent_draw()
                self.sprite_text.parent_draw()
                self.width_text.parent_draw()
                self.height_text.parent_draw()


            # Other


            # hide entity check
            if self.hidden:
                self.toggle_button.text_object.text = "^"
                self.entity_frame.disable_children = True
                self.show_info = False
                if self.entity_frame.width != 0:
                    self.entity_frame.width -= 7 * self.speed
                if self.info_frame.width != 0:
                    self.info_frame.width -= 10 * self.speed

            elif not self.hidden:
                self.toggle_button.text_object.text = ">"

                if self.entity_frame.width != 400:
                    self.entity_frame.width += 7 * self.speed
                else:
                    self.entity_frame.disable_children = False
                    if self.x_text.text != "HEllo world":
                        self.show_info = True
                if self.info_frame.width != 500:
                    self.info_frame.width += 10 * self.speed

            # Extra Menu Check
            if self.extra_menus:
                self.extra_menu_button.text_object.text = "-"
                self.extra_menu_button.text_object.position = (
                self.extra_menu_button.x + 15, self.extra_menu_button.y + 5)

                if self.extra_menu.width != 200:
                    self.extra_menu.width += 10
                else:
                    self.extra_menu.disable_children = False
                if self.extra_menu.height < 100:
                    self.extra_menu.height += 10

            if self.extra_menus == False:
                self.extra_menu_button.text_object.text = "="
                self.extra_menu_button.text_object.position = (
                self.extra_menu_button.x + 15, self.extra_menu_button.y + 5)
                self.extra_menu.disable_children = True
                if self.extra_menu.width > 0:
                    self.extra_menu.width -= 10
                if self.extra_menu.height != 0:
                    self.extra_menu.height -= 3

            if not self.hidden:
                self.x_arrow.render()
                self.y_arrow.render()
                self.main_arrow.render()
            # window update
            self.main_window.update()


if __name__ == "__main__":
    editor = Editor()
    editor.mainloop()
