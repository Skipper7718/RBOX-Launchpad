import threading
from time import sleep
from textwrap import wrap
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
        self.query = []
    
    def get_index(self, s:str):
        for conf in self.config:
            if(conf[1] == s):
                return self.config.index(conf)
        return None
    
    def run_data_engine(self):
        printd("START MAIN ENGINE")
        while True:
            if not self._running: break
            button = self.pi.read_button() - 1
            if(button != None):
                if(button < 16 and button >= 0):

                    printd(f"Motion trigger: Button ID {button}")
                    s = f"{self.config[button][0]}{self.config[button][1]}{self.config[button][2]}"

                    payload = bytes.fromhex(s)
                    printd(f"generated payload: {payload.hex()}")

                    self.midi.connection.write_short(payload[0], payload[1], payload[2])
        printd("STOP MAIN ENGINE")
    
    def run_rgb_engine(self):
        printd("START RGB ENGINE")
        while self._running:
            data = self.midi.input.read(3)
            if (data!=None):
                self.query.append(data)
                
        printd("STOP RGB ENGINE")
    
    def run_query_engine(self):
        printd("START QUERY ENGINE")
        while self._running:
            if(len(self.query) < 1): continue
            dataquery = self.query[0]
            data = wrap(bytearray(dataquery[0][0]).hex(), 2)[:-1]
            printd(data)
            if(data[0] == "90"):
                index = self.get_index(data[1])
                printd(f"GOT RGB SIGNAL: Button {data[1]}, pallette {data[2]}\nIndex >> {index}")

                if (index != None):
                    self.pi.send_rgb(index, int(data[2], 16))
            self.query.pop(0)
            sleep(0.016)
        printd("STOP QUERY ENGINE")

    def start(self, config):
        self._running = True
        self.config = config

        self.dataengine = threading.Thread(target=self.run_data_engine)
        self.dataengine.daemon = True
        self.dataengine.start()
    
        self.rgbengine1 = threading.Thread(target=self.run_rgb_engine)
        self.rgbengine1.daemon = True
        self.rgbengine1.start()

        self.rgbengine = threading.Thread(target=self.run_rgb_engine)
        self.rgbengine.daemon = True
        self.rgbengine.start()

        self.queryengine = threading.Thread(target=self.run_query_engine)
        self.queryengine.daemon = True
        self.queryengine.start()
    
    def stop(self):
        self._running = False

        self.dataengine.join()
        self.rgbengine.join()
        self.rgbengine1.join()
        self.queryengine.join()