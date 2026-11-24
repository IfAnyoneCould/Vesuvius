from game.threadhelper import ThreadHelper
from game.context import GameContext
import time


class ShowTags:
    def __init__(self, ctx: GameContext) -> None:
        self.ctx = ctx
        self.thread = ThreadHelper()
        self.tags = [None] * ctx.io_config.scanners.count
        self.changed = False

    def render(self):
        w = self.ctx.lcd.resx
        h = self.ctx.lcd.resy
        self.ctx.lcd.use_lcd()
        while self.thread.running:
            if self.changed:
                with self.thread.lock:
                    self.changed = False
                    tags = self.tags.copy()
                self.ctx.framebuf.fill(0)
                offset = 10
                for l in tags:
                    if l is not None:
                        self.ctx.framebuf.text(l, 10, offset, 0xFFFF)
                    offset += 10
                self.ctx.lcd.blit(self.ctx.mv, 0, 0, w, h)
            else:
                time.sleep_ms(1)

    def render_cleanup(self):
        pass

    def run(self):
        self.thread.start((self.render, (), self.render_cleanup, ()))
        last = []
        try:
            while self.thread.running:
                rfids = self.ctx.rfid_processor.poll_all()
                with self.thread.lock:
                    if last != rfids:
                        last = rfids
                        self.changed = True
                        self.tags = [
                            " | ".join([str(i) for i in v]) for k, v in rfids.items()
                        ]
                self.ctx.buttons.update(time.ticks_ms())
                if self.ctx.buttons.is_pressed("b"):
                    self.thread.stop()
        finally:
            if self.thread.running:
                self.thread.stop()
            self.thread.wait()
