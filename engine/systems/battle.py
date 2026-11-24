from engine.core.container import HandlerContainer
from engine.systems.battle import battle
import random as rand


def battle(unit1, unit2, handlers: HandlerContainer):
    units = [unit1, unit2]
    damage = [0, 0]
    health = [0, 0]

    for i in range(len(units)):
        damage[i] = handlers.damage_handler.get_damage(units[i])
        health[i] = handlers.health_handler.get_health(units[i])

    dealt = [0, 0]
    for i in range(len(dealt)):
        for r in range(handlers.config.battle.dice_rolls):
            dealt[i] += rand.randint(0, damage[i])
        dealt[i] /= max(damage[0], damage[1]) * handlers.config.battle.dice_rolls
        dealt[i] *= health[1 - i]  # scale damage from 0 to health

    if dealt[0] == dealt[1]:
        return battle(unit1, unit2, handlers)

    winner = 1 if dealt[1] > dealt[0] else 0
    loser = 1 - winner

    handlers.gold_handler.add_gold(
        units[winner], handlers.gold_handler.get_gold(units[loser])
    )
    handlers.gold_handler.set_gold(units[loser], 0)

    # too lazy to add the set_health method rn
    handlers.health_handler.add_health(units[loser], -health[loser])
    handlers.health_handler.add_health(units[winner], -dealt[loser])

    return winner, dealt, damage, health
