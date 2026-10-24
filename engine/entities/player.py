import engine.core.entity as Entity
import engine.entities.castle as Castle
import engine.entities.regions as Regions
import engine.entities.unit as Unit
from engine.core.container import HandlerContainer
from engine.core.rfid import RFIDProcessor


def new_player(handlers: HandlerContainer, rfid_processor: RFIDProcessor):
    id = Entity.get_id()
    handlers.player_handler.add(id)
    castle_id = Castle.new_castle(handlers)
    handlers.player_handler.add_castle(id, castle_id)
    region_id = Regions.new_region(handlers)
    handlers.player_handler.add_region(id, region_id)
    region = handlers.region_handler.get_name(region_id)
    castle_rfid = rfid_processor.encode_rfid(castle_id, "castle", region)
    region_rfid = rfid_processor.encode_rfid(region_id, "region", region)
    handlers.rfid_handler.add(region_id, rfid=region_rfid)
    handlers.rfid_handler.add(castle_id, rfid=castle_rfid)
    return id


def remove_player(id, handlers: HandlerContainer):
    castle = handlers.player_handler.get_castle(id)
    if castle is not None:
        Castle.remove_castle(castle, handlers)
        handlers.rfid_handler.remove(castle)
    region = handlers.player_handler.get_region(id)
    if region is not None:
        Regions.remove_region(region, handlers)
        handlers.rfid_handler.remove(region)
    units = handlers.player_handler.get_units(id).copy()
    for unit in units:
        remove_unit(unit, handlers)
    handlers.player_handler.remove(id)


def add_unit(
    player_id, kind, handlers: HandlerContainer, rfid_processor: RFIDProcessor
):
    unit_id = Unit.new_unit(kind, handlers)
    region = handlers.region_handler.get_name(
        handlers.player_handler.get_region(player_id)
    )
    unit_rfid = rfid_processor.encode_rfid(unit_id, kind, region)
    handlers.player_handler.add_unit(player_id, unit_id)
    handlers.rfid_handler.add(unit_id, rfid=unit_rfid)
    return unit_id


def remove_unit(unit_id, handlers: HandlerContainer):
    Unit.remove_unit(unit_id, handlers)
    handlers.rfid_handler.remove(unit_id)
