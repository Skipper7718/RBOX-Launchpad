import threading
from time import sleep
import sys
import midi_driver

from debug import printd

class RBoxTask:
    def __init__(self, port:str, midi:int):
        self._running = False
        self.config = None
        self.midi = midi_driver.MidiController(midi)
        self.pi = midi_driver.SerialController(port)
    
    def run(self):
        while (self._running):
            button = self.pi.read_button() -1

            printd(f"Button {button} was clicked!")
            s = f"{self.config[button][0]}{self.config[button][1]}{self.config[button][2]}"

            payload = bytes.fromhex(s)
            printd(payload.hex())

            self.midi.connection.write_short(payload[0], payload[1], payload[2])
    
    def start(self, config):
        self._running = True
        self.config = config
        threading.Thread(target=self.run).start()
    
    def stop(self):
        self._running = False