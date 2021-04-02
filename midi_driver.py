from pygame import midi
import sys, serial
from debug import printd
midi.init()

class SerialController:
    def __init__(self, port:str, baud:int=115200):
        self.connection = serial.Serial(port, baud)
    
    def read_button(self):
        byte = self.connection.read(1)
        return int.from_bytes(byte, "big")

class MidiController:
    def __init__(self, port:int):
        midi.init()
        self.connection = midi.Output(port)
    
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


# from time import sleep
# ser = SerialController("COM9", 115200)
# while True:
#     print(ser.read_button())