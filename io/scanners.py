from io.ioconfig import IoConfig
from drivers.mfrc522 import MFRC522


class Scanners:
    def __init__(self, config: IoConfig) -> None:
        self.config = config
        sck = config.scanners.shared_pins.sck
        miso = config.scanners.shared_pins.miso
        mosi = config.scanners.shared_pins.mosi
        rst = config.scanners.shared_pins.rst
        self.scanners = [
            MFRC522(spi_id=0, sck=sck, miso=miso, mosi=mosi, cs=c, rst=rst)
            for c in config.scanners.cs
        ]
        for scanner in self.scanners:
            scanner.init()

    def get_position_from_index(self, index):
        return next(
            (k for k, v in self.config.scanners.positions.items() if v == index), None
        )

    def get_index_from_position(self, position):
        return self.config.scanners.positions.get(position)

    def poll_all(self):
        results = []
        for s in self.scanners:
            stat, _ = s.request(s.REQIDL)
            if stat == s.OK:
                stat, uid = s.SelectTagSN()
                if stat == s.OK:
                    results.append(s.tohexstring(uid))
        return results

    def poll_position(self, position):
        index = self.config.scanners.positions.get(position)
        if index is None:
            raise ValueError(
                f"scanner position: {position} does not exist, check ioconfig"
            )
        s = self.scanners[index]
        stat, _ = s.request(s.REQIDL)
        if stat == s.OK:
            stat, uid = s.SelectTagSN()
            if stat == s.OK:
                return s.tohexstring(uid)

    def poll_index(self, index):
        pos = self.get_position_from_index(index)
        if pos is None:
            raise IndexError(f"index {index} out of bounds")
        s = self.scanners[index]
        stat, _ = s.request(s.REQIDL)
        if stat == s.OK:
            stat, uid = s.SelectTagSN()
            if stat == s.OK:
                return s.tohexstring(uid)
