import sys, os, json, midi_driver, rboxdriver
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from serial.tools.list_ports import comports
from debug import printd

#used for getting path for data embedded in the .exe
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path("GUI.ui"), self)

        #load config
        with open("config.json", "r") as f:
            self.settings = json.loads(f.read())

        #define variables
        self.selected_button = None
        self.running = False
        self.rbox = None
        self.buttons = []

        #get buttons for config
        for i in range(16):
            self.buttons.append(self.findChild(QtWidgets.QPushButton, f"button_{i}"))
            self.buttons[i].clicked.connect(self.button_clicked)

        #get widgets
        self.serial_port    = self.findChild(QtWidgets.QComboBox, "serial_port")
        self.midi_port      = self.findChild(QtWidgets.QComboBox, "midi_port")
        self.midi_port_in   = self.findChild(QtWidgets.QComboBox, "midi_port_in")
        self.connect        = self.findChild(QtWidgets.QPushButton, "connect")
        self.run            = self.findChild(QtWidgets.QPushButton, "run")
        self.config         = self.findChild(QtWidgets.QPushButton, "config")
        self.selected       = self.findChild(QtWidgets.QLabel, "selected")
        self.guibytes       = [self.findChild(QtWidgets.QLineEdit, "byte1"), self.findChild(QtWidgets.QLineEdit, "byte2"), self.findChild(QtWidgets.QLineEdit, "byte3")]
        self.apply          = self.findChild(QtWidgets.QPushButton, "apply")
        self.quit           = self.findChild(QtWidgets.QAction, "quit")
        self.to_tray        = self.findChild(QtWidgets.QAction, "to_tray")

        #connect functions
        self.to_tray.triggered.connect(lambda self: self.hide())
        self.quit.triggered.connect(lambda : exit())
        self.connect.clicked.connect(self.connect_launchpad)
        self.apply.clicked.connect(self.apply_changes)
        self.run.clicked.connect(self.run_engine)
        self.config.clicked.connect(self.stop_engine)

        #set default settings on boot
        self.config.setEnabled(False)
        self.apply.setEnabled(False)
        self.set_button_status(False)

        # fill combo box
        self.serial_port.addItems(list(str(i).split()[0] for i in comports()))
        self.midi_port.addItems(midi_driver.get_ports())
        self.midi_port_in.addItems(midi_driver.get_ports())
        
        ### SET UP TRAY ICON ###
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))

        self.showaction = QtWidgets.QAction("Show", self)
        self.exitaction = QtWidgets.QAction("Exit", self)
        self.showaction.triggered.connect(self.show)
        self.exitaction.triggered.connect(lambda : quit())

        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(self.showaction)
        tray_menu.addAction(self.exitaction)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        #execute window
        self.show()
    
    #message box
    def message(self,text):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("INFO")
        msg.setText(text)
        msg.exec_()

    #set enabled status of all buttons
    def set_button_status(self, troof:bool):
        for i in range(16):
            self.buttons[i].setEnabled(troof)

    
    def button_clicked(self):
        self.selected_button = self.buttons.index(self.sender())
        
        printd(f"Button {self.selected_button} was clicked") #debug

        self.selected.setText(f"SELECTED {self.selected_button}")

        for i, byte in enumerate(self.guibytes):
            self.byte.setText(self.settings[self.selected_button][i])

    def connect_launchpad(self):
        #create rbox object
        self.rbox = rboxdriver.RBoxTask(self.serial_port.currentText(), int(self.midi_port.currentText().split()[0]), int(self.midi_port_in.currentText().split()[0]))
        
        #debug
        printd("Trying to initialize component RboxTask\n"+self.serial_port.currentText()+ self.midi_port.currentText().split()[0]+ self.midi_port_in.currentText().split()[0])
        printd(self.rbox)
        
        #toggle connected mode
        self.rbox.pi.send       ("a") #send a for launchpad to start in performance mode
        self.message            ("Connected!")
        self.connect.setEnabled (False)
        self.apply.setEnabled   (True)
        self.set_button_status  (True)


    def apply_changes(self):
        for i, byte in enumerate(self.guibytes):
            text = self.byte.text()

            if(text != "" or self.selected_button != None):
                self.settings[self.selected_button][i] = text
        
        #write changes to config
        with open("config.json", "w") as f:
            f.write(json.dumps(self.settings, indent=4))


    def run_engine(self):
        #start engines
        self.rbox.start         (self.settings)
        #change ui
        self.set_button_status  (False)
        self.apply.setEnabled   (False)
        self.run.setEnabled     (False)
        self.config.setEnabled  (True)
        self.message            ("Engines running")


    def stop_engine(self):
        #stop engines
        self.rbox.stop          ()
        #change ui
        self.apply.setEnabled   (True)
        self.config.setEnabled  (False)
        self.run.setEnabled     (True)
        self.set_button_status  (True)
        self.message            ("Engines stopped, config possible")
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())