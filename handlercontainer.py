from gold import GoldHandler
from health import HealthHandler
from config import Config


class HandlerContainer:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.gold_handler = GoldHandler(config)
        self.healh_handler = HealthHandler(config)
