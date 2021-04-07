from pygame import midi
import sys, serial, signal
from debug import printd
from textwrap import wrap
midi.init()


def interrupt():
    printd("got interrupt signal")
    signal.alarm(0)
    return None


class SerialController:
    def __init__(self, port:str, baud:int=115200):
        self.connection = serial.Serial(port, baud, timeout=2)
    
    def read_button(self):
        byte = self.connection.read(1)
        return int.from_bytes(byte, "big")
    
    def send(self, payload):
        self.connection.write(payload.encode())
        self.connection.close()
        self.connection.open()
    
    def send_rgb(self, button, rgb):
        message = f"{button}|{rgb}"
        self.send(len(message))
        self.send(message)

class MidiController:
    def __init__(self, out_port:int, in_port:int):
        midi.init()
        self.connection = midi.Output(out_port)
        self.input = midi.Input(in_port)
    
    def send(self, payload:bytes):
        self.connection.write_short(payload[0], payload[1], payload[2])
    
    def read_rgb_data(self):
        if(self.input.poll()):
            return wrap(bytearray(self.input.read(3)[0][0]).hex(),2)[:-1]
        else:
            return None
    
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