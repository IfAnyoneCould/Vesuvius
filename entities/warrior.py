from core.entity import Entity
from core.container import HandlerContainer


class warrior(Entity):
    def __init__(self, handlers: HandlerContainer):
        super().__init__()
        handlers.gold_handler.add(self.id, "unit")
        handlers.healh_handler.add(
            self.id, "unit", handlers.config.unit.warrior.base_health
        )
        handlers.damage_handler.add(
            self.id, "unit", handlers.config.unit.warrior.base_damage
        )
