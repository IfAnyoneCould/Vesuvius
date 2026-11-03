from game.context import GameContext
from graphics.animation import Animation
import time
import _thread as thread
import sys


class Farm:
    def __init__(self, player_id, ids, ctx: GameContext):
        self.ctx = ctx
        self.player_id = player_id
        self.ids = ids
        self.lock = thread.allocate_lock()
        self.running = True
        self.done = False
        self.error = None

    def farm_render(self, anim: Animation):
        try:
            anim.gen_buffer()
            while self.running:
                time_ms = time.ticks_ms()
                anim.play(time_ms)
                if anim.is_finished():
                    with self.lock:
                        self.running = False
                    break
                anim.draw(self.ctx.lcd)
        except Exception as e:
            with self.lock:
                sys.print_exception(e)
                self.error = e
        finally:
            anim.unload()
            with self.lock:
                self.done = True

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
        try:
            thread.start_new_thread(self.farm_render, (anim,))
        except OSError:
            time.sleep_ms(5)
            thread.start_new_thread(self.farm_render, (anim,))
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


def start_menu(ctx: GameContext):
    pass
