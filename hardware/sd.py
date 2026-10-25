from hardware.ioconfig import IoConfig
import os
from drivers import sdcard
from machine import Pin
from hardware.spi import SPIHandler


class SD:
    def __init__(self, spi_handler: SPIHandler, config: IoConfig):
        self.spi_handler = spi_handler
        self.config = config
        try:
            Pin(config.lcd.cs, Pin.OUT, value=1)  # deselect display during SD init
            spi = spi_handler.get_spi(config.sd.spi_id)
            sd = sdcard.SDCard(spi, Pin(config.sd.cs, Pin.OUT), baudrate=config.sd.baud)
            os.mount(sd, config.sd.mount_point)
            self.initialized = True
            return
        except OSError as e:
            self.initialized = False
            self.error = e

    def use_sd(self):
        if not self.initialized:
            raise ValueError("cannot use uninitialized sd")
        self.spi_handler.use(self.config.sd.spi_id, self.config.sd.baud)
