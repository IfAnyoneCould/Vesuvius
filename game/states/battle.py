from game.threadhelper import ThreadHelper
from game.context import GameContext
from graphics.animation import Animation
from graphics.sprite import Sprite
from engine.systems.battle import battle
import time

# NOTE this is kinda weird because one state sort of contains two.
# while i could split it into two, its smaller this way
# not the best practice and it makes me feel a bit iffy, but it works for now at least


class Battle:
    def __init__(self, ids, ctx: GameContext) -> None:
        self.ctx = ctx
        self.ids = [id for k, id in ids.items() if k != "center"]
        self.thread = ThreadHelper()

    def render(self, anim: Animation):
        anim.gen_buffer()
        while self.thread.running:
            t = time.ticks_ms()
            anim.play(t)
            if anim.is_finished():
                self.thread.stop()
            else:
                anim.draw(self.ctx.lcd)

    def render_cleanup(self, anim: Animation):
        anim.unload()

    def run(self):
        battle(self.ids[0], self.ids[1], self.ctx.handlers)
        anim = Animation("battle", self.ctx.sd, self.ctx.graphics_config)
        self.thread.start((self.render, (anim,), self.render_cleanup, (anim,)))
        while self.thread.running:
            self.ctx.buttons.update(time.ticks_ms())
            if self.ctx.buttons.is_pressed("a"):
                self.thread.stop()
            time.sleep_ms(1)
        self.thread.wait()

        bg = Sprite("some background", self.ctx.sd, self.ctx.graphics_config)
        bg.load()
        bg.draw(self.ctx.lcd)

        try:
            # draw all of the information from the battle here

            self.ctx.buttons.update(time.ticks_ms())
            while not self.ctx.buttons.is_pressed("a"):
                self.ctx.buttons.update(time.ticks_ms())
                time.sleep_ms(1)

        finally:
            bg.unload()
