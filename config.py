import json


class Player:
    def __init__(self, data) -> None:
        self.count: int = data["count"]
        self.untis: int = data["units"]
        self.start_gold: int = data["start_gold"]


class Warrior:
    def __init__(self, data) -> None:
        self.base_health = data["base_health"]


class Unit:
    def __init__(self, data) -> None:
        self.start_gold: int = data["start_gold"]
        self.warrior = Warrior(data["warrior"])


class Game:
    def __init__(self, data) -> None:
        self.max_rounds: int = data["max_rounds"]
        self.winning_gold: int = data["winning_gold"]


class Config:
    def __init__(self, data):
        self.player = Player(data["player"])
        self.unit = Unit(data["unit"])
        self.game = Game(data["game"])


def deep_merge(base, override):
    for k, v in override.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            deep_merge(base[k], v)
        else:
            base[k] = v
    return base


def load_config(path):
    with open("configs/default.json") as f:
        data = json.load(f)
    with open("configs/" + path + ".json") as f:
        deep_merge(data, json.load(f))
    return Config(data)
