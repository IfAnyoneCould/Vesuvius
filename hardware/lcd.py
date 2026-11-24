from hardware.ioconfig import IoConfig
from hardware.spi import SPIHandler
from machine import Pin
from drivers import st7789py as st7789
from drivers.ezFBfont import ezFBfont
import framebuf
from fonts.spleen import (
    ezFBfont_spleen_6x12_ascii_12,
    ezFBfont_spleen_12x24_ascii_23,
    ezFBfont_spleen_16x32_ascii_30,
)


class LCD:
    def __init__(self, spi_handler: SPIHandler, config: IoConfig, mv: memoryview):
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
        self.mv = mv
        self.fonts = {
            "small": ezFBfont_spleen_6x12_ascii_12,
            "body": ezFBfont_spleen_12x24_ascii_23,
            "title": ezFBfont_spleen_16x32_ascii_30,
        }

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
            buf[: width * height * self.config.lcd.bpp // 8], x, y, width, height
        )

    def write_buffer(self, src, width, height, palette: framebuf.FrameBuffer):
        dest = framebuf.FrameBuffer(self.mv, width, height, framebuf.RGB565)
        dest.blit(src, 0, 0, -1, palette)

    def write_screen(self, x, y, width, height):
        self.blit(
            self.mv[: self.config.lcd.bpp // 8 * width * height], x, y, width, height
        )

    def blit_palette(
        self,
        src,
        x,
        y,
        width,
        height,
        palette: framebuf.FrameBuffer,
    ):
        self.write_buffer(src, width, height, palette)
        self.write_screen(x, y, width, height)

    def write_text(self, text, x, y, width, height, size, center=False):
        f = ezFBfont(
            framebuf.FrameBuffer(self.mv, width, height, framebuf.RGB565),
            self.fonts[size],
            cswap=True,
            fg=0,
            bg=0xFFFF,
            tkey=0xFFFF,
        )
        if center:
            f.write(text, x, y, halign="center", valign="center")
        else:
            f.write(text, x, y)

    def get_font_size(self, font):
        return (self.fonts[font].max_width(), self.fonts[font].height())
