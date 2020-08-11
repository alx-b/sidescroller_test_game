import pyglet


class Ground:
    def __init__(self, img, pos_x, pos_y, batch, group):
        self.sprite = pyglet.sprite.Sprite(
            img, x=pos_x, y=pos_y, batch=batch, group=group
        )

    def get_right_side(self):
        return self.sprite.x + self.sprite.width

    def get_bottom_side(self):
        return self.sprite.y

    def get_left_side(self):
        return self.sprite.x

    def get_top_side(self):
        return self.sprite.y + self.sprite.height

    def move_left(self, speed, dt):
        self.sprite.x -= speed * dt

    def move_right(self, speed, dt):
        self.sprite.x += speed * dt

    def get_x(self):
        return self.sprite.x

    def get_y(self):
        return self.sprite.y

    def get_width(self):
        return self.sprite.width

    def get_height(self):
        return self.sprite.height
