from game.context import GameContext
from game.threadhelper import ThreadHelper
from graphics.animation import Animation
import time


class Testing:
    def __init__(self, ctx: GameContext) -> None:
        self.ctx = ctx
        self.thread = ThreadHelper()

    def render(self, anim: Animation):
        anim.gen_buffer()
        while self.thread.running:
            anim.play(time.ticks_ms())
            anim.draw(self.ctx.lcd)

    def render_cleanup(self, anim: Animation):
        anim.unload()

    def run(self):
        anim = Animation("animation example", self.ctx.sd, self.ctx.graphics_config)
        self.thread.start((self.render, (anim,), self.render_cleanup, (anim,)))
        while self.thread.running:
            self.ctx.buttons.update(time.ticks_ms())
            if self.ctx.buttons.is_pressed("b"):
                self.thread.stop()
            time.sleep_ms(1)
        self.thread.wait()
