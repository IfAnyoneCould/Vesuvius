from game.threadhelper import ThreadHelper
from game.context import GameContext
from graphics.animation import Animation
import time


class StartMenu:
    def __init__(self, ctx: GameContext) -> None:
        self.ctx = ctx
        self.thread = ThreadHelper()

    def render(self, anim: Animation):
        anim.gen_buffer()
        while self.thread.running:
            time_ms = time.ticks_ms()
            anim.play(time_ms)
            anim.draw(self.ctx.lcd)

    def render_cleanup(self, anim: Animation):
        anim.unload()

    def run(self):
        anim = Animation("start_menu", self.ctx.sd, self.ctx.graphics_config)
        self.thread.start(
            (
                self.render,
                (anim,),
                self.render_cleanup,
                (anim,),
            )
        )
        while not self.ctx.buttons.is_pressed("a") and self.thread.running:
            self.ctx.buttons.update(time.ticks_ms())
            time.sleep_ms(1)
        self.thread.stop()
        self.thread.wait()
        # there currently isn't a transition or anything, it just cuts but thats a later thing of polish that i would add to the lcd driver
