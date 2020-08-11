import pyglet

from player import Player
from ground import Ground
from resource import WorldResource
from enemy import Enemy


class Scene:
    def __init__(self, width, height):
        self.win_width = width
        self.win_height = height

        self.batch = pyglet.graphics.Batch()
        self.bg = pyglet.graphics.OrderedGroup(0)
        self.mid = pyglet.graphics.OrderedGroup(1)
        self.fg = pyglet.graphics.OrderedGroup(2)

        self.char = Player(112, 80, batch=self.batch, group=self.mid)
        self.colliders = []
        self.non_colliders = []
        self.level = self.get_level_layout()
        self.create_batch_sprite_from_level()
        self.enemies = []
        self.enemies.append(Enemy(160, 68, batch=self.batch, group=self.mid))
        self.enemies.append(Enemy(195, 36, batch=self.batch, group=self.mid))

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
        """ Match the layout with its proper tile sprite. """
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
                        self.non_colliders.append(
                            Ground(
                                WorldResource.grid_tileset[(x, y)],
                                idx * WorldResource.grid_tileset[(x, y)].width,
                                idy * WorldResource.grid_tileset[(x, y)].height,
                                self.batch,
                                self.bg,
                            )
                        )
                    else:
                        self.colliders.append(
                            Ground(
                                WorldResource.grid_tileset[(x, y)],
                                idx * WorldResource.grid_tileset[(x, y)].width,
                                idy * WorldResource.grid_tileset[(x, y)].height,
                                self.batch,
                                self.bg,
                            )
                        )

    def draw(self):
        WorldResource.background.blit(0, 0)
        self.batch.draw()

    def update(self, dt):
        self.char.update(dt)

        if not self.char.collision_check(self.colliders) and not self.char.is_jumping:
            self.char.velocity = -15
            force = self.char.mass * self.char.velocity
            self.char.collision_shape.shape.y += force * dt
            self.char.velocity -= 2
        if self.char.is_attacking:
            self.enemies = self.char.attack(self.enemies)
        # camera/scrolling effect
        if self.char.collision_shape.shape.x > (0.5 * self.win_width):
            for tile in self.colliders:
                tile.move_left(self.char.speed_right, dt)
            for tile in self.non_colliders:
                tile.move_left(self.char.speed_right, dt)
            self.char.collision_shape.shape.x -= self.char.speed_right * dt
            for tile in self.enemies:
                tile.move_left(self.char.speed_right, dt)

        elif self.char.collision_shape.shape.x < (self.win_width / 3):
            for tile in self.colliders:
                tile.move_right(self.char.speed_left, dt)
            for tile in self.non_colliders:
                tile.move_right(self.char.speed_left, dt)
            self.char.collision_shape.shape.x += self.char.speed_left * dt
            for tile in self.enemies:
                tile.move_right(self.char.speed_left, dt)
