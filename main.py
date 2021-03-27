from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys, os, json

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI.ui", self)

        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())