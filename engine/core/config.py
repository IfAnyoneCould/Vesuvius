import json


class Player:
    def __init__(self, data) -> None:
        self.count: int = data["count"]
        self.units: int = data["units"]
        self.start_gold: int = data["start_gold"]


class _Dev_Unit_:
    def __init__(self, data) -> None:
        self.base_health = data["base_health"]
        self.base_damage = data["base_damage"]


class Warrior:
    def __init__(self, data) -> None:
        self.base_health = data["base_health"]
        self.base_damage = data["base_damage"]


class Ranger:
    def __init__(self, data) -> None:
        self.base_health = data["base_health"]
        self.base_damage = data["base_damage"]


class Scout:
    def __init__(self, data) -> None:
        self.base_health = data["base_health"]
        self.base_damage = data["base_damage"]


class Unit:
    def __init__(self, data) -> None:
        self.start_gold: int = data["start_gold"]
        self._dev_unit_ = _Dev_Unit_(data["_dev_unit_"])
        self.warrior = Warrior(data["warrior"])
        self.ranger = Ranger(data["ranger"])
        self.scout = Scout(data["scout"])


class FarmingRewards:
    def __init__(self, data) -> None:
        self.own = data["own"]
        self.adjacent = data["adjacent"]
        self.diagonal = data["diagonal"]


class Game:
    def __init__(self, data) -> None:
        self.max_rounds: int = data["max_rounds"]
        self.winning_gold: int = data["winning_gold"]
        self.farming_rewards = FarmingRewards(data["farming_rewards"])


class Regions:
    def __init__(self, data) -> None:
        self.count = data["count"]
        self.names = data["names"]


class Rfid:
    def __init__(self, data) -> None:
        self.id_bytes = data["id_bytes"]
        self.id_encoding = data["id_encoding"]
        self.piece_bytes = data["piece_bytes"]
        self.region_bytes = data["region_bytes"]


class Config:
    def __init__(self, data):
        self.player = Player(data["player"])
        self.unit = Unit(data["unit"])
        self.game = Game(data["game"])
        self.regions = Regions(data["regions"])
        self.rfid = Rfid(data["rfid"])


def deep_merge(base, override):
    for k, v in override.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            deep_merge(base[k], v)
        else:
            base[k] = v
    return base


def load_config(path=None):
    with open("configs/engine_default.json") as f:
        data = json.load(f)
    if path is not None:
        with open("configs/" + path + ".json") as f:
            deep_merge(data, json.load(f))
    return Config(data)
