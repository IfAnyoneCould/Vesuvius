from ioconfig import IoConfig
from machine import Pin, SPI
from drivers import st7789py as st7789


class Lcd:
    def __init__(self, config: IoConfig):
        self.config = config
        spi = SPI(
            1,
            baudrate=config.lcd.baud,
            sck=Pin(config.lcd.sck),
            mosi=Pin(config.lcd.mosi),
        )
        self.display = st7789.ST7789(
            spi,
            config.lcd.resx,
            config.lcd.resy,
            reset=Pin(config.lcd.rst, Pin.OUT),
            cs=Pin(config.lcd.cs, Pin.OUT),
            dc=Pin(config.lcd.dc, Pin.OUT),
            backlight=Pin(config.lcd.bl, Pin.OUT),
            rotation=0,
        )
