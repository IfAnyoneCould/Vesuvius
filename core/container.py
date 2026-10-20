from components.gold import GoldHandler
from components.health import HealthHandler
from components.damage import DamageHandler
from core.config import Config


class HandlerContainer:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.gold_handler = GoldHandler(config)
        self.healh_handler = HealthHandler(config)
        self.damage_handler = DamageHandler(config)
