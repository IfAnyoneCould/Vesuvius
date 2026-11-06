from game.context import GameContext
from game.gameloop import Game
from game.states.displayerror import display_error
import machine
import time
import gc
import io
import sys


def main():
    machine.freq(150_000_000, 150_000_000)  # pyright: ignore[reportCallIssue]
    ctx = None
    while True:
        try:
            if ctx is None:
                ctx = GameContext()
            game = Game(ctx)
            game.loop()

        except Exception as e:
            if ctx is not None:
                # reloading context is slow but its not like were pressed for time here
                err = display_error(ctx, e)
                try:
                    ctx.sd.use_sd()
                    with open("/sd/logs/errors.txt", "a") as f:
                        f.write("ticks: " + str(time.ticks_ms()) + " | " + err + "\n")
                except Exception as ee:
                    ctx.framebuf.text(
                        "log failed: " + str(ee),
                        10,
                        ctx.io_config.lcd.resy - 10,
                        0xFFFF,
                    )
                    ctx.lcd.use_lcd()
                    ctx.lcd.blit(
                        ctx.mv, 0, 0, ctx.io_config.lcd.resx, ctx.io_config.lcd.resy
                    )
                while not ctx.buttons.is_pressed("a"):
                    ctx.buttons.update(time.ticks_ms())
                    time.sleep_ms(1)
                time.sleep(0.5)
            else:
                try:
                    ctx = GameContext(kind="minimal")
                    display_error(ctx, e)
                    ctx = None
                    time.sleep(5)
                except Exception:
                    # honestly, idk
                    return
        gc.collect()


if __name__ == "__main__":
    main()
