from game.context import GameContext
from graphics.animation import Animation
import time

"""
how game states are going to work
the gamestate class controls all of the different states the game is going to take
really, its just a wrapper for a bunch of related functions that share some varibales like context
while i was thinking of making each state seperately via composition because they all share
some systems like animations and stuff like that but it just felt too complicated
i think all of the objects relating to a state are going to be created from scratch every time
the state is switched to, but that might be more efficient? if thats wrong i can make the states
permanent, but this is an interesting architecture.

the game loop controls switching between states for better organization
this also means gameloop decides what state needs to run,
meaning that gamestate functions assume that the correct conditions have been met, such as scanners
and other stuff etc


"""


def farm(player_id, ids, ctx: GameContext):
    region_id = ids["center"]
    region = ctx.handlers.region_handler.get_name(region_id)
    farm_animation = Animation(
        "farm_" + region,
        ctx.sd,
        ctx.graphics_config,
    )

    player_region_id = ctx.handlers.player_handler.get_region(player_id)
    region_position = ctx.handlers.region_handler.get_adjacency(
        player_region_id, region_id
    )

    units = [i for p, i in ids.items() if p != "center"]
    gold_amount = getattr(ctx.engine_config.game.farming_rewards, region_position)
    for unit in units:
        ctx.handlers.gold_handler.add_gold(unit, gold_amount)

    # farming animation is simple because only the animation plays and nothing else
    farm_animation.gen_buffer()
    while True:
        time_ms = time.ticks_ms()
        farm_animation.play(time_ms)
        if farm_animation.is_finished():
            break
        farm_animation.draw(ctx.lcd)
    farm_animation.unload()
