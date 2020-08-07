import pyglet

from resource import EnemyResource


class Enemy:
    def __init__(self, x, y):
        self.sprite = pyglet.sprite.Sprite(EnemyResource.idle_anim, x=x, y=y)
        # self.attack_zone = pyglet.sprite.Sprite(
        #    PlayerResource.attack_slash_anim,
        #    x=(self.sprite.x + self.sprite.width),
        #    y=(self.sprite.y),
        # )
        # self.attack_zone.visible = False

        # self.shape_collision = pyglet.shapes.Rectangle(x=x, y=y, width=6, height=6)
        # self.shape_collision.anchor_position = (
        #    self.shape_collision.width // 2,
        #    self.shape_collision.height // 2,
        # )
        # self.shape_collision.position = (x, y)
        # self.shape_collision.opacity = 150  # 0 to 255

    def draw(self):
        self.sprite.draw()
