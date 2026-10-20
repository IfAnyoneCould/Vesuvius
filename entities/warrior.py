from core.config import Config
from core.entity import Entity
from components.gold import GoldHandler
from components.health import HealthHandler


class warrior(Entity):
    def __init__(self, config: Config):
        super().__init__()
