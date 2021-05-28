import sys, serial, signal
from pygame import midi
from debug import printd
from textwrap import wrap
from time import sleep

midi.init() #initialize pygame midi component

#serial controller class
class SerialController:
    def __init__(self, port:str, baud:int=115200):
        self.connection = serial.Serial(port, baud, timeout=2)
    
    #read button number from byte
    def read_button(self):
        # if not self.connection.is_open: #I dont know why, but sometimes the connection just closes
        #     self.connection.open()
        waiting = self.connection.in_waiting
        if(waiting > 0):
            byte = self.connection.read(self.connection.in_waiting) #recieve waiting bytes
            button = int.from_bytes(byte, "little")
            if(button < 16 and button >=0):
                return button
            elif(button == 2573):
                return 10
    
    #just write a string to launchpad
    def send(self, payload):
        self.connection.write(payload.encode())
        # self.connection.close()
        # self.connection.open()
    
    def send_rgb(self, button, rgb):

        #fill up with "0"
        button = str(button)
        while (len(button) < 2):
            button = "0" + button

        rgb = str(rgb)
        while (len(rgb) < 3):
            rgb = "0" + rgb
        
        #message to send to launchpad
        message = f"{button}.{rgb}"

        #transmit!
        self.send(message)
        self.connection.flushInput() #there is a bug, where read bytes remain in input buffer after this message is sent
        
        printd(f"sending message {message}")#debug


#midi controller class
class MidiController:
    def __init__(self, out_port:int, in_port:int):

        self.connection = midi.Output(out_port) #set port to set button response
        self.input = midi.Input(in_port)        #set port to recieve RGB signals
    
    #send 3 byte long payload to midi port
    def send(self, payload:bytes):
        self.connection.write_short(payload[0], payload[1], payload[2])

#used for the qcomboboxes
def get_ports() -> list:
    arr = []
    __id = 0

    while True:
        __info = midi.get_device_info(__id)

        if(__info != None):
            #I stands for input port and I for input port
            arr.append(f"{__id} {__info[1].decode()} I") if __info[2] == 1 else arr.append(f"{__id} {__info[1].decode()} O")

        else: break #quit while loop when reading ports is done

        __id += 1

    return arr