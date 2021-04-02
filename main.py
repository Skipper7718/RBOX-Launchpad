from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys, os, json
from serial.tools.list_ports import comports
from debug import printd
import midi_driver
import rboxdriver

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI.ui", self)

        self.buttons = []
        for i in range(16):
            self.buttons.append(self.findChild(QtWidgets.QPushButton, f"button_{i}"))
            self.buttons[i].clicked.connect(self.button_clicked)

        self.selected_button = None
        self.running = False
        self.rbox = None
        
        with open("config.json", "r") as f:
            self.settings = json.loads(f.read())

        self.serial_port    = self.findChild(QtWidgets.QComboBox, "serial_port")
        self.midi_port      = self.findChild(QtWidgets.QComboBox, "midi_port")
        self.connect        = self.findChild(QtWidgets.QPushButton, "connect")
        self.run            = self.findChild(QtWidgets.QPushButton, "run")
        self.config         = self.findChild(QtWidgets.QPushButton, "config")
        self.selected       = self.findChild(QtWidgets.QLabel, "selected")
        self.color_r        = self.findChild(QtWidgets.QSpinBox, "color_r")
        self.color_g        = self.findChild(QtWidgets.QSpinBox, "color_g")
        self.color_b        = self.findChild(QtWidgets.QSpinBox, "color_b")
        self.guibytes       = [self.findChild(QtWidgets.QLineEdit, "byte1"), self.findChild(QtWidgets.QLineEdit, "byte2"), self.findChild(QtWidgets.QLineEdit, "byte3")]
        self.apply          = self.findChild(QtWidgets.QPushButton, "apply")
        self.quit           = self.findChild(QtWidgets.QAction, "quit")

        self.quit.triggered.connect(lambda : exit())
        self.connect.clicked.connect(self.connect_launchpad)
        self.apply.clicked.connect(self.apply_changes)
        self.run.clicked.connect(self.run_engine)
        self.config.clicked.connect(self.stop_engine)

        # self.set_button_status(False)
        self.serial_port.addItems(list(str(i).split()[0] for i in comports()))
        self.midi_port.addItems(midi_driver.get_ports())

        self.show()
    
    def message(self,text):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("INFO")
        msg.setText(text)
        msg.exec_() 
    
    def set_button_status(self, troof:bool):
        for i in range(16):
            self.buttons[i].setEnabled(troof)
    
    def button_clicked(self):
        self.selected_button = int(self.buttons.index(self.sender()))
        
        printd(f"Button {self.selected_button} was clicked")
        self.selected.setText(f"SELECTED {self.selected_button}")

        for i in range(3):
            self.guibytes[i].setText(self.settings[self.selected_button][i])
    
    def connect_launchpad(self):
        self.rbox = rboxdriver.RBoxTask(self.serial_port.currentText(), int(self.midi_port.currentText().split()[0]))
        printd(self.rbox)
        self.connect.setEnabled(False)
        self.rbox.pi.send("a")
        self.message("Connected!")

    def apply_changes(self):
        self.message("Saved!")

        for i in range(3):

            text = self.guibytes[i].text()
            if(text != "" or self.selected_button != None):
                self.settings[self.selected_button][i] = text
        
        with open("config.json", "w") as f:
            f.write(json.dumps(self.settings, indent=4))

    def run_engine(self):
        self.set_button_status(False)
        self.rbox.start(self.settings)
        self.message("Engine running")

    def stop_engine(self):
        self.set_button_status(True)
        self.rbox.stop()
        self.message("Engine stopped, config possible")
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())