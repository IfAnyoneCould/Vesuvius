from game.context import GameContext
from graphics.animation import Animation
import time
import _thread as thread
import sys

from graphics.sprite import Sprite


class ThreadHelper:
    def __init__(self) -> None:
        self.running = True
        self.done = False
        self.lock = thread.allocate_lock()
        self.error: Exception | None = None

    def start(self, args):
        try:
            thread.start_new_thread(self.render, args)
        except OSError:
            time.sleep_ms(5)
            thread.start_new_thread(self.render, args)

    def stop(self):
        with self.lock:
            self.running = False

    def wait(self):
        try:
            while self.running:
                with self.lock:
                    if self.error is not None:
                        self.running = False
                        raise self.error
                time.sleep_ms(1)
        finally:
            self.running = False
            while not self.done:
                time.sleep_ms(1)

    def render(self, body, args, end, endargs):
        try:
            body(*args)
        except Exception as e:
            with self.lock:
                sys.print_exception(e)
                self.error = e
                self.running = False
        finally:
            try:
                end(*endargs)
            finally:
                with self.lock:
                    self.done = True


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

    def farm(self):
        region_id = self.ids["center"]
        region = self.ctx.handlers.region_handler.get_name(region_id)
        farm_animation = Animation(
            "farm_" + region,
            self.ctx.sd,
            self.ctx.graphics_config,
        )

        player_region_id = self.ctx.handlers.player_handler.get_region(self.player_id)
        region_position = self.ctx.handlers.region_handler.get_adjacency(
            player_region_id, region_id
        )

        units = [i for p, i in self.ids.items() if p != "center"]
        gold_amount = getattr(
            self.ctx.engine_config.game.farming_rewards, region_position
        )
        for unit in units:
            self.ctx.handlers.gold_handler.add_gold(unit, gold_amount)

        return farm_animation

    def run(self):
        anim = self.farm()
        self.thread.start(
            (
                self.render,
                (anim,),
                self.render_cleanup,
                (anim,),
            )
        )
        self.thread.wait()


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
