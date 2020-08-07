import pyglet

from player import Player
from ground import Ground
from resource import WorldResource
from enemy import Enemy


class Scene:
    def __init__(self):
        self.char = Player(112, 80)
        self.grounds = []
        self.undergrounds = []
        self.ground_batch = pyglet.graphics.Batch()
        self.level = self.get_level_layout()
        self.create_batch_sprite_from_level()
        self.enemy = Enemy(200, 30)

    def get_level_layout(self):
        """ Store the level layout from a file into a list. """
        level = []
        rows = []
        with open("level_layout.txt", "r", encoding="utf-8") as f:
            for row in f:
                for item in row:
                    if item == "\n":
                        level.append(rows.copy())
                        rows.clear()
                    else:
                        rows.append(item)
        # So the layout is read from the bottom left corner.
        level.reverse()
        return level

    def create_batch_sprite_from_level(self):
        """ Match the layout with its proper tile sprites """
        x = None
        y = None
        for idy, row in enumerate(self.level):
            for idx, value in enumerate(row):
                if value != "0" and value != "\n":
                    if value == "1":
                        x = 5
                        y = 0
                    elif value == "2":
                        x = 5
                        y = 1
                    elif value == "3":
                        x = 5
                        y = 2
                    elif value == "4":
                        x = 4
                        y = 0
                    elif value == "5":
                        x = 4
                        y = 1
                    elif value == "6":
                        x = 4
                        y = 2
                    elif value == "7":
                        x = 3
                        y = 0
                    elif value == "8":
                        x = 3
                        y = 1
                    elif value == "9":
                        x = 3
                        y = 2
                    elif value == "a":
                        x = 3
                        y = 3
                    elif value == "b":
                        x = 3
                        y = 5

                    if value == "5":
                        self.undergrounds.append(
                            Ground(
                                WorldResource.grid_tileset[(x, y)],
                                idx * WorldResource.grid_tileset[(x, y)].width,
                                idy * WorldResource.grid_tileset[(x, y)].height,
                                self.ground_batch,
                            )
                        )
                    else:
                        self.grounds.append(
                            Ground(
                                WorldResource.grid_tileset[(x, y)],
                                idx * WorldResource.grid_tileset[(x, y)].width,
                                idy * WorldResource.grid_tileset[(x, y)].height,
                                self.ground_batch,
                            )
                        )

    def draw(self):
        WorldResource.background.blit(0, 0)
        self.ground_batch.draw()
        self.char.draw()
        self.enemy.draw()

    def update(self, dt):
        self.char.update(dt)

        if not self.collision_check() and not self.char.is_jumping:
            self.char.velocity = -15
            force = self.char.mass * self.char.velocity
            self.char.shape_collision.y += force * dt
            self.char.velocity -= 2
        # camera/scrolling effect
        if self.char.shape_collision.x > 140:
            for tile in self.grounds:
                tile.move_left(self.char.speed_right, dt)
            for tile in self.undergrounds:
                tile.move_left(self.char.speed_right, dt)
            self.char.shape_collision.x -= self.char.speed_right * dt
            self.enemy.sprite.x -= self.char.speed_right * dt

        elif self.char.shape_collision.x < 100:
            for tile in self.grounds:
                tile.move_right(self.char.speed_left, dt)
            for tile in self.undergrounds:
                tile.move_right(self.char.speed_left, dt)
            self.char.shape_collision.x += self.char.speed_left * dt
            self.enemy.sprite.x += self.char.speed_right * dt

    def collision_check(self):
        counter = 0
        for ground in self.grounds:
            # Not sure if that work but only do the collision detection if the
            # tile is close to the character (200x200)
            if (
                ground.sprite.x > self.char.shape_collision.x - 100
                and ground.sprite.x < self.char.shape_collision.x + 100
                and ground.sprite.y > self.char.shape_collision.y - 100
                and ground.sprite.y < self.char.shape_collision.y + 100
            ):
                if self.bottom_side_collide_with_object_top_side(ground):
                    counter += 1
                    self.char.is_jumping = False
                    self.char.velocity = 20
                    self.char.shape_collision.y = (
                        ground.sprite.y
                        + ground.sprite.height
                        + self.char.shape_collision.height // 2
                    )
                if self.right_side_collide_with_object_left_side(ground):
                    self.char.shape_collision.x = (
                        ground.get_left_side() - self.char.shape_collision.width // 2
                    )
                    self.char.speed_right = 0
                if self.left_side_collide_with_object_right_side(ground):
                    self.char.shape_collision.x = (
                        ground.sprite.x
                        + ground.sprite.width
                        + self.char.shape_collision.width // 2
                    )
                    self.char.speed_left = 0
                if self.top_side_collide_with_object_bottom_side(ground):
                    self.char.shape_collision.y = (
                        ground.get_bottom_side() - self.char.shape_collision.width // 2
                    )
                    # Knock back effect from hitting platform's bottom when jumping
                    self.char.velocity = -20
                    force = self.char.mass * self.char.velocity
                    self.char.shape_collision.y += force * 1.0 / 120.0
                    self.char.velocity -= 2

                self.char.speed_right = 60
                self.char.speed_left = 60
        if counter > 0:
            return True
        else:
            return False

    def bottom_side_collide_with_object_top_side(self, object):
        if (
            self.char.get_bottom_side() <= object.get_top_side()
            and self.char.get_bottom_side() > object.get_bottom_side()
            and self.char.shape_collision.x > object.get_left_side()
            and self.char.shape_collision.x < object.get_right_side()
        ):
            return True
        return False

    def right_side_collide_with_object_left_side(self, object):
        if (
            self.char.get_right_side() >= object.get_left_side()
            and self.char.get_right_side() < object.get_right_side()
            and self.char.shape_collision.y < object.get_top_side()
            and self.char.shape_collision.y > object.get_bottom_side()
        ):
            return True
        return False

    def left_side_collide_with_object_right_side(self, object):
        if (
            self.char.get_left_side() <= object.get_right_side()
            and self.char.get_left_side() > object.get_left_side()
            and self.char.shape_collision.y < object.get_top_side()
            and self.char.shape_collision.y > object.get_bottom_side()
        ):
            return True
        return False

    def top_side_collide_with_object_bottom_side(self, object):
        if (
            self.char.get_top_side() >= object.get_bottom_side()
            and self.char.get_top_side() < object.get_top_side()
            and self.char.shape_collision.x > object.get_left_side()
            and self.char.shape_collision.x < object.get_right_side()
        ):
            return True
        return False
