from core.container import HandlerContainer
from core.entity import Entity


class Ranger(Entity):
    def __init__(self, handlers: HandlerContainer) -> None:
        super().__init__()
        handlers.gold_handler.add(self.id, "unit")
        handlers.damage_handler.add(
            self.id, "unit", handlers.config.unit.ranger.base_damage
        )
        handlers.healh_handler.add(
            self.id, "unit", handlers.config.unit.ranger.base_health
        )
