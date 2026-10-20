from core.handler import HandlerTemplate
from core.config import Config


class PlayerHandler(HandlerTemplate):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.handlers = {"standard": StandardPlayerHandler(config)}
        self.unit_to_player = {}
        self.castle_to_player = {}

    def add(self, id, kind, units=None):
        handler = self.handlers[kind]
        self.ids[id] = handler
        handler.add(id)
        if units is not None:
            for unit in units:
                self.add_unit(id, unit)

    def add_unit(self, player_id, unit_id):
        self.ids[player_id].add_unit(player_id, unit_id)
        self.unit_to_player[unit_id] = player_id

    def remove_unit(self, player_id, unit_id):
        self.ids[player_id].remove_unit(player_id, unit_id)
        self.unit_to_player.pop(unit_id, None)

    def remove(self, id):
        if self.get_castle(id) is not None:
            self.castle_to_player.pop(self.get_castle(id), None)
        units = self.get_units(id).copy()
        for unit in units:
            self.remove_unit(id, unit)
        self.ids[id].remove(id)
        self.ids.pop(id, None)

    def get_player_from_unit(self, unit_id):
        return self.unit_to_player[unit_id]

    def get_player_from_castle(self, castle_id):
        return self.castle_to_player[castle_id]

    def add_castle(self, player_id, castle_id):
        self.ids[player_id].add_castle(player_id, castle_id)
        self.castle_to_player[castle_id] = player_id

    def get_castle(self, id):
        return self.ids[id].get_castle(id)

    def get_units(self, id):
        return self.ids[id].get_units(id)


class StandardPlayerHandler:
    def __init__(self, config: Config):
        self._units = {}
        self._castle = {}

    def add(self, id):
        self._units[id] = []

    def add_unit(self, player_id, unit_id):
        self._units[player_id].append(unit_id)

    def remove_unit(self, player_id, unit_id):
        if unit_id in self._units[player_id]:
            self._units[player_id].remove(unit_id)

    def remove(self, id):
        self._castle.pop(id, None)
        self._units.pop(id, None)

    def add_castle(self, player_id, castle_id):
        self._castle[player_id] = castle_id

    def get_castle(self, id):
        return self._castle.get(id, None)

    def get_units(self, id):
        return self._units[id]
