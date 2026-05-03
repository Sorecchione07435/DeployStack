import sys
import threading
import time

class Spinner:
    def __init__(self, message="Processing"):
        self.spinner = ["|", "/", "-", "\\"]
        self.idx = 0
        self.running = False
        self.thread = None
        self.message = message
        self._lock = threading.Lock()

    def start(self):
        self.running = True
        self.idx = 0
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def _spin(self):
        while self.running:
            with self._lock:
                sys.stdout.write(f"\r{self.message} {self.spinner[self.idx]}")
                sys.stdout.flush()
                self.idx = (self.idx + 1) % len(self.spinner)
            time.sleep(0.1)

    def pause(self):
        self.running = False
        if self.thread:
            self.thread.join()

        sys.stdout.write(f"\r{' ' * (len(self.message) + 4)}\r")
        sys.stdout.flush()

    def resume(self):
        self.running = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def stop(self, done_message="DONE", color="yellow", width=80):
        color_codes = {
            "yellow": "\033[33m",
            "red": "\033[31m",
            "green": "\033[32m",
            "reset": "\033[0m"
        }
        self.running = False
        if self.thread:
            self.thread.join()

        color_code = color_codes.get(color, "")
        reset_code = color_codes["reset"]
        message_aligned = self.message.ljust(width)
        sys.stdout.write(f"\r{message_aligned}[ {color_code}{done_message}{reset_code} ]\n")
        sys.stdout.flush()