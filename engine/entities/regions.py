from engine.core.container import HandlerContainer
import engine.core.entity as Entity


def new_region(handlers: HandlerContainer):
    id = Entity.get_id()
    handlers.region_handler.add(id)
    return id


def remove_region(id, handlers: HandlerContainer):
    handlers.region_handler.remove(id)
