import engine.core.entity as Entity
import engine.entities.castle as Castle
import engine.entities.regions as Regions
import engine.entities.unit as Unit
from engine.core.container import HandlerContainer


def new_player(handlers: HandlerContainer):
    id = Entity.get_id()
    handlers.player_handler.add(id)
    castle_id = Castle.new_castle(handlers)
    handlers.player_handler.add_castle(id, castle_id)
    region_id = Regions.new_region(handlers)
    handlers.player_handler.add_region(id, region_id)
    return id


def remove_player(id, handlers: HandlerContainer):
    castle = handlers.player_handler.get_castle(id)
    if castle is not None:
        Castle.remove_castle(castle, handlers)
    region = handlers.player_handler.get_region(id)
    if region is not None:
        Regions.remove_region(region, handlers)
    units = handlers.player_handler.get_units(id).copy()
    for unit in units:
        Unit.remove_unit(unit, handlers)
    handlers.player_handler.remove(id)
