import engine.core.config as EngineConfig
import hardware.ioconfig as IOConfig
import graphics.graphicsconfig as GraphicsConfig
from hardware.lcd import LCD
from hardware.spi import SPIHandler
from hardware.scanners import Scanners
from hardware.sd import SD
from hardware.buttons import Buttons
from engine.core.container import HandlerContainer
from engine.core.rfid import RFIDProcessor


class GameContext:
    def __init__(self, mode=None) -> None:
        self.engine_config = EngineConfig.load_config(mode)
        self.io_config = IOConfig.load_config()
        self.graphics_config = GraphicsConfig.load_config()

        # not super clean, but better than passing in configs to constructors
        if self.io_config.lcd.bpp != self.graphics_config.textures["bytes_per_pixel"]:
            raise ValueError("graphics and io configs bpp must match, check both")

        self.spi_handler = SPIHandler(self.io_config)
        self.sd = SD(self.spi_handler, self.io_config)
        if self.sd.error is not None:
            raise self.sd.error
        self.lcd = LCD(self.spi_handler, self.io_config)
        self.scanners = Scanners(self.spi_handler, self.io_config)
        self.buttons = Buttons(self.io_config)

        self.handlers = HandlerContainer(self.engine_config)
        self.rfid_processor = RFIDProcessor(self.scanners, self.engine_config)
