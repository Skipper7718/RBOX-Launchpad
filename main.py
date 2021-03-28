from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys, os, json
from debug import printd

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI.ui", self)

        self.buttons = []
        for i in range(16):
            self.buttons.append(self.findChild(QtWidgets.QPushButton, f"button_{i}"))
            self.buttons[i].clicked.connect(self.button_clicked)
        self.selected_button = None

        self.port       = self.findChild(QtWidgets.QComboBox, "port")
        self.connect    = self.findChild(QtWidgets.QPushButton, "connect")
        self.connected  = self.findChild(QtWidgets.QCheckBox, "connected")
        self.run        = self.findChild(QtWidgets.QPushButton, "run")
        self.config     = self.findChild(QtWidgets.QPushButton, "config")
        self.selected   = self.findChild(QtWidgets.QLabel, "selected")
        self.color_r    = self.findChild(QtWidgets.QSpinBox, "color_r")
        self.color_g    = self.findChild(QtWidgets.QSpinBox, "color_g")
        self.color_b    = self.findChild(QtWidgets.QSpinBox, "color_b")
        self.byte1      = self.findChild(QtWidgets.QLineEdit, "byte1")
        self.byte2      = self.findChild(QtWidgets.QLineEdit, "byte2")
        self.byte3      = self.findChild(QtWidgets.QLineEdit, "byte3")
        self.apply      = self.findChild(QtWidgets.QPushButton, "apply")

        # self.set_button_status(False)

        self.show()
    
    def set_button_status(self, troof:bool):
        for i in range(16):
            self.buttons[i].setEnabled(troof)

    def button_clicked(self):
        self.selected_button = int(self.buttons.index(self.sender()))
        
        printd(f"Button {self.selected_button} was clicked")
        self.selected.setText(f"SELECTED {self.selected_button}")
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())