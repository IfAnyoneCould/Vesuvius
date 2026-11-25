from engine.core.container import HandlerContainer


def farm(player_id, ids, handlers: HandlerContainer):

    region_id = ids["center"]
    region = handlers.region_handler.get_name(region_id)

    player_region_id = handlers.player_handler.get_region(player_id)
    region_position = handlers.region_handler.get_adjacency(player_region_id, region_id)

    units = [i for p, i in ids.items() if p != "center"]
    gold_amount = getattr(handlers.config.game.farming_rewards, region_position)
    for unit in units:
        handlers.gold_handler.add_gold(unit, gold_amount)

    return region
