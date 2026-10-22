from engine.components.gold import GoldHandler
from engine.components.health import HealthHandler
from engine.components.player import PlayerHandler
from engine.components.damage import DamageHandler
from engine.components.region import RegionHandler
from engine.core.config import Config


class HandlerContainer:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.gold_handler = GoldHandler(config)
        self.healh_handler = HealthHandler(config)
        self.damage_handler = DamageHandler(config)
        self.player_handler = PlayerHandler(config)
        self.region_handler = RegionHandler(config)
