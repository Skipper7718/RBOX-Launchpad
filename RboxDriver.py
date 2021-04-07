import threading
from time import sleep
import sys
import midi_driver
import threading

from debug import printd

class RBoxTask:
    def __init__(self, port:str, midiout:int, midiin:int):
        self._running = False
        self.config = None
        self.midi = midi_driver.MidiController(midiout, midiin)
        self.pi = midi_driver.SerialController(port)
    
    def get_index(self, s:str):
        for conf in self.config:
            if(conf[1] == s):
                return self.config.index(conf)
        return None
    
    def run_data_engine(self):
        while True:
            if not self._running: break
            button = self.pi.read_button() - 1
            if(button != None):
                if(button < 16 and button >= 0):

                    printd(f"Button {button} was clicked!")
                    s = f"{self.config[button][0]}{self.config[button][1]}{self.config[button][2]}"

                    payload = bytes.fromhex(s)
                    printd(payload.hex())
                    printd(payload)

                    self.midi.connection.write_short(payload[0], payload[1], payload[2])
        printd("EXIT MAIN ENGINE")
    
    def run_rgb_engine(self):
        while self._running:
            data = self.midi.read_rgb_data()

            if(data != None):

                if(data[0] == "90"):
                    index = self.get_index(data[1])

                    if (index != None):
                        self.pi.send_rgb(index, int(data[2], 16))
        printd("EXIT RGB ENGINE")
        
    def start(self, config):
        self._running = True
        self.config = config

        self.dataengine = threading.Thread(target=self.run_data_engine, daemon=True)
        self.dataengine.daemon = True
        self.dataengine.start()

        self.rgbengine = threading.Thread(target=self.run_rgb_engine)
        self.rgbengine.daemon = True
        self.rgbengine.start()
    
    def stop(self):
        self._running = False

        self.dataengine.join()
        self.rgbengine.join()