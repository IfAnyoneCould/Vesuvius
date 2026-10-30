from game.context import GameContext
import game.gamestate as GameState


def main():
    try:
        ctx = GameContext()

    except Exception as e:
        with open("/logs/errors.txt", "a+") as f:
            f.write(e)
        # TODO function that does stuff here, notifies players, etc
        main()


# if __name__ == "__main__":
#    main()


# TESTING
# im not loading a full ctx because i haven't wired up all of the stuff yet
#
import hardware.ioconfig as ioconfig
from graphics.animation import Animation
from hardware.sd import SD
from hardware.spi import SPIHandler
import graphics.graphicsconfig as graphicsconfig
import time
from hardware.lcd import LCD

h_config = ioconfig.load_config()
g_config = graphicsconfig.load_config()
spi = SPIHandler(h_config)
sd = SD(spi, h_config)
lcd = LCD(spi, h_config)
animation = Animation("animation example", sd, g_config)

animation.gen_buffer()
while True:
    time_ms = time.ticks_ms()
    animation.play(time_ms)
    animation.draw(lcd)
