import pyglet

from resource import PlayerResource
from attack_zone import AttackZone, CollisionShape


class Player:
    def __init__(self, x, y, batch=None, group=None):
        self.key_handler = pyglet.window.key.KeyStateHandler()

        self.sprite = pyglet.sprite.Sprite(
            PlayerResource.idle_anim, x=x, y=y, batch=batch, group=group
        )

        self.attack_zone = AttackZone(
            anim=PlayerResource.attack_slash_anim,
            x=(self.sprite.x + self.sprite.width),
            y=(self.sprite.y),
            batch=batch,
            group=group,
        )
        self.collision_shape = CollisionShape(
            x=x, y=y, width=6, height=8, batch=batch, group=group
        )

        self.can_move = True
        self.is_facing_right = True
        self.is_jumping = False
        self.is_attacking = False

        self.mass = 10
        self.velocity = 20
        self.speed_right = 60
        self.speed_left = 60

    def attack(self, objects):
        deads = []
        if self.attack_zone.is_visible():
            print("IM ATTAKING")
            for object in objects:
                if self.is_facing_right:
                    if (
                        object.get_left_side() < self.attack_zone.get_right_side()
                        and object.get_left_side() > self.attack_zone.get_left_side()
                        and object.get_top_side() > self.attack_zone.get_bottom_side()
                        and object.get_top_side() <= self.attack_zone.get_top_side()
                    ):
                        object.is_dead()
                        deads.append(object)
                else:
                    if (
                        object.get_right_side() > self.attack_zone.get_left_side()
                        and object.get_right_side() < self.attack_zone.get_right_side()
                        and object.get_top_side() > self.attack_zone.get_bottom_side()
                        and object.get_top_side() <= self.attack_zone.get_top_side()
                    ):
                        object.is_dead()
                        deads.append(object)
        for dead in deads:
            if dead in objects:
                objects.remove(dead)

        self.is_attacking = False
        return objects

    def set_idle_anim(self, dt):
        self.attack_zone.set_visibility(False)
        self.set_animation(PlayerResource.idle_anim)
        self.can_move = True

    def set_idle_anim_left(self, dt):
        self.attack_zone.set_visibility(False)
        self.set_animation(PlayerResource.idle_anim.get_transform(flip_x=True))
        self.can_move = True

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.Z:
            self.is_jumping = True
        if symbol == pyglet.window.key.X and self.can_move:
            self.attack_zone.set_visibility(True)
            self.is_attacking = True
            self.can_move = False
            if self.is_facing_right:
                pyglet.clock.schedule_once(self.set_idle_anim, 0.4)
                self.set_animation(PlayerResource.attack_anim)
                self.attack_zone.set_animation(PlayerResource.attack_slash_anim)
            elif not self.is_facing_right:
                pyglet.clock.schedule_once(self.set_idle_anim_left, 0.4)
                self.set_animation(
                    PlayerResource.attack_anim.get_transform(flip_x=True)
                )
                self.attack_zone.set_animation(
                    PlayerResource.attack_slash_anim.get_transform(flip_x=True)
                )

        if (
            symbol == pyglet.window.key.RIGHT
            and not self.key_handler[pyglet.window.key.LEFT]
        ):
            self.attack_zone.set_visibility(False)
            self.is_facing_right = True
            self.set_animation(PlayerResource.run_anim)
        elif (
            symbol == pyglet.window.key.LEFT
            and not self.key_handler[pyglet.window.key.RIGHT]
        ):
            self.attack_zone.set_visibility(False)
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

    def update(self, dt):
        if self.is_jumping:
            self.jump(dt)
        self.move(dt)
        self.sprite.update(
            x=self.collision_shape.get_x(), y=self.collision_shape.get_y()
        )
        if self.is_facing_right:
            self.attack_zone.update(
                x=self.sprite.x + self.sprite.width, y=self.sprite.y
            )
        else:
            self.attack_zone.update(
                x=self.sprite.x - self.sprite.width, y=self.sprite.y
            )

    def move(self, dt):
        if (
            self.key_handler[pyglet.window.key.RIGHT]
            and self.can_move
            and not self.key_handler[pyglet.window.key.LEFT]
        ):
            self.is_facing_right = True
            self.collision_shape.move_right(self.speed_right * dt)

        elif (
            self.key_handler[pyglet.window.key.LEFT]
            and self.can_move
            and not self.key_handler[pyglet.window.key.RIGHT]
        ):
            self.is_facing_right = False
            self.collision_shape.move_left(self.speed_left * dt)

    def jump(self, dt):
        """ Fake physics to simulate a jump """
        force = self.mass * self.velocity
        # if force >= 0:
        #    self.set_animation(PlayerResource.jump_anim)
        # else:
        #    self.set_animation(PlayerResource.jump_fall_anim)

        self.collision_shape.jump(force * dt)
        self.velocity -= 1.5

    def set_animation(self, animation, dt=0):
        self.sprite.image = animation

    def collision_check(self, colliders):
        return self.collision_shape.collision_check(self, colliders)
