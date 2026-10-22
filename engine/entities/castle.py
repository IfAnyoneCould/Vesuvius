from engine.core.container import HandlerContainer
import engine.core.entity as Entity


def new_castle(handlers: HandlerContainer):
    id = Entity.get_id()
    handlers.gold_handler.add(id, "castle")
    return id


def remove_castle(id, handlers: HandlerContainer):
    handlers.gold_handler.remove(id)
