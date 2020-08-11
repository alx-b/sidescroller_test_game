import pyglet


class AttackZone:
    def __init__(self, anim, x, y, batch=None, group=None):
        self.sprite = pyglet.sprite.Sprite(anim, x=x, y=y, batch=batch, group=group)
        self.sprite.visible = False

    def get_right_side(self):
        return self.sprite.x + (self.sprite.width // 2)

    def get_bottom_side(self):
        return self.sprite.y - (self.sprite.height // 2)

    def get_left_side(self):
        return self.sprite.x - (self.sprite.width // 2)

    def get_top_side(self):
        return self.sprite.y + (self.sprite.height // 2)

    def is_visible(self) -> bool:
        return True if self.sprite.visible else False

    def set_visibility(self, status: bool):
        self.sprite.visible = status

    def set_animation(self, anim):
        self.sprite.image = anim

    def update(self, x=None, y=None):
        self.sprite.update(x, y)


class CollisionShape:
    def __init__(self, x, y, width, height, batch=None, group=None):
        self.shape = pyglet.shapes.Rectangle(
            x=x, y=y, width=width, height=height, batch=batch, group=group
        )
        self.shape.anchor_position = (self.shape.width // 2, self.shape.height // 2)
        self.shape.opacity = 100  # 0 to 255

    def get_right_side(self):
        return self.shape.x + (self.shape.width // 2)

    def get_bottom_side(self):
        return self.shape.y - (self.shape.height // 2)

    def get_left_side(self):
        return self.shape.x - (self.shape.width // 2)

    def get_top_side(self):
        return self.shape.y + (self.shape.height // 2)

    def get_x(self):
        return self.shape.x

    def get_y(self):
        return self.shape.y

    def move_right(self, dt_speed):
        self.shape.x += dt_speed

    def move_left(self, dt_speed):
        self.shape.x -= dt_speed

    def jump(self, dt_force):
        self.shape.y += dt_force

    def collision_check(self, player, colliders):
        counter = 0
        for ground in colliders:
            # Not sure if that work but only do the collision detection if the
            # tile is close to the character (200x200)
            if (
                ground.get_x() > self.get_x() - 100
                and ground.get_x() < self.get_x() + 100
                and ground.get_y() > self.get_y() - 100
                and ground.get_y() < self.get_y() + 100
            ):
                if self.bottom_side_collide_with_object_top_side(ground):
                    counter += 1
                    player.is_jumping = False
                    player.velocity = 20
                    self.shape.y = (
                        ground.get_y() + ground.get_height() + self.shape.height // 2
                    )
                if self.right_side_collide_with_object_left_side(ground):
                    self.shape.x = ground.get_left_side() - self.shape.width // 2
                    player.speed_right = 0
                if self.left_side_collide_with_object_right_side(ground):
                    self.shape.x = (
                        ground.get_x() + ground.get_width() + self.shape.width // 2
                    )
                    player.speed_left = 0
                if self.top_side_collide_with_object_bottom_side(ground):
                    self.shape.y = ground.get_bottom_side() - self.shape.width // 2
                    # Knock back effect from hitting platform's bottom when jumping
                    player.velocity = -20
                    force = player.char.mass * player.velocity
                    self.shape.y += force * 1.0 / 120.0
                    player.velocity -= 2

                player.speed_right = 60
                player.speed_left = 60
        if counter > 0:
            return True
        else:
            return False

    def bottom_side_collide_with_object_top_side(self, object):
        if (
            self.get_bottom_side() <= object.get_top_side()
            and self.get_bottom_side() > object.get_bottom_side()
            and self.get_x() > object.get_left_side()
            and self.get_x() < object.get_right_side()
        ):
            return True
        return False

    def right_side_collide_with_object_left_side(self, object):
        if (
            self.get_right_side() >= object.get_left_side()
            and self.get_right_side() < object.get_right_side()
            and self.get_y() < object.get_top_side()
            and self.get_y() > object.get_bottom_side()
        ):
            return True
        return False

    def left_side_collide_with_object_right_side(self, object):
        if (
            self.get_left_side() <= object.get_right_side()
            and self.get_left_side() > object.get_left_side()
            and self.get_y() < object.get_top_side()
            and self.get_y() > object.get_bottom_side()
        ):
            return True
        return False

    def top_side_collide_with_object_bottom_side(self, object):
        if (
            self.get_top_side() >= object.get_bottom_side()
            and self.get_top_side() < object.get_top_side()
            and self.get_x() > object.get_left_side()
            and self.get_x() < object.get_right_side()
        ):
            return True
        return False
