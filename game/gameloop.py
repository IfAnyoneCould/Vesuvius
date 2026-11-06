from game.context import GameContext
from game.states.farm import Farm
from game.states.modeselect import ModeSelect
from game.states.startmenu import StartMenu
from game.states.testing import Testing
import time


class Game:
    def __init__(self, ctx: GameContext) -> None:
        self.ctx = ctx
        self.round = 0
        self.turn = 0
        self.player_order = []
        self.running = True
        self.last_state = "none"
        self.state = "start_menu"
        self.states = {
            "start_menu": self.start_menu,
            "mode_select": self.mode_select,
            "testing": self.testing,
        }

    def set_state(self, state):
        self.last_state = self.state
        self.state = state

    def start_menu(self):
        s = StartMenu(self.ctx)
        s.run()
        self.set_state("mode_select")

    def mode_select(self):
        s = ModeSelect(self.ctx)
        mode = s.run()
        if mode == "standard":
            self.set_state("player_init")
        elif mode == "back":
            self.set_state(self.last_state)
        else:
            self.set_state("testing")

    def testing(self):
        s = Testing(self.ctx)
        s.run()
        self.set_state(self.last_state)

    def start(self):
        pass

    def loop(self):
        while self.running:
            # in here run a function that looks at the current turn, round and rfid tags
            self.states[self.state]()
            time.sleep_ms(1)
