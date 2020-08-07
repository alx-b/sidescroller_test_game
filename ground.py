import pyglet


class Ground:
    def __init__(self, img, pos_x, pos_y, grounds):
        self.sprite = pyglet.sprite.Sprite(img, x=pos_x, y=pos_y, batch=grounds)

    def get_right_side(self):
        return self.sprite.x + self.sprite.width

    def get_bottom_side(self):
        return self.sprite.y

    def get_left_side(self):
        return self.sprite.x

    def get_top_side(self):
        return self.sprite.y + self.sprite.height

    def draw(self):
        self.sprite.draw()

    def move_left(self, speed, dt):
        self.sprite.x -= speed * dt

    def move_right(self, speed, dt):
        self.sprite.x += speed * dt
