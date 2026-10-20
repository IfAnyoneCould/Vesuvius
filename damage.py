from config import Config
from handlertemplate import HandlerTemplate


class DamageHandler(HandlerTemplate):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.handlers = {"unit": UnitDamageHandler(self.config)}

    def add(self, id, kind, base=None):
        self.ids[id].add(id, kind, base)

    def get_damage(self, id):
        self.ids[id].get_damage(id)

    def set_damage(self, id, val):
        self.ids[id].set_damage(id, val)


class UnitDamageHandler:
    def __init__(self, config: Config) -> None:
        self._damage = {}
        self._base_damage = {}

    def add(self, id, kind, base):
        self._base_damage[id] = base
        self._damage[id] = base

    def remove(self, id):
        self._base_damage.pop(id, None)
        self._damage.pop(id, None)
