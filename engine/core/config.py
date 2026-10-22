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


class Game:
    def __init__(self, data) -> None:
        self.max_rounds: int = data["max_rounds"]
        self.winning_gold: int = data["winning_gold"]


class Regions:
    def __init__(self, data) -> None:
        self.count = data["count"]
        self.names = data["names"]


class Config:
    def __init__(self, data):
        self.player = Player(data["player"])
        self.unit = Unit(data["unit"])
        self.game = Game(data["game"])
        self.regions = Regions(data["regions"])


def deep_merge(base, override):
    for k, v in override.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            deep_merge(base[k], v)
        else:
            base[k] = v
    return base


def load_config(path):
    with open("engine/configs/default.json") as f:
        data = json.load(f)
    with open("engine/configs/" + path + ".json") as f:
        deep_merge(data, json.load(f))
    return Config(data)
