import pygame.mouse
import tkinter
import tkinter.filedialog
from cardboard import *
import json
import threading
import random
import os
from bisect import bisect_left
import subprocess
# import pygame
def take_closest(myList, myNumber):
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

def prompt_file():
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

class Ecs:
    def __init__(self,camera):


        self.data = {}
        self.dragging = False
        self.x = []
        self.y = []
        self.sprites = []
        self.width = []
        self.heights = []
        self.camera = camera
        self.id = 0
        self.ids = []
        self.deletes = []
        self.entities = []
        self.move_entity = None

    def get(self,id):
        return self.data[str(id)]

    def add_entity(self, entity):
        self.x.append(entity.rect.x)
        self.y.append(entity.rect.y)
        self.sprites.append(entity.path)
        self.width.append(entity.width)
        self.heights.append(entity.height)
        self.deletes.append(entity.destroyed)
        self.data[self.id] = [entity.rect.x,entity.rect.y,entity.path,entity.width,entity.height,entity.destroyed]
        entity.id = self.id
        self.id += 1
        self.entities.append(entity)

        return self.id

    def render(self):
        for entity in self.entities:
            entity.render()

    def get_all(self):
        return self.data

    def update(self,entity):
        self.data[entity.id] = [entity.rect.x -  self.camera.cam_x, entity.rect.y -  self.camera.cam_y, entity.path, entity.width, entity.height,entity.destroyed]
        #print(str(entity.id))
        self.entities[entity.id] = entity

    def on_click(self):
        pos = pygame.mouse.get_pos()
        for entity in self.entities:
            if entity.rect.collidepoint(pos):
                #print(str(entity.id))
                self.move_entity = self.entities[entity.id]
                self.dragging = True

                return self.move_entity

    def on_drag(self,pos):
        if self.move_entity != None and self.dragging:
            self.move_entity.x = pos[0] - self.move_entity.width / 2 - self.camera.cam_x
            self.move_entity.y = pos[1] - self.move_entity.height / 2 - self.camera.cam_y
            self.update(self.move_entity)
            return self.move_entity

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

    def reset(self):
        self.data = {}
        self.dragging = False
        self.x = []
        self.y = []
        self.sprites = []
        self.width = []
        self.heights = []
        self.id = 0
        self.ids = []
        self.deletes = []
        self.entities = []
        self.move_entity = None


