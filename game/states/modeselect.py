from game.context import GameContext
from game.threadhelper import ThreadHelper
from graphics.sprite import Sprite
import time


class ModeSelect:
    def __init__(self, ctx: GameContext) -> None:
        self.ctx = ctx
        self.thread = ThreadHelper()
        self.current = 0
        self.changed = True

    def render(
        self,
        bg: Sprite,
        box: Sprite,
        select_box: Sprite,
        options,
        y_offset,
        x_offset,
    ):
        bg.load()
        box.load()
        select_box.load()

        # TODO implement text, currently only draws generic boxes

        bg.draw(self.ctx.lcd)
        while self.thread.running:
            if self.changed:
                with self.thread.lock:
                    self.changed = False
                for i, o in enumerate(options):
                    if self.current == i:
                        select_box.set_position(x_offset, y_offset * i)
                        select_box.draw(self.ctx.lcd)
                    else:
                        box.set_position(x_offset, y_offset * i)
                        box.draw(self.ctx.lcd)
            else:
                time.sleep_ms(1)

    def render_cleanup(self, bg: Sprite, box: Sprite, select_box: Sprite):
        bg.unload()
        box.unload()
        select_box.unload()

    def run(self):
        # NOTE a current limitation of this system is that all sprites and such have to be placed
        # manually, even for menus. while i could make a template engine, that would be massively
        # overkill for this small of a game. if this was ported into a full video game, it would
        # make sense
        bg = Sprite("menu_background", self.ctx.sd, self.ctx.graphics_config)
        box = Sprite("menu_select_box", self.ctx.sd, self.ctx.graphics_config)
        select_box = Sprite(
            "menu_select_highlight", self.ctx.sd, self.ctx.graphics_config
        )
        options = self.ctx.engine_config.modes

        y_offset = box.get_height()
        x_offset = 0  # in case i want to move them later

        self.thread.start(
            (
                self.render,
                (
                    bg,
                    box,
                    select_box,
                    options,
                    y_offset,
                    x_offset,
                ),
                self.render_cleanup,
                (
                    bg,
                    box,
                    select_box,
                ),
            )
        )
        while self.thread.running:
            self.ctx.buttons.update(time.ticks_ms())
            if self.ctx.buttons.is_pressed("a"):
                with self.thread.lock:
                    if self.current + 1 == len(options):
                        self.current = 0
                    else:
                        self.current += 1
                    self.changed = True
            elif self.ctx.buttons.is_pressed("b"):
                self.thread.stop()
                self.changed = True  # uesless here, but maybe for the future
            else:
                time.sleep_ms(1)
        self.thread.wait()
        return self.current
