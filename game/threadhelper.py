import _thread as thread
import time
import sys


class ThreadHelper:
    def __init__(self) -> None:
        self.running = True
        self.done = False
        self.lock = thread.allocate_lock()
        self.error: Exception | None = None

    def start(self, args):
        try:
            thread.start_new_thread(self.render, args)
        except OSError:
            time.sleep_ms(5)
            thread.start_new_thread(self.render, args)

    def stop(self):
        with self.lock:
            self.running = False

    def wait(self):
        try:
            while self.running:
                with self.lock:
                    if self.error is not None:
                        self.running = False
                        raise self.error
                time.sleep_ms(1)
        finally:
            self.running = False
            while not self.done:
                time.sleep_ms(1)

    def render(self, body, args, end, endargs):
        try:
            body(*args)
        except Exception as e:
            with self.lock:
                sys.print_exception(e)
                self.error = e
                self.running = False
        finally:
            try:
                end(*endargs)
            finally:
                with self.lock:
                    self.done = True
