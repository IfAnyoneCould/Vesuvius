from engine.core.handler import HandlerTemplate
from engine.core.config import Config


class RFIDHandler(HandlerTemplate):
    def __init__(
        self, config: Config
    ) -> None:  # ik config isn't used and i kind of override everything from HandlerTemplate, but it's the principle that matters
        super().__init__(
            config
        )  # i want to keep the system consistent even if it isn't the most efficient
        self.handlers = {"piece": PieceRFIDHandler()}
        self._rfid_to_piece = {}

    def add(self, id, kind="piece", rfid=None):
        if rfid is None:
            raise ValueError("RFIDHandler.add() requires an rfid")
        handler = self.handlers[kind]
        handler.add(id, rfid)
        self._rfid_to_piece[rfid] = id
        self.ids[id] = handler

    def remove(self, id):
        rfid = self.get(id)
        if rfid is not None:
            self._rfid_to_piece.pop(rfid)
        self.ids[id].remove(id)
        self.ids.pop(id, None)

    def get(self, id):
        return self.ids[id].get(id)

    def get_id_from_rfid(self, rfid):
        return self._rfid_to_piece.get(rfid)


class PieceRFIDHandler:
    def __init__(self) -> None:
        self._rfids = {}

    def add(self, id, rfid):
        self._rfids[id] = rfid

    def remove(self, id):
        self._rfids.pop(id, None)

    def get(self, id):
        return self._rfids.get(id)
