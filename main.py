from game.context import GameContext
from game.gameloop import Game
import machine


def main():
    machine.freq(150_000_000, 150_000_000)  # pyright: ignore[reportCallIssue]
    try:
        ctx = GameContext()
        game = Game(ctx)
        game.loop()

    except Exception as e:
        with open("/logs/errors.txt", "a+") as f:
            f.write(e)
        # TODO function that does stuff here, notifies players, etc
        main()


if __name__ == "__main__":
    main()
