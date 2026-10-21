from engine.core.config import Config
from engine.core.handler import HandlerTemplate


class HealthHandler(HandlerTemplate):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.handlers = {"unit": UnitHealthHandler(config)}

    def add(self, id, kind, base=None):
        if base == None:
            raise ValueError("HealthHandler.add() requires a base")
        handler = self.handlers[kind]
        self.ids[id] = handler
        handler.add(id, base)

    def get_health(self, id):
        return self.ids[id].get_health(id)

    def get_max_health(self, id):
        return self.ids[id].get_max_health(id)

    def get_base_health(self, id):
        return self.ids[id].get_base_health(id)

    def is_alive(self, id):
        return self.ids[id].get_health(id) > 0

    def add_health(self, id, val):
        self.ids[id].add_health(id, val)

    def sub_health(self, id, val):
        self.ids[id].sub_health(id, val)

    def set_max_health(self, id, val):
        self.ids[id].set_max_health(id, val)


class UnitHealthHandler:
    def __init__(self, config: Config) -> None:
        self._base_health = {}
        self._health = {}
        self._max_health = {}
        self.config = config

    def add(self, id, base):
        self._base_health[id] = base
        self._max_health[id] = base
        self._health[id] = base

    def remove(self, id):
        self._health.pop(id, None)
        self._base_health.pop(id, None)
        self._max_health.pop(id, None)

    def get_health(self, id):
        return self._health[id]

    def get_max_health(self, id):
        return self._max_health[id]

    def get_base_health(self, id):
        return self._base_health[id]

    def add_health(self, id, val):
        self._health[id] = min(self.get_max_health(id), self.get_health(id) + val)

    def sub_health(self, id, val):
        self._health[id] = max(0, self.get_health(id) - val)

    def set_max_health(self, id, val):
        self._max_health[id] = val
