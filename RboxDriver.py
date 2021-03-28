import threading
from time import sleep
import sys

from debug import printd

class RBoxTask:
    def __init__(self):
        self._running = False
    
    def run(self):
        while (self._running):
            pass # here will be the Rbox main loop
    
    def start(self):
        self._running = True
        threading.Thread(target=self.run).start()
    
    def stop(self):
        self._running = False