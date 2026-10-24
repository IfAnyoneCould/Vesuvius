from hardware.ioconfig import IoConfig
from hardware.spi import SPIHandler
from drivers.mfrc522 import MFRC522


class Scanners:
    def __init__(self, spi_handler: SPIHandler, config: IoConfig) -> None:
        self.config = config
        rst = config.scanners.shared.rst
        spi_config = spi_handler.get_spi_config(config.scanners.shared.spi_id)
        self.scanners = [
            MFRC522(
                spi_id=config.scanners.shared.spi_id,
                sck=spi_config["sck"],
                miso=spi_config["miso"],
                mosi=spi_config["mosi"],
                cs=c,
                rst=rst,
            )
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
        results = {}
        for i, s in enumerate(self.scanners):
            result = self.poll_scanner(s)
            if result is not None:
                results[i] = result
        return results

    def poll_position(self, position):
        return self.poll_index(self.get_index_from_position(position))

    def poll_index(self, index):
        return self.poll_scanner(self.scanners[index])

    def poll_scanner(self, scanner: MFRC522):
        if not self.select_tag(scanner):
            return
        result = b""
        start = int(self.config.scanners.memory_block.start, 16)
        end = int(self.config.scanners.memory_block.end, 16)
        for addr in range(start, end, self.config.scanners.memory_block.pages_per_read):
            stat, data = scanner.read(addr)
            if stat == scanner.ERR:
                raise ValueError(
                    f"failed to read address {addr}"
                )  # ik its the wrong error type, idk what's the right one
            result += bytes(data)
        return result[: (end - start) * self.config.scanners.memory_block.page_size]

    def write_index(self, index, tag):
        scanner = self.scanners[index]
        if not self.select_tag(scanner):
            return False
        start = int(self.config.scanners.memory_block.start, 16)
        end = int(self.config.scanners.memory_block.end, 16)
        for addr in range(start, end):
            i = addr - start
            page_size = self.config.scanners.memory_block.page_size
            data = tag[i * page_size : (i + 1) * page_size]
            stat = scanner.writeNTAGPage(addr, list(data))
            if stat == scanner.ERR:
                raise ValueError(
                    f"writing data {data} to address {addr} on scanner {index} failed"
                )  # ik this is the wrong error type, but idk the correct one
        return True

    def write_position(self, position, tag):
        index = self.get_index_from_position(position)
        return self.write_index(index, tag)

    def select_tag(self, scanner: MFRC522, first=True):
        stat, _ = scanner.request(scanner.REQALL)
        if stat == scanner.OK:
            stat, _ = scanner.SelectTagSN()
            if stat == scanner.OK:
                return True
        if first:
            return self.select_tag(scanner, first=False)
        return False
