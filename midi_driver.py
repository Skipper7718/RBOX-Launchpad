from pygame import midi
import sys, serial, signal
from debug import printd
from textwrap import wrap
from time import sleep
midi.init()


class SerialController:
    def __init__(self, port:str, baud:int=115200):
        self.connection = serial.Serial(port, baud, timeout=2)
    
    def read_button(self):
        if not self.connection.is_open:
            self.connection.open
        byte = self.connection.read(self.connection.inWaiting())
        return int.from_bytes(byte, "big")
    
    def send(self, payload):
        self.connection.write(payload.encode())
        # self.connection.close()
        # self.connection.open()
    
    def send_rgb(self, button, rgb):
        if(len(str(button)) < 2):
            button1 = f"0{button}"
        else:
            button1 = str(button)

        if(len(str(rgb)) < 2):
            rgb1 = f"00{rgb}"
        elif(len(str(rgb)) < 3):
            rgb1 = f"0{rgb}"
        else:
            rgb1 = str(rgb)
        message = f"{button1}.{rgb1}"
        self.send(message)

        self.connection.flushInput()
        
        printd(f"sending message {message}")

class MidiController:
    def __init__(self, out_port:int, in_port:int):
        midi.init()
        self.connection = midi.Output(out_port)
        self.input = midi.Input(in_port)
    
    def send(self, payload:bytes):
        self.connection.write_short(payload[0], payload[1], payload[2])
    
def get_ports() -> list:
    arr = []
    _id = 0
    while True:
        _info = midi.get_device_info(_id)
        if(_info != None):
            arr.append(f"{_id} {_info[1].decode()} I") if _info[2] == 1 else arr.append(f"{_id} {_info[1].decode()} O")
        else: break
        _id += 1
    return arr