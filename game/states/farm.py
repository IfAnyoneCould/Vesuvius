from game.context import GameContext
from game.threadhelper import ThreadHelper
from graphics.animation import Animation
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
