from game.context import GameContext
from game.gameloop import Game
from game.states.displayerror import display_error
import machine
import time


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
                display_error(ctx, e)
                while not ctx.buttons.is_pressed("a"):
                    ctx.buttons.update(time.ticks_ms())
                    time.sleep_ms(1)
                time.sleep(0.5)


if __name__ == "__main__":
    main()
