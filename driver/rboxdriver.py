import threading, sys, midi_driver, threading, json, pyautogui
from time import sleep
from textwrap import wrap
from debug import printd

#Class called from main
class RBoxTask:
    def __init__(self, port:str, midiout:int, midiin:int):
        self.__running = False
        self.config = None
        #call midi controller
        self.midi = midi_driver.MidiController(midiout, midiin)
        #call serial controller
        self.pi = midi_driver.SerialController(port)
        self.query = []
    
    #get index of button determined by the midi config
    def get_index(self, s:str):
        for conf in self.config:
            if(conf[1] == s):
                return self.config.index(conf)
        return None
    
    #engine for handling button presses
    def run_data_engine(self):
        printd("START MAIN ENGINE")

        while True:
            if not self.__running: break #close process when __running is false
            button = self.pi.read_button() #red button input from USB
            if(button != None):
                if(button < 16 and button >= 0):

                    printd(f"Motion trigger: Button ID {button}")#debug

                    s = f"{self.config[button][0]}{self.config[button][1]}{self.config[button][2]}"
                    payload = bytes.fromhex(s)

                    printd(f"generated payload: {payload.hex()}")#debug

                    self.midi.connection.write_short(payload[0], payload[1], payload[2]) #write to midi port

        printd("STOP MAIN ENGINE")

    #puts midi signals recieved into the query
    #this process runs twice to ensure all data is captured
    def run_rgb_engine(self):
        printd("START RGB ENGINE")

        while self.__running:
            if(self.midi.input.poll()):
                data = self.midi.input.read(1)
                self.query.append(data)

                printd(data)#debug
                
        printd("STOP RGB ENGINE")
    
    #process that handles the query
    def run_query_engine(self):
        printd("START QUERY ENGINE")

        while self.__running:
            #some invalid messages will give IndexError and sometimes other errors
            try:
                dataquery = self.query[0]
                data = wrap(bytearray(dataquery[0][0]).hex(), 2)[:-1]
            except:
                if(len(self.query) > 0):
                    self.query.pop(0)
                continue #check next entry

            if(data[0] == "90"): #only NoteOn messages will be interpreted as RGB signals
                index = self.get_index(data[1]) #get button index to send to launchpad

                printd(f"GOT RGB SIGNAL: Button {data[1]}, pallette {data[2]}\nIndex >> {index}")#debug

                if (index != None):
                    #relay message to launchpad
                    self.pi.send_rgb(index, int(data[2], 16))

            if(len(self.query) > 0):
                self.query.pop(0)
            sleep(0.002) #sleep for 2ms

        printd("STOP QUERY ENGINE")
    
    #library used for multiprocessing purposes. The RBOX has two engines for handling input so it can recieve the signals more precise
    #there is a bug where one process is failing, thats why I will be switching the engine to rust soon
    def start(self, config):
        self.__running = True
        self.config = config

        #start engine for handling button inputs
        self.dataengine         = threading.Thread(target=self.run_data_engine)
        self.dataengine.daemon  = True
        self.dataengine.start   ()
    
        #start engines for handling input
        self.rgbengine1         = threading.Thread(target=self.run_rgb_engine)
        self.rgbengine1.daemon  = True
        self.rgbengine1.start   ()

        self.rgbengine          = threading.Thread(target=self.run_rgb_engine)
        self.rgbengine.daemon   = True
        self.rgbengine.start    ()

        #start engine for processing the query
        self.queryengine        = threading.Thread(target=self.run_query_engine)
        self.queryengine.daemon = True
        self.queryengine.start  ()
    
    def stop(self):
        self.__running = False

        self.dataengine .join()
        self.rgbengine  .join()
        self.rgbengine1 .join()
        self.queryengine.join()

class RBoxTilt:
    def __init__(self, port:str):
        self.pi = midi_driver.SerialController(port)
        self.__running = False

        with open("tiltconfig.json", "r") as file:
            self.config = json.loads(file.read())
    
    def run_tilt_engine(self):
        printd("STARTING TILT ENGINE")
        while True:
            if not self.__running: break

            button = self.pi.read_button()

            if(button != None):
                if(button < 16 and button >= 0):
                    printd(f"MOTION TRIGGER: {button}")
                    try:
                        pyautogui.hotkey(*self.config[button])
                    except:
                        pass

        printd("STOPPING TILT ENGINE")
    
    def start(self):
        self.__running              = True
        self.tiltengine             = threading.Thread(target=self.run_tilt_engine)
        self.tiltengine.daemon      = True
        self.tiltengine.start       ()
    
    def stop(self):
        self.__running      = False
        self.tiltengine     .join()