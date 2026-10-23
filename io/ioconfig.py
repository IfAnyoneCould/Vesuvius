import json


class SharedPins:
    def __init__(self, data) -> None:
        self.sck = data["sck"]
        self.mosi = data["mosi"]
        self.miso = data["miso"]
        self.rst = data["rst"]


class Scanners:
    def __init__(self, data) -> None:
        self.count = data["count"]
        self.positions = data[
            "positions"
        ]  # kept as a dict because it's easier to work with
        self.shared_pins = SharedPins(data["shared_pins"])
        self.cs = data["cs"]


class Sd:
    def __init__(self, data) -> None:
        self.baud = data["baud"]
        self.sck = data["sck"]
        self.mosi = data["mosi"]
        self.miso = data["miso"]
        self.cs = data["cs"]
        self.mount_point = data["mount_point"]


class Lcd:
    def __init__(self, data) -> None:
        self.baud = data["baud"]
        self.resx = data["resx"]
        self.resy = data["resy"]
        self.sck = data["sck"]
        self.mosi = data["mosi"]
        self.cs = data["cs"]
        self.dc = data["dc"]
        self.rst = data["rst"]
        self.bl = data["bl"]


class IoConfig:
    def __init__(self, data) -> None:
        self.sd = Sd(data["sd"])
        self.lcd = Lcd(data["lcd"])
        self.scanners = Scanners(data["scanners"])


def load_config():
    with open("io/configs/default.json") as f:
        data = json.load(f)
    return IoConfig(data)
