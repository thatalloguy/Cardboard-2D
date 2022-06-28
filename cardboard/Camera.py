
class Camera:
    def __init__(self,pos,zoom):
        self.zoom = zoom
        self.cam_x = pos[0]
        self.cam_y = pos[1]

    def get_pos(self):
        return self.cam_x, self.cam_y

    def set_x(self, x):
        self.cam_x = x


    def set_y(self, y):
        self.cam_x = y


    def move_x(self, x):
        self.cam_x += x

    def move_y(self, y):
        self.cam_x += y

    def zoom_in(self,zoom):
        if self.zoom > 1 or self.zoom == 1:
            self.zoom += zoom
        else:
            self.zoom = 1

    def get_zoom(self):
        return self.zoom