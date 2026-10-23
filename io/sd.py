from ioconfig import IoConfig
import os
from drivers import sdcard
from machine import SPI, Pin


def mount_sd(config: IoConfig):
    try:
        Pin(config.lcd.cs, Pin.OUT, value=1)  # deselect display during init
        spi = SPI(
            1,
            sck=Pin(config.sd.sck),
            mosi=Pin(config.sd.mosi),
            miso=Pin(config.sd.miso),
        )
        sd = sdcard.SDCard(spi, Pin(config.sd.cs, Pin.OUT), baudrate=config.sd.baud)
        os.mount(sd, config.sd.mount_point)
        return None
    except OSError as e:
        return e
