from core.container import HandlerContainer
import core.entity as Entity


def new_castle(handlers: HandlerContainer):
    id = Entity.get_id()
    handlers.gold_handler.add(id, "castle")
    return id
