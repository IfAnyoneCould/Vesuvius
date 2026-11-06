from game.context import GameContext
import io
import sys
import time


def display_error(ctx: GameContext, error: Exception, first=True):
    if not first:
        return
    w = ctx.io_config.lcd.resx
    h = ctx.io_config.lcd.resy
    err = io.StringIO()
    sys.print_exception(error, err)  # pyright: ignore[reportArgumentType]
    ctx.framebuf.fill(0)
    offset = 10
    for l in err.getvalue().splitlines():
        chars_per_line = 38
        sub = [l[i : i + chars_per_line] for i in range(0, len(l), chars_per_line)]
        for s in sub:
            ctx.framebuf.text(
                s, 10, offset, 0xFFFF
            )  # stupid pyright thinks there is an error
            offset += 10
    ctx.lcd.use_lcd()
    ctx.lcd.blit(ctx.mv, 0, 0, w, h)
    try:
        ctx.sd.use_sd()
        with open("/sd/logs/errors.txt", "a") as f:
            f.write("ticks: " + str(time.ticks_ms()) + " | " + err.getvalue() + "\n")
    except Exception as e:
        display_error(ctx, e, first=False)
