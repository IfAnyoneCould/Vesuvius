import json


class Shared:
    def __init__(self, data) -> None:
        self.spi_id = data["spi_id"]
        self.rst = data["rst"]


class MemoryBlock:
    def __init__(self, data) -> None:
        self.start = data["start"]
        self.end = data["end"]
        self.page_size = data["page_size"]
        self.pages_per_read = data["pages_per_read"]


class Scanners:
    def __init__(self, data) -> None:
        self.memory_block = MemoryBlock(data["memory_block"])
        self.count = data["count"]
        self.positions = data[
            "positions"
        ]  # kept as a dict because it's easier to work with
        self.shared = Shared(data["shared"])
        self.cs = data["cs"]


class Sd:
    def __init__(self, data) -> None:
        self.baud = data["baud"]
        self.spi_id = data["spi_id"]
        self.cs = data["cs"]
        self.mount_point = data["mount_point"]


class Lcd:
    def __init__(self, data) -> None:
        self.baud = data["baud"]
        self.resx = data["resx"]
        self.resy = data["resy"]
        self.spi_id = data["spi_id"]
        self.cs = data["cs"]
        self.dc = data["dc"]
        self.rst = data["rst"]
        self.bl = data["bl"]


class IoConfig:
    def __init__(self, data) -> None:
        self.spi = data["spi"]
        self.sd = Sd(data["sd"])
        self.lcd = Lcd(data["lcd"])
        self.scanners = Scanners(data["scanners"])


def load_config():
    with open("configs/hardware.json") as f:
        data = json.load(f)
    return IoConfig(data)
