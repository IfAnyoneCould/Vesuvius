from game.context import GameContext


def main():
    try:
        ctx = GameContext()

    except Exception as e:
        with open("/logs/errors.txt", "a+") as f:
            f.write(e)
        # TODO function that does stuff here, notifies players, etc
        main()


if __name__ == "main.py":
    main()
