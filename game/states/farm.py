from game.context import GameContext
from game.threadhelper import ThreadHelper
from graphics.animation import Animation
from engine.systems.farm import farm
import time


class Farm:
    def __init__(self, player_id, ids, ctx: GameContext):
        self.ctx = ctx
        self.player_id = player_id
        self.ids = ids
        self.thread = ThreadHelper()

    def render(self, anim: Animation):
        anim.gen_buffer()
        while self.thread.running:
            time_ms = time.ticks_ms()
            anim.play(time_ms)
            if anim.is_finished():
                self.thread.stop()
                break
            anim.draw(self.ctx.lcd)

    def render_cleanup(self, anim: Animation):
        anim.unload()

    def run(self):
        region = farm(self.player_id, self.ids, self.ctx.handlers)
        anim = Animation(
            "farm_" + region,
            self.ctx.sd,
            self.ctx.graphics_config,
        )
        self.thread.start(
            (
                self.render,
                (anim,),
                self.render_cleanup,
                (anim,),
            )
        )
        while self.thread.running:
            self.ctx.buttons.update(time.ticks_ms())
            if self.ctx.buttons.is_pressed("a"):
                self.thread.stop()
            time.sleep_ms(1)
        self.thread.wait()
