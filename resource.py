import pyglet


# class TileSheet:
#    def __init__(self, tilesheet, tile_width, tile_height):
#        self.width = tilesheet.width
#        self.height = tilesheet.height
#        self.tile_width = tile_width
#        self.tile_height = tile_height
#        self.total_cols = self.width // self.tile_width
#        self.total_rows = self.height // self.tile_height
#        self.tiles = self.tilesheet_into_list(tilesheet, tile_width, tile_height)
#
#    def tilesheet_into_list(self, tilesheet, tile_width, tile_height):
#        tiles = []
#        for row in range(0, tilesheet.width, tile_width):
#            rows = []
#            for tile in range(0, tilesheet.height, tile_height):
#                rows.append(
#                    tilesheet.get_region(
#                        x=row, y=tile, width=tile_width, height=tile_height
#                    )
#                )
#            tiles.append(rows)
#
#        return tiles
#
#    def print_info(self):
#        print(
#            f"tilesheet height: {self.height}\n"
#            f"tilesheet width: {self.width}\n"
#            f"tile width: {self.tile_width}\n"
#            f"tile height: {self.tile_height}\n"
#            f"total rows: {self.total_rows}\n"
#            f"total cols: {self.total_cols}\n"
#        )


class PlayerResource:
    def idle_animation(the_grid):
        frames = []
        for i in range(4):
            frames.append(the_grid[(8, i)])
        return pyglet.image.Animation.from_image_sequence(frames, duration=0.17)

    def run_animation(the_grid):
        frames = []
        for i in range(6):
            frames.append(the_grid[(11, i)])
        return pyglet.image.Animation.from_image_sequence(frames, duration=0.08)

    def jump_animation(the_grid):
        frames = []
        for i in range(3):
            frames.append(the_grid[(6, i)])
        return pyglet.image.Animation.from_image_sequence(frames, duration=0.5)

    def jump_fall_animation(the_grid):
        frames = []
        for i in range(3):
            frames.append(the_grid[(7, i)])
        return pyglet.image.Animation.from_image_sequence(frames, duration=0.5)

    def attack_animation(the_grid):
        frames = []
        for i in range(3):
            frames.append(the_grid[(9, i * 2)])
        return pyglet.image.Animation.from_image_sequence(
            frames, duration=0.1, loop=False
        )

    def attack_slash_animation(the_grid):
        frames = []
        for i in range(1, 8, 2):
            frames.append(the_grid[(9, i)])
        return pyglet.image.Animation.from_image_sequence(
            frames, duration=0.1, loop=False
        )

    pyglet.resource.path = ["images/herochar_sprites/"]
    pyglet.resource.reindex()

    player = pyglet.resource.image("herochar_spritesheet.png")
    the_grid = pyglet.image.ImageGrid(player, 13, 8)

    for img in the_grid:
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2

    run_anim = run_animation(the_grid)
    idle_anim = idle_animation(the_grid)
    jump_anim = jump_animation(the_grid)
    jump_fall_anim = jump_fall_animation(the_grid)
    attack_anim = attack_animation(the_grid)
    attack_slash_anim = attack_slash_animation(the_grid)


class WorldResource:
    pyglet.resource.path = ["images/tiles_and_background_foreground/"]
    pyglet.resource.reindex()

    background = pyglet.resource.image("background.png")

    tileset = pyglet.resource.image("tileset.png")
    grid_tileset = pyglet.image.ImageGrid(tileset, 6, 12)


class EnemyResource:
    def idle_animation(grid):
        frames = []
        for i in range(5):
            frames.append(grid[(0, i)])
        return pyglet.image.Animation.from_image_sequence(frames, duration=0.17)

    pyglet.resource.path = ["images/enemies_sprites/slime/"]
    pyglet.resource.reindex()

    tileset = pyglet.resource.image("slime_idle_anim_strip_5.png")
    grid_tileset = pyglet.image.ImageGrid(tileset, 1, 5)

    for img in grid_tileset:
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2

    idle_anim = idle_animation(grid_tileset)
