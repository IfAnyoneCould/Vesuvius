from game.context import GameContext


class SelectorReturn:
    def __init__(self, type, ids, error=None) -> None:
        self.type = type
        self.ids = ids
        self.error = error


class StateSelector:
    def __init__(self, ctx: GameContext) -> None:
        self.ctx = ctx

    def non_center_by_player(self, no_c):
        s: dict[int | str, list] = {}
        for id in no_c:
            player_id = self.ctx.handlers.player_handler.get_player_from_id(id)["owner"]
            if player_id is not None:
                s.setdefault(player_id, [])
                s[player_id].append(id)

        return s

    def process_center(self, ids):
        center = ids.get("center")
        if center is None:
            return "empty", None, None
        player_info = self.ctx.handlers.player_handler.get_player_from_id(center)
        return center, player_info["type"], player_info["owner"]

    def check_types(self, no_c, *types):
        for u in no_c:
            kind = self.ctx.handlers.player_handler.get_player_from_id(u)["type"]
            if kind not in types:
                return False
        return True

    def select(self, player_id, ids):
        center, c_type, owner = self.process_center(ids)

        no_c = [id for p, id in ids.items() if p != "center"]
        no_c_by_p = self.non_center_by_player(no_c)

        if c_type == "region":
            if len(no_c_by_p) > 1:
                return SelectorReturn(
                    "farm", ids, "can only farm with one players units"
                )
            elif len(no_c_by_p) == 0:
                return SelectorReturn("farm", ids, "add units to farm")
            elif not self.check_types(no_c, "unit"):
                return SelectorReturn(
                    "farm", ids, "can only farm with unit type pieces"
                )
            elif no_c_by_p.get(player_id) is None:
                return SelectorReturn("farm", ids, "can only farm with own units")
            return SelectorReturn("farm", ids)
        elif c_type == "castle":
            # this is where depositing and raiding will be handled
            pass
        elif c_type == "unit":
            return SelectorReturn(None, ids, "remove unit from center")
        elif c_type == "empty":
            if len(no_c) != 2:
                return SelectorReturn("battle", ids, "can only battle with 2 units")
            elif len(no_c_by_p) != 2:
                return SelectorReturn("battle", ids, "can only battle with 2 players")
            elif not self.check_types(no_c, "unit"):
                return SelectorReturn(
                    "battle", ids, "can only battle with unit type pieces"
                )
            elif no_c_by_p.get(player_id) is None:
                return SelectorReturn("battle", ids, "active player must be in battle")
            return SelectorReturn("battle", ids)
        return SelectorReturn(None, None, "unrecognized center")
