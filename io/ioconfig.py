import json


class Lcd:
    def __init__(self, data) -> None:
        self.sck = data["sck"]
        self.mosi = data["mosi"]
        self.res = data["res"]
        self.dc = data["dc"]
        self.bl = data["bl"]


class IoConfig:
    def __init__(self, data) -> None:
        self.lcd = data["lcd"]


def load_config():
    with open("io/configs/default.json") as f:
        data = json.load(f)
    return IoConfig(data)
