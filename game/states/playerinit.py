from game.context import GameContext
from game.threadhelper import ThreadHelper


class PlayerInit:
    def __init__(self, ctx: GameContext) -> None:
        self.ctx = ctx
        self.thread = ThreadHelper()

    def render(self):
        pass

    def render_cleanup(self):
        pass

    def player_init(self):
        pass

    def run(self):
        pass
