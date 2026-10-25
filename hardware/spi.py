from machine import Pin, SPI
from hardware.ioconfig import IoConfig


class SPIHandler:
    def __init__(self, config: IoConfig) -> None:
        self.spi_ids = {}
        self.spi_config = {}
        self.using = None
        self.current_baud = None
        for k, v in config.spi.items():
            k = int(k)
            spi = SPI(k, sck=Pin(v["sck"]), mosi=Pin(v["mosi"]), miso=Pin(v["miso"]))
            self.spi_ids[k] = spi
            self.spi_config[k] = v

    def get_spi(self, id):
        return self.spi_ids[id]

    def get_spi_config(self, id):
        return self.spi_config[id]

    def use(self, id, baud):
        if self.using != id or self.current_baud != baud:
            self.get_spi(id).init(baudrate=baud)
            self.using = id
            self.current_baud = baud
