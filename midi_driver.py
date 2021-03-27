from pygame import midi
import sys, serial, json
from serial.tools.list_ports import comports

class SerialController:
    def __init__(self, port:str, baud:int):
        self.connection = serial.Serial(port, baud)
    
    def read_button(self):
        byte = self.connection.read(1)
        return int.from_bytes(byte, "big")

class MidiController:
    def __init__(self, port:str):
        midi.init()
        self.connection = midi.Output(port)
    
    def send(self, payload:bytes):
        self.connection.write_short(payload[0], payload[1], payload[2])