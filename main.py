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
from hardware.buttons import Buttons
import _thread as thread
import sys

h_config = ioconfig.load_config()
g_config = graphicsconfig.load_config()
spi = SPIHandler(h_config)
sd = SD(spi, h_config)
lcd = LCD(spi, h_config)
buttons = Buttons(h_config)

animation = Animation("animation example", sd, g_config)

animation.gen_buffer()

playing = True
running = True
lock = thread.allocate_lock()
error = None


def render():
    global error, running
    try:
        while running:
            time_ms = time.ticks_ms()
            if playing:
                animation.play(time_ms)
                animation.draw(lcd)
            else:
                time.sleep_ms(1)
    except Exception as e:
        with lock:
            running = False
            sys.print_exception(e)
            error = e


def game():
    global playing, running
    while running:
        time_ms = time.ticks_ms()
        buttons.update(time_ms)
        if buttons.is_pressed("a"):
            playing = not playing
        with lock:
            if error is not None:
                running = False
                raise error
        time.sleep_ms(1)


thread.start_new_thread(render, ())
try:
    game()
finally:
    running = False
