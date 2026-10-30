from hardware.ioconfig import IoConfig
from machine import Pin


class Buttons:
    def __init__(self, config: IoConfig) -> None:
        self.config = config
        # this is a better way than how scanners.py works but i don't want to refactor it there
        self.buttons = {
            n.lower(): Pin(b, Pin.IN, Pin.PULL_UP)
            for n, b in config.buttons.names.items()
        }
        self.last_time = None
        self.poll_interval = config.buttons.poll_rate_ms
        self.last_state = {n: self.is_down(n) for n in self.buttons}
        self.just_pressed = {n: False for n in self.buttons}

    def get_button(self, name):
        return self.buttons.get(name)

    def is_down(self, name):
        button = self.get_button(name.lower())
        if button is not None:
            return not button.value()
        raise ValueError(f"button {name} not recognized")

    def update(self, time_ms):
        if self.last_time is None:
            self.last_time = time_ms

        for b in self.just_pressed:
            self.just_pressed[b] = False

        dt = time_ms - self.last_time
        if dt >= self.poll_interval:
            for b in self.buttons:
                down = self.is_down(b)
                if down and not self.last_state[b]:
                    self.just_pressed[b] = down
                self.last_state[b] = down
            self.last_time = time_ms

    def is_pressed(self, name):
        name = name.lower()
        button = self.get_button(name)
        if button is not None:
            return self.just_pressed[name]
        raise ValueError(f"button {name} not recognized")

    # could be useful if you want to iterate through the pressed keys
    def get_pressed(self):
        return [b for b, p in self.just_pressed.items() if p]
