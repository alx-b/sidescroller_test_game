import pyglet

from resource import EnemyResource


class Enemy:
    def __init__(self, x, y, batch=None, group=None):
        self.sprite = pyglet.sprite.Sprite(
            EnemyResource.idle_anim, x=x, y=y, batch=batch, group=group
        )

    def is_dead(self):
        print("IM DEAD")
        self.sprite.delete()

    def move_left(self, speed, dt):
        self.sprite.x -= speed * dt

    def move_right(self, speed, dt):
        self.sprite.x += speed * dt

    def get_right_side(self):
        return self.sprite.x + self.sprite.width // 2

    def get_left_side(self):
        return self.sprite.x - self.sprite.width // 2

    def get_top_side(self):
        return self.sprite.y + self.sprite.height // 2

    def get_bottom_side(self):
        return self.sprite.y - self.sprite.height // 2

    def set_animation(self, anim):
        self.sprite.image = anim
