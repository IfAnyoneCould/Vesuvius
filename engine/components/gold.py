from engine.core.config import Config
from engine.core.handler import HandlerTemplate


class GoldHandler(HandlerTemplate):
    def __init__(self, config: Config):
        super().__init__(config)
        self.handlers = {
            "unit": UnitGoldHandler(config),
            "castle": CastleGoldHandler(config),
        }

    def set_gold(self, id, val):
        self.ids[id].set_gold(id, val)

    def get_gold(self, id):
        return self.ids[id].get_gold(id)

    def add_gold(self, id, val):
        self.ids[id].add_gold(id, val)

    def get_transported_gold(self, id):
        return (
            self.ids[id].get_transported_gold(id)
            if self.check_kind(id, "unit")
            else None
        )

    def add_transported_gold(self, id, val):
        if not self.check_kind(id, "unit"):
            return False
        self.ids[id].add_transported_gold(id, val)
        return True

    def deposit(self, unit_id, castle_id):
        if not (
            self.check_kind(unit_id, "unit") and self.check_kind(castle_id, "castle")
        ):
            return False
        gold = self.get_gold(unit_id)
        self.add_gold(castle_id, gold)
        self.add_transported_gold(
            unit_id, gold
        )  # not perfectly efficient, but this dosen't run every frame so its fine
        self.set_gold(unit_id, 0)
        return True


class UnitGoldHandler:
    def __init__(self, config: Config):
        self._gold = {}
        self._transported_gold = {}
        self.config = config

    def remove(self, id):
        self._gold.pop(id, None)
        self._transported_gold.pop(id, None)

    def add(self, id):
        self._gold[id] = self.config.unit.start_gold
        self._transported_gold[id] = 0

    def get_gold(self, id):
        return self._gold[id]

    def get_transported_gold(self, id):
        return self._transported_gold[id]

    def add_transported_gold(self, id, val):
        self._transported_gold[id] += val

    def set_gold(self, id, val):
        self._gold[id] = val

    def add_gold(self, id, val):
        self._gold[id] += val


class CastleGoldHandler:
    def __init__(self, config: Config):
        self._gold = {}
        self.config = config

    def remove(self, id):
        self._gold.pop(id, None)

    def add(self, id):
        self._gold[id] = self.config.player.start_gold

    def get_gold(self, id):
        return self._gold[id]

    def set_gold(self, id, val):
        self._gold[id] = val

    def add_gold(self, id, val):
        self._gold[id] += val
