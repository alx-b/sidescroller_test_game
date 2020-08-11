import pyglet

from scene import Scene


class MainWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__()
        self.width = 240
        self.height = 160

        self.scene = Scene(self.width, self.height)
        self.push_handlers(self.scene.char.key_handler)

    def on_key_press(self, symbol, modifiers):
        self.scene.char.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.scene.char.on_key_release(symbol, modifiers)

    def update(self, dt):
        self.scene.update(dt)

    def on_draw(self):
        self.clear()
        self.scene.draw()


if __name__ == "__main__":
    window = MainWindow()
    pyglet.clock.schedule_interval(window.update, 1 / 120.0)
    pyglet.app.run()
