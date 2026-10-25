from hardware.ioconfig import IoConfig
from hardware.spi import SPIHandler
from machine import Pin
from drivers import st7789py as st7789


class LCD:
    def __init__(self, spi_handler: SPIHandler, config: IoConfig):
        self.config = config
        self.spi_handler = spi_handler
        spi = spi_handler.get_spi(config.lcd.spi_id)
        self.display = st7789.ST7789(
            spi,
            config.lcd.resy,
            config.lcd.resx,  # driver wants these flipped
            reset=Pin(config.lcd.rst, Pin.OUT),
            cs=Pin(config.lcd.cs, Pin.OUT),
            dc=Pin(config.lcd.dc, Pin.OUT),
            backlight=Pin(config.lcd.bl, Pin.OUT),
            rotation=1,  # rotate to landscape
        )
        self.resx = config.lcd.resx
        self.resy = config.lcd.resy

    def use_lcd(self):
        self.spi_handler.use(self.config.lcd.spi_id, self.config.lcd.baud)

    # TODO fix the clipping issues and handle all positioning cases
    # also, figure out how to handle transparent backgrounds
    def blit(self, buf, x, y, width, height):
        if x + width > self.resx:
            width = self.resx - x
        if y + height > self.resy:
            height = self.resy - y
        self.display.blit_buffer(
            buf[: width * height * self.config.lcd.bpp], x, y, width, height
        )
