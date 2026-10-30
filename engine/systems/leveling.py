from engine.core.container import HandlerContainer
import math


def calc_stats(unit_id, handlers: HandlerContainer):
    gold = handlers.gold_handler.get_transported_gold(unit_id)
    if gold is None:
        raise ValueError(
            f"cannot calculate stats, {unit_id} does not exist in gold_handler"
        )
    # TODO actually work on these equations, temporary for now
    health_mod = int(10 * math.log(gold + 1))
    damage_mod = int(10 * math.log(gold + 1))

    handlers.healh_handler.set_health_mod(unit_id, health_mod)
    handlers.damage_handler.set_damage_mod(unit_id, damage_mod)


# unit_id and castle_id assumed to belong to same player, gameloop handles that
def deposit_gold(unit_id, castle_id, handlers: HandlerContainer):
    if not handlers.gold_handler.deposit(unit_id, castle_id):
        raise ValueError(f"failed deposit between {unit_id} and {castle_id}")
    calc_stats(unit_id, handlers)
    handlers.healh_handler.full_heal(unit_id)
