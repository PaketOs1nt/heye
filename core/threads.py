import time
from threading import Lock, Thread
from typing import List

from config import THREADS_GC_TIMEOUT


class Threads:
    INSTANCE: "Threads"

    def __init__(self):
        self.lock = Lock()
        self.threads: List[Thread] = []
        self.gcthread = Thread(target=self.gc, daemon=True, name="GC Threads")
        self.gcthread.start()

    def gc(self):
        while True:
            with self.lock:
                for thread in self.threads.copy():
                    if not thread.is_alive():
                        thread.join()
                        self.threads.remove(thread)

            time.sleep(THREADS_GC_TIMEOUT)

    def post(self, thread: Thread):
        thread.daemon = True
        with self.lock:
            self.threads.append(thread)

        thread.start()


Threads.INSTANCE = Threads()
