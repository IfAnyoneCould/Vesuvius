import core.entity as Entity
from core.container import HandlerContainer


def new_unit(kind, handlers: HandlerContainer):
    id = Entity.get_id()
    stats = getattr(handlers.config.unit, kind)
    handlers.gold_handler.add(id, "unit")
    handlers.damage_handler.add(id, "unit", stats.base_damage)
    handlers.healh_handler.add(id, "unit", stats.base_health)
    return id
