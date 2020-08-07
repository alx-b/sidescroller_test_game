import pyglet

from resource import PlayerResource


class Player:
    def __init__(self, x, y):
        self.key_handler = pyglet.window.key.KeyStateHandler()

        self.sprite = pyglet.sprite.Sprite(PlayerResource.idle_anim, x=x, y=y)
        self.attack_zone = pyglet.sprite.Sprite(
            PlayerResource.attack_slash_anim,
            x=(self.sprite.x + self.sprite.width),
            y=(self.sprite.y),
        )
        self.attack_zone.visible = False

        self.shape_collision = pyglet.shapes.Rectangle(x=x, y=y, width=6, height=8)
        self.shape_collision.anchor_position = (
            self.shape_collision.width // 2,
            self.shape_collision.height // 2,
        )
        self.shape_collision.position = (x, y)
        self.shape_collision.opacity = 0  # 0 to 255

        self.can_move = True
        self.is_facing_right = True
        self.is_jumping = False
        self.mass = 10
        self.velocity = 20
        self.speed_right = 60
        self.speed_left = 60

    def set_idle_anim(self, dt):
        self.attack_zone.visible = False
        self.set_animation(PlayerResource.idle_anim)
        self.can_move = True

    def set_idle_anim_left(self, dt):
        self.attack_zone.visible = False
        self.set_animation(PlayerResource.idle_anim.get_transform(flip_x=True))
        self.can_move = True

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.Z:
            self.is_jumping = True
        if symbol == pyglet.window.key.X and self.can_move:
            self.attack_zone.visible = True
            self.can_move = False
            if self.is_facing_right:
                pyglet.clock.schedule_once(self.set_idle_anim, 0.4)
                self.set_animation(PlayerResource.attack_anim)
                self.set_attack_animation(PlayerResource.attack_slash_anim)
            elif not self.is_facing_right:
                pyglet.clock.schedule_once(self.set_idle_anim_left, 0.4)
                self.set_animation(
                    PlayerResource.attack_anim.get_transform(flip_x=True)
                )
                self.set_attack_animation(
                    PlayerResource.attack_slash_anim.get_transform(flip_x=True)
                )

        if (
            symbol == pyglet.window.key.RIGHT
            and not self.key_handler[pyglet.window.key.LEFT]
        ):
            self.attack_zone.visible = False
            self.is_facing_right = True
            self.set_animation(PlayerResource.run_anim)
        elif (
            symbol == pyglet.window.key.LEFT
            and not self.key_handler[pyglet.window.key.RIGHT]
        ):
            self.attack_zone.visible = False
            self.is_facing_right = False
            self.set_animation(PlayerResource.run_anim.get_transform(flip_x=True))

    def on_key_release(self, symbol, modifiers):
        if (
            symbol == pyglet.window.key.RIGHT
            and not self.key_handler[pyglet.window.key.LEFT]
        ):
            self.set_animation(PlayerResource.idle_anim)
        elif (
            symbol == pyglet.window.key.LEFT
            and not self.key_handler[pyglet.window.key.RIGHT]
        ):
            self.set_animation(PlayerResource.idle_anim.get_transform(flip_x=True))

    def get_right_side(self):
        return self.shape_collision.x + (self.shape_collision.width // 2)

    def get_bottom_side(self):
        return self.shape_collision.y - (self.shape_collision.height // 2)

    def get_left_side(self):
        return self.shape_collision.x - (self.shape_collision.width // 2)

    def get_top_side(self):
        return self.shape_collision.y + (self.shape_collision.height // 2)

    def draw(self):
        self.attack_zone.draw()
        self.sprite.draw()
        self.shape_collision.draw()

    def update(self, dt):
        if self.is_jumping:
            self.jump(dt)
        self.move(dt)
        self.sprite.x = self.shape_collision.x
        self.sprite.y = self.shape_collision.y
        if self.is_facing_right:
            self.attack_zone.x = self.sprite.x + self.sprite.width
            self.attack_zone.y = self.sprite.y
        else:
            self.attack_zone.x = self.sprite.x - self.sprite.width
            self.attack_zone.y = self.sprite.y

    def move(self, dt):
        if (
            self.key_handler[pyglet.window.key.RIGHT]
            and self.can_move
            and not self.key_handler[pyglet.window.key.LEFT]
        ):
            self.is_facing_right = True
            self.shape_collision.x += self.speed_right * dt

        elif (
            self.key_handler[pyglet.window.key.LEFT]
            and self.can_move
            and not self.key_handler[pyglet.window.key.RIGHT]
        ):
            self.is_facing_right = False
            self.shape_collision.x -= self.speed_left * dt

    def jump(self, dt):
        """ Fake physics to simulate a jump """
        force = self.mass * self.velocity
        # if force >= 0:
        #    self.set_animation(PlayerResource.jump_anim)
        # else:
        #    self.set_animation(PlayerResource.jump_fall_anim)

        self.shape_collision.y += force * dt
        self.velocity -= 1.5

    def set_animation(self, animation, dt=0):
        self.sprite.image = animation

    def set_attack_animation(self, animation):
        self.attack_zone.image = animation
