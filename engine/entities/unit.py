import engine.core.entity as Entity
from engine.core.container import HandlerContainer


def new_unit(kind, handlers: HandlerContainer):
    id = Entity.get_id()
    stats = getattr(handlers.config.unit, kind)
    handlers.gold_handler.add(id, "unit")
    handlers.damage_handler.add(id, "unit", stats.base_damage)
    handlers.healh_handler.add(id, "unit", stats.base_health)
    return id


def remove_unit(id, handlers: HandlerContainer):
    player = handlers.player_handler.get_player_from_unit(id)
    if player is not None:
        handlers.player_handler.remove_unit(player, id)
    handlers.gold_handler.remove(id)
    handlers.damage_handler.remove(id)
    handlers.healh_handler.remove(id)
