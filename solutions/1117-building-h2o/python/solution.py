import threading
from typing import Callable

class H2O:
    def __init__(self):
        self.sem_h = threading.Semaphore(2)
        self.sem_o = threading.Semaphore(0)
        self.lock = threading.Lock()
        self.h_count = 0

    def hydrogen(self, releaseHydrogen: 'Callable[[], None]') -> None:
        self.sem_h.acquire()
        releaseHydrogen()
        with self.lock:
            self.h_count += 1
            if self.h_count == 2:
                self.h_count = 0
                self.sem_o.release()

    def oxygen(self, releaseOxygen: 'Callable[[], None]') -> None:
        self.sem_o.acquire()
        releaseOxygen()
        self.sem_h.release(2)

class Solution(H2O):
    pass
