from game.context import GameContext
from graphics.animation import Animation
import time
import _thread as thread
import sys


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
        self.thread.wait()  # i could put this in start but keeping them serperate might be useful


class StartMenu:
    def __init__(self, ctx: GameContext) -> None:
        self.ctx = ctx
        self.thread = ThreadHelper()

    def render(self):
        pass

    def render_cleanup(self):
        pass

    def menu(self):
        pass

    def run(self):
        pass


class ModeSelect:
    def __init__(self, ctx: GameContext) -> None:
        self.ctx = ctx
        self.thread = ThreadHelper()

    def render(self):
        pass

    def render_cleanup(self):
        pass

    def menu(self):
        pass

    def run(self):
        pass