class Editor:
    def __init__(self):
        self.main_window = Board(pygame.display.Info().current_w, pygame.display.Info().current_h - 50,
                                 title="A editor probably",bg=(0, 51, 153))

        # Setup Gui frames
        self.entity_frame = Frame((5, 5), 400, 300, color=(128, 128, 128))
        self.info_frame = Frame((pygame.display.Info().current_w - 500, 5), 500, pygame.display.Info().current_h - 5,
                                color=(128, 128, 128))
        self.toggle_frame = Frame((0, 0), 0, 0)
        self.toggle_button = Button(self.entity_frame.x, self.entity_frame.y, 50, 50, ">", toggle=True,
                                    command=self.hide_main_menus,font='cardboard/fonts/FFFFORWA.TTF', offset_x=15,offset_y=5)
        self.toggle_button.text_object.position = (self.toggle_button.x + 15, self.toggle_button.y + 5)
        self.toggle_button.text_object.color1 = (0, 0, 0)
        self.toggle_frame.add_child(self.toggle_button)
        # Editor Variables
        self.hidden = False
        self.extra_menus = False
        self.run = True
        self.id = 0
        self.camera = Camera((0, 0), 100)
        self.Ecs = Ecs(self.camera)
        self.speed = 4
        self.all_entities = []
        self.all_tools = []
        self.monitor_height = pygame.display.Info().current_h - 5
        self.monitor_width = pygame.display.Info().current_w - 5

        # Toolssss
        self.x_arrow = Tool(500,500,200,100,"editor_gui/arrow_left.png",debug_rendering=True)

        # MORE UI
        # CreateButton
        self.createbutton = Button(self.entity_frame.x + 175, self.entity_frame.y, 50, 50, "+",
                                   command=self.Create_test_entity,font='cardboard/fonts/FFFFORWA.TTF', offset_x=15,offset_y=5)
        self.createbutton.text_object.position = (self.createbutton.x + 15, self.createbutton.y + 5)
        self.createbutton.text_object.color1 = (0, 0, 0)
        self.entity_frame.add_child(self.createbutton)

        # tool buttons
        self.move_button = Button(self.entity_frame.x,self.entity_frame.y + 60,120,50,"Debug",toggle=True,command=self.toggle_move)
        self.move_button.text_object.position = (self.move_button.x + 4, self.move_button.y + 5)
        self.move_button.text_object.color1 = (0, 0, 0)
        self.entity_frame.add_child(self.move_button)
        # Extra Menu Button
        self.extra_menu_button = Button(self.entity_frame.x + 350, self.entity_frame.y, 50, 50, "=", toggle=True,
                                        command=self.hide_extra_menus,font='cardboard/fonts/FFFFORWA.TTF', offset_x=15,offset_y=5)
        self.extra_menu_button.text_object.position = (self.extra_menu_button.x + 15, self.extra_menu_button.y + 5)
        self.extra_menu_button.text_object.color1 = (0, 0, 0)
        self.entity_frame.add_child(self.extra_menu_button)

        # -- Extra Menu Frame
        self.extra_menu = Frame((405, 5), 0, 0, color=(51, 51, 51))
        self.save_button = Button(self.extra_menu.x - 5, self.extra_menu.y, 205, 50, "Save Project",
                                  command=self.save_project)
        self.save_button.text_object.size = 128
        self.save_button.text_object.position = (self.entity_frame.x + 5, self.entity_frame.y + 200)
        self.save_button.text_object.color1 = (0, 0, 0)
        self.extra_menu.add_child(self.save_button)
        # Open button
        self.open_button = Button(self.extra_menu.x - 5, self.extra_menu.y + 55, 205, 50, "Open Project",
                                  command=self.open_project)
        self.open_button.text_object.size = 128
        self.open_button.text_object.position = (self.open_button.x, self.open_button.y)
        self.open_button.text_object.color1 = (0, 0, 0)
        self.new_button = Button(self.extra_menu.x - 5, self.extra_menu.y + 110, 205, 50, "New Project",command=self.new_project)
        self.new_button.text_object.color1 = (0,0,0)
        self.extra_menu.add_child(self.open_button)
        self.extra_menu.add_child(self.new_button)

        # Error Gui
        self.message = "ERROR: ERROR NO ERROR MESSAGE"
        self.message_type = "ERROR"
        self.show_message = False
        self.message_box = Tool(0,self.monitor_height,300,200,color=(255, 77, 77))
        self.message_button = Button(self.message_box.rect.x + 250,self.message_box.rect.y + 200,50,50,"x",offset_x=15,command=self.dismiss_message,font='cardboard/fonts/FFFFORWA.TTF')
        self.message_button.text_object.color1 = (0,0,0)
        self.message_text = Text(self.message,500,500,color1=(0,0,0))
        # Entity Info
        self.x_text = Text("HEllo world",self.info_frame.x+ 10,self.info_frame.y + 10,color1=(0,0,0),size=64)
        self.x_entry = Entry(self.x_text.x + 60, self.x_text.y + 15,200,50)
        self.y_text = Text("HEllo world", self.info_frame.x + 10, self.info_frame.y + 65, color1=(0, 0, 0), size=64)
        self.y_entry = Entry(self.y_text.x + 60, self.y_text.y + 15, 200, 50)
        self.sprite_text = Text("HEllo world", self.info_frame.x + 10, self.info_frame.y + 120, color1=(0, 0, 0), size=64)
        self.width_text = Text("HEllo world", self.info_frame.x + 10, self.info_frame.y + 180, color1=(0, 0, 0), size=64)
        self.width_entry = Entry(self.width_text.x + 225, self.width_text.y + 15, 200, 50)
        self.height_text = Text("HEllo world", self.info_frame.x + 10, self.info_frame.y + 235, color1=(0, 0, 0), size=64)
        self.height_entry = Entry(self.height_text.x + 230, self.height_text.y + 15, 200, 50)
        self.change_w = Button(self.width_entry.input_rect.x + self.width_entry.input_rect.w + 5, self.width_entry.input_rect.y,50,50,"o",offset_x=15,command=self.change_size_via_info_frame)
        self.change_w.text_object.color1 = (0,0,0)
        self.change_h = Button(self.height_entry.input_rect.x + self.height_entry.input_rect.w + 5,
                               self.height_entry.input_rect.y, 50, 50, "o", offset_x=15)
        self.change_sprite = Button(self.sprite_text.x + 400,self.sprite_text.y + 15, 50, 50, "o", offset_x=15)
        self.change_sprite.text_object.color1 = (0,0,0)

        self.remove_button = Button(self.info_frame.x + 5,self.info_frame.y + self.info_frame.height - 100,150,50,"Remove",offset_x=5)
        self.remove_button.text_object.color1 = (0,0,0)
        self.change_h.text_object.color1 = (0, 0, 0)

        # Settings UI
        self.settings_frame = Frame((self.entity_frame.x + self.entity_frame.width,self.entity_frame.y),1015,700,color=(51, 51, 51))
        self.settings_Text = Text("Settings",self.settings_frame.x + 5,self.settings_frame.y + 5)
        self.settings_frame.add_child(self.settings_Text)
        self.settings_button = Button(self.move_button.x+ 120,self.move_button.y,150,50,"Settings",offset_x=5,offset_y=5,command=self.toggle_settings,toggle=True)
        self.settings_button.text_object.color1 = (0,0,0)
       # self.entity_frame.add_child(self.settings_button)

        # All the different Settings UI
        self.sky_text = Text("Sky Color:",self.settings_frame.x + 5,self.settings_frame.y + 100)
        self.red_entry = Entry(self.sky_text.x + 170,self.sky_text.y,50,50,text="204, 255, 255")
        self.settings_frame.add_child(self.sky_text)
        self.apply_button = Button(self.settings_frame.x + self.settings_frame.width - 105, self.settings_frame.y + self.settings_frame.height - 55,100,50,"apply",offset_x=5)
        self.apply_button.text_object.color1 = (0,0,0)
        self.settings_frame.add_child(self.apply_button)
        # Build / Run UI and other
        self.build_button = Button(self.entity_frame.x, self.entity_frame.y + 125, 100,50,"build",offset_x=5,command=self.build_project)
        self.build_button.text_object.color1 = (0,0,0)
        self.run_button = Button(self.entity_frame.x + 105, self.entity_frame.y + 125, 75, 50, "run", offset_x=5,command=self.run_project)
        self.run_button.text_object.color1 = (0, 0, 0)
        self.entity_frame.add_child(self.build_button)
        self.entity_frame.add_child(self.run_button)

        #  Camera UI'ss
        self.reset_button = Button(self.entity_frame.x, self.entity_frame.y + 180,185,50,"Reset View",offset_x=5,command=self.reset_view)
        self.reset_button.text_object.color1 = (0,0,0)
        self.entity_frame.add_child(self.reset_button)
        self.camera_data = {}

        # Script UI
        self.new_script_button = Button(self.entity_frame.x, self.entity_frame.y + 235,305,50,"Create New Script",offset_x=10,command=self.create_new_script)
        self.new_script_button.text_object.color1 = (0,0,0)
        self.entity_frame.add_child(self.new_script_button)
        self.open_script_button = Button(self.entity_frame.x + 190, self.entity_frame.y + 180, 205, 50, "Open Script",offset_x=10, command=self.Open_a_script)
        self.open_script_button.text_object.color1 = (0, 0, 0)
        self.entity_frame.add_child(self.new_script_button)
        self.entity_frame.add_child(self.open_script_button)

        self.script_lists = {}
        self.script_count = 0


        self.show_info = False
        self.changing = False
        self.rectangle_draging = False
        self.move_mode = False
        self.show_settings = False
        self.debug = False
        self.check_for_new_project = False
        self.first_loop = True
        self.created_new_project = False
        self.workspace = False
        self.moving_camera = False
        # The Actaul game

    def save_project(self):
        if not self.workspace:
            self.new_project()
            self.save_project()
        else:
            with open("projects/" + self.workspace + "/game_data.json", "w") as write_file:
                write_file.write(json.dumps(self.Ecs.data))#, sort_keys=True, indent=2, ensure_ascii=True))
                self.Show_message("Saved project","MESSAGE")
                write_file.close()
            if self.camera_data == {}:
                self.camera_data[0] = self.camera.cam_x
                self.camera_data[1] = self.camera.cam_y
                self.camera_data[3] = self.camera.zoom
            with open("projects/" + self.workspace + "/data/camera_data.json", "w") as write_file:
                write_file.write(json.dumps(self.camera_data))#, sort_keys=True, indent=2, ensure_ascii=True))
                write_file.close()

            with open("projects/" + self.workspace + "/data/script_data.json", "w") as write_file:
                write_file.write(json.dumps(self.script_lists))#, sort_keys=True, indent=2, ensure_ascii=True))
                write_file.close()

    def open_project(self):
        for entity in self.Ecs.entities:
            entity.destroy()
        self.imtrying = prompt_file()
        self.workspace = os.path.dirname(self.imtrying).split("/")[-1]
        with open("projects/" + self.workspace + "/game_data.json", "r") as file:
            data = json.load(file)
            file.close()

        with open("projects/" + self.workspace + "/data/camera_data.json", "r") as le_file:
            camera_data = json.load(le_file)
            le_file.close()

        with open("projects/" + self.workspace + "/data/script_data.json", "r") as le_file:
            self.script_lists = json.load(le_file)
            le_file.close()

        for i in self.script_lists:
            self.script_count += 1
        self.Ecs.reset()
        self.camera_data = camera_data
        self.camera.cam_x = self.camera_data["0"]
        self.camera.cam_y = self.camera_data["1"]


        self.Ecs.data = data
        self.Create_new_entity_from_data(data)
        #self.camera.zoom = self.camera_data[2]

        #try:
        #    with open("projects/" + self.workspace + "/game_data.json", "r") as file:
        #        data = json.load(file)
        #        file.close()
        #    self.Ecs.data = data
        #    self.Create_new_entity_from_data(data)
        #except Exception as e:
        #    self.Show_message(str(e),"ERROR")

    def new_project(self):
        self.select_window = tkinter.Tk()
        self.select_window.title("Name Of Your New Project")
        self.select_window.geometry("400x100+500+500")
        self.select_window.iconbitmap("cardboard/images/logo.ico")
        new_name = tkinter.Entry(self.select_window,width=400,font=("default",56))
        new_name.place(width=350, height=100)
        self.name_button = tkinter.Button(self.select_window,text="Done",width=50,command=lambda: self.Setup_new_project(new_name.get())).place(width=50,height=100,x=350,y=0)
        self.select_window.resizable(False,False)
        #new_name = new_name.get()
        self.select_window.mainloop()

    def build_project(self):
        if self.workspace != False:
            try:
                # Import Files
                with open("editor_data/build_Config.py", "r") as file:
                    build_config = file.read()
                    file.close()

                with open("editor_data/settings.py", "r") as file:
                    settings_file = file.read()
                    file.close()

                # Write / Convert Files
                with open("projects/" + self.workspace + "/game.py", "w") as file:
                    file.write(build_config)
                    file.close()

                with open("projects/" + self.workspace + "/settings.py", "w") as file:
                    file.write(settings_file)
                    file.close()
                self.Show_message("Builded project","MESSAGE")
            except Exception as e:
                self.Show_message(str(e),"ERROR")


        else:
            self.save_project()
            self.build_project()

    def run_project(self):
        print("RUN")
        if self.workspace != False:
            self.save_project()
            os.system("python " + "projects/" + self.workspace + "/game.py " + self.workspace)
        else:
            self.save_project()
            self.build_project()
            self.run_project()

    def Open_a_script(self):
        name = prompt_file().replace("\\","/")
        name = os.path.basename(name).split(".")[0]
        try:
            if name != True:
                x = threading.Thread(target=lambda: self.open_script(name))
                x.start()
        except Exception as e:
            print(str(e))
            self.Show_message("Please Install Python 3.7", "WARNING")

    def create_new_script(self):
        self.script_window = tkinter.Tk()
        self.script_window.title("Name Of Your New Script")
        self.script_window.geometry("400x100+1000+700")
        self.script_window.iconbitmap("cardboard/images/logo.ico")
        new_name = tkinter.Entry(self.script_window, width=400, font=("default", 56))
        new_name.place(width=350, height=100)
        name_button = tkinter.Button(self.script_window, text="Done", width=50,command=lambda: self.Setup_new_script(new_name.get())).place(width=50,height=100,x=350, y=0)
        self.script_window.resizable(False, False)
        # new_name = new_name.get()
        self.script_window.mainloop()

    def open_script(self,name):
        os.system("python -m idlelib " + os.getcwd().replace("\\", "/") + "/projects/" + self.workspace + "/scripts/" + str(name) + ".py")

    def Setup_new_script(self,name):
        self.script_window.destroy()
        if self.workspace == False:
            self.save_project()
        else:

            with open("editor_data/script_config.py", "r") as file:
                script_config = file.readlines()
                file.close()

            with open("projects/" + self.workspace + "/scripts/" + str(name) + ".py", "w") as file:
                script_config[1] = "from projects." + str(self.workspace) + ".game import *\n"
                file.writelines(script_config)
                file.close()

            self.script_lists[self.script_count] = str(name)
            self.script_count += 1

            try:
                x = threading.Thread(target=lambda: self.open_script(name))
                x.start()
            except Exception as e:
                print(str(e))
                self.Show_message("Please Install Python 3.7", "WARNING")

    def Setup_new_project(self,name):
        self.select_window.destroy()
        try:
            os.makedirs("projects/" + name)
            os.makedirs("projects/" + name + "/" + "scripts")
            os.makedirs("projects/" + name + "/" + "images")
            os.makedirs("projects/" + name + "/" + "data")
            self.workspace = name
            self.Ecs.reset()
            print(self.workspace)


        except Exception as e:
            self.Show_message(str(e), "ERROR")

    def Create_new_entity_from_data(self,data):
        count  = 0
        for i in range(10000):
            new_x = data[str(count)][0]
            new_y = data[str(count)][1]
            new_path = data[str(count)][2]
            new_width = data[str(count)][3]
            new_height = data[str(count)][4]
            is_destroyed = data[str(count)][5]
            # add the offsetmonkey
            if not is_destroyed:
                self.new_entity = Entity(self.camera, (new_x - self.camera.cam_x,new_y - self.camera.cam_y),Sprite(path=str(new_path)), new_width, new_height)
                self.new_entity.destroyed = is_destroyed
                self.Ecs.add_entity(self.new_entity)
            count += 1

    def reset_view(self):
        self.camera.set_x(0)
        self.camera.set_y(0)

    def toggle_move(self):
        if self.debug:
            for entity in self.Ecs.entities:
                entity.debug_rendering = False
                self.debug = False

            for tool in self.all_tools:
                tool.debug_rendering = True
        else:
            for entity in self.Ecs.entities:
                entity.debug_rendering = True
                self.debug = True

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
            self.selected_entity = pos
        except:
            self.Show_message("Cant find entity","ERROR")
        if found and self.selected_entity != None:
            self.x_text.text = "X: "# + str(self.selected_entity.x)
            self.x_entry.user_text = str(self.selected_entity.rect.x)
            self.y_text.text = "Y: "# + str(self.selected_entity.y)
            self.y_entry.user_text = str(self.selected_entity.rect.y)
            self.sprite_text.text = "Sprite: " + str(self.selected_entity.path)
            self.width_text.text = "Width: "# + str(self.selected_entity.width)
            self.width_entry.user_text = str(self.selected_entity.width)
            self.height_text.text = "Height: "# + str(self.selected_entity.height)
            self.height_entry.user_text = str(self.selected_entity.height)
            self.show_info = True
            self.x_arrow.rect.x = self.selected_entity.x
            self.x_arrow.rect.y = self.selected_entity.y - 25
            self.change_w.command = lambda: self.change_size_via_info_frame(pos)
            self.change_h.command = lambda: self.change_size_via_info_frame(pos)
            self.remove_button.command = lambda: self.remove_entity(pos)
            self.change_sprite.command = lambda: self.Change_sprite(pos)

    def remove_entity(self,entity):
        entity.destroyed = True
        self.show_info = False
        self.Ecs.update(entity)

    def Change_sprite(self,entity):
        self.new_sprite_file = prompt_file()
        print(self.new_sprite_file)
        entity.path = self.new_sprite_file
        self.Ecs.update(entity)

    def dismiss_message(self):
        self.show_message = False

    def change_size_via_info_frame(self,entity):
        try:
            entity.width = int(self.width_entry.user_text)
            entity.height = int(self.height_entry.user_text)
            self.Ecs.update(entity)
        except Exception as e:
            self.Show_message(str(e),"ERROR")

    def Show_message(self,message,type):
        self.message = message
        self.message_type = type
        self.show_message  = True

    def toggle_settings(self):
        if self.show_settings:
            self.show_settings = False
        else:
            self.show_settings = True

    def mainloop(self):
        while self.run:

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.run = False
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.Ecs.dragging = False
                    elif event.button == 3:
                        self.moving_camera = False
                        self.camera_data[0] = self.camera.cam_x
                        self.camera_data[1] = self.camera.cam_y
                        self.camera_data[2] = self.camera.zoom

                    pos = pygame.mouse.get_pos()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if not self.hidden:
                        if event.button == 1:
                            self.entity_info = self.Ecs.on_click()
                            self.view_entity_info(self.entity_info)
                        if event.button == 3:
                            self.moving_camera = True



                elif event.type == pygame.MOUSEMOTION and not self.moving_camera:

                    mouse_x, mouse_y = event.pos
                    if not self.hidden:
                        self.entity_info = self.Ecs.on_drag(event.pos)
                        self.view_entity_info(self.entity_info)

                        #self.x_arrow.rect.y = mouse_y + self.offset_y
                elif event.type == pygame.MOUSEMOTION and self.moving_camera:
                    mouse_x, mouse_y = event.pos
                    self.camera.set_x(mouse_x - self.monitor_width /2 )
                    self.camera.set_y(mouse_y - self.monitor_height / 2)
                    self.camera_data[0] = self.camera.cam_x
                    self.camera_data[1] = self.camera.cam_y
                    self.camera_data[2] = self.camera.zoom

            if self.first_loop:
                self.first_loop = False
                self.Show_message("Hello World","MESSAGE")

            if self.show_message:
                self.message_text.text = self.message
                if self.message_type == "ERROR":
                    self.message_box.color = (255,77,77)
                elif self.message_type == "WARNING":
                    self.message_box.color = (255, 198, 26)
                elif self.message_type == "MESSAGE":
                    self.message_box.color = (0, 153, 255)
                self.message_text.x = self.message_box.rect.x
                self.message_text_pos = self.message_box.rect.y + 60
                self.message_text.y = self.message_text_pos
                if self.message_box.rect.y != self.monitor_height - 200:
                    self.message_box.rect.y -= 10
                if self.message_button.rect.y != self.monitor_height - 200:
                    self.message_button.rect.y -= 10


            if not self.show_message:
                if self.message_box.rect.y != self.monitor_height:
                    self.message_box.rect.y += 10
            # Clearing
            self.main_window.clear(204, 255, 255)
            # Rendering
            # Entity rendering go here
            self.Ecs.render()
            # Entity Info

            #if self.show_settings:# and not self.hidden:
            #    self.settings_frame.render()
            #    self.red_entry.handle(events)
            # Gui layout
            if not self.entity_frame.disable_children:
                self.extra_menu.render()
            self.entity_frame.render()
            self.toggle_frame.render()
            self.info_frame.render()
            # UI RENDER
            if self.show_info:
                self.x_text.parent_draw()
                self.x_entry.handle(events)
                self.y_text.parent_draw()
                self.y_entry.handle(events)
                self.sprite_text.parent_draw()
                self.width_text.parent_draw()
                self.width_entry.handle(events)
                self.height_text.parent_draw()
                self.height_entry.handle(events)
                self.change_h.parent_draw()
                self.change_w.parent_draw()
                self.remove_button.parent_draw()
                self.change_sprite.parent_draw()

            # Other
            # hide entity check
            if self.hidden:
                for entity in self.Ecs.entities:
                    entity.debug_rendering = False
                self.toggle_button.text_object.text = "^"
                self.entity_frame.disable_children = True
                self.entity_frame.width = 0
                self.info_frame.width = 0
                self.show_info = False
                #if self.entity_frame.width != 0:
                #    self.entity_frame.width -= 7 * self.speed
                #if self.info_frame.width != 0:
                #    self.info_frame.width -= 10 * self.speed

            elif not self.hidden:
                self.toggle_button.text_object.text = ">"
                self.entity_frame.width = 400
                self.info_frame.width = 500
                self.entity_frame.disable_children = False
                if self.debug:
                    for entity in self.Ecs.entities:
                        entity.debug_rendering = True
                #self.show_info = True
                #if self.entity_frame.width < 400:
                #    self.entity_frame.width += 7 * self.speed
                #else:
                #    if self.entity_frame.width != 400:
                #        self.entity_frame.width = 400
                #    if self.debug:
                #        for entity in self.Ecs.entities:
                #            entity.debug_rendering = True
                #    self.entity_frame.disable_children = False
                #    if self.x_text.text != "HEllo world":
                #        self.show_info = True
                #if self.info_frame.width <= 500:
                #    self.info_frame.width += 10 * self.speed

            # Extra Menu Check
            if self.extra_menus:
                self.extra_menu_button.text_object.text = "-"
                self.extra_menu_button.text_object.position = (
                self.extra_menu_button.x + 15, self.extra_menu_button.y + 5)

                if self.extra_menu.width != 200:
                    self.extra_menu.width += 10
                else:
                    if self.extra_menu.width != 200 :
                        self.extra_menu.width = 200
                    self.extra_menu.disable_children = False
                if self.extra_menu.height != 160:# or self.extra_menu.height != 100:
                    self.extra_menu.height += 5
                else:
                    if self.extra_menu.height != 160:
                        self.extra_menu.height = 160

            if self.extra_menus == False:
                self.extra_menu_button.text_object.text = "="
                self.extra_menu_button.text_object.position = (
                self.extra_menu_button.x + 15, self.extra_menu_button.y + 5)
                self.extra_menu.disable_children = True
                if self.extra_menu.width > 0:
                    self.extra_menu.width -= 10
                else:
                    self.extra_menu.width = 0
                    self.extra_menu.height = 0
                if self.extra_menu.height != 0:
                    self.extra_menu.height -= 3
                else:
                    self.extra_menu.width = 0
                    self.extra_menu.height = 0

            if not self.hidden:
                self.message_box.render()
                if self.show_message:
                    self.message_button.parent_draw()
                    self.message_text.parent_draw()
            # window update
            self.main_window.update()

if __name__ == "__main__":
    editor = Editor()
    editor.mainloop()