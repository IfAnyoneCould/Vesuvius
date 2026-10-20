from config import Config
from entity import Entity
from gold import GoldHandler
from health import HealthHandler


class warrior(Entity):
    def __init__(self, config: Config):
        super().__init__()
