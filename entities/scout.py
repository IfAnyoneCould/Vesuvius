from core.entity import Entity
from core.container import HandlerContainer


class Scout(Entity):
    def __init(self, handlers: HandlerContainer):
        super().__init()
        handlers.damage_handler.add(
            self.id, "unit", handlers.config.unit.scout.base_damage
        )
        handlers.healh_handler.add(
            self.id, "unit", handlers.config.unit.scout.base_health
        )
        handlers.gold_handler.add(self.id, "unit")
