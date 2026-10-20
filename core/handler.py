from core.config import Config


class HandlerTemplate:
    def __init__(self, config: Config) -> None:
        self.ids = {}
        self.handlers = {}
        self.config = config

    def add(self, id, kind):
        handler = self.handlers[kind]
        handler.add(id)
        self.ids[id] = handler

    def get_handler(self, id):
        return self.ids[id]

    def check_kind(self, id, *kinds) -> bool:
        handlers = []
        for kind in kinds:
            handlers.append(self.handlers[kind])

        return self.ids.get(id) in handlers

    def remove(self, id):
        self.ids[id].remove(id)
        self.ids.pop(id, None)
