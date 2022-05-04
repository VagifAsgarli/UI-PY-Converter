import subprocess
import os
import sys
from pathlib import Path
# from threading import Thread

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (QMainWindow, QLineEdit, QFileDialog, QPushButton)
from PyQt5.QtGui import QIcon


# def pip_install():
#     try:
#         import auto_py_to_exe
#         del auto_py_to_exe
#     except ImportError:
#         print("Installing auto_py_to_exe...")
#         command = ["python", "-m", "pip", "install", "auto_py_to_exe"]
#         p = subprocess.Popen(
#             command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE).communicate()
        
#         if p[1]:
#             print("Error:", p[1].decode("utf-8"))

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.show()
    
    def setupUi(self):
        uic.loadUi("gui/gui.ui", self)
        self.setFixedSize(self.size())
        self.setWindowTitle("UI File Converter")
        self.setWindowIcon(QIcon("images/Aztu.png"))
        
        self.gosterge: QLineEdit
        
        self.uitopyButton: QPushButton
        self.uitopyButton.clicked.connect(self.ui_to_py)
        
        self.pytoexeButton: QPushButton
        self.pytoexeButton.clicked.connect(self.py_to_exe)
        
        self.selectButton: QPushButton
        self.selectButton.clicked.connect(self.SelectFile)
        
        self.uitopyButton.setEnabled(False)
        self.pytoexeButton.setEnabled(False)
    
    def SelectFile(self):
        u = QFileDialog.getOpenFileName(self, "Import File", os.getcwd(), "UI and Python Source File (*.ui *.py)")[0]
        if u:
            self.path = Path(u)
            self.dirname = os.path.dirname(self.path)
            self.basename = os.path.basename(self.path)
            self.gosterge.setText(str(self.path))
            if u.endswith(".ui"):
                self.uitopyButton.setEnabled(True)
                self.pytoexeButton.setEnabled(False)
            elif u.endswith(".py"):
                self.uitopyButton.setEnabled(False)
                self.pytoexeButton.setEnabled(True)
        
    def ui_to_py(self):
        command = [".\converter\pyuic5", "-x", str(self.path), "-o", str(self.path.with_suffix(".py"))]
        p = subprocess.Popen(command, stdout=sys.stdout, stderr=subprocess.PIPE, universal_newlines=True, bufsize=1, shell=True).communicate()
        if p[1]:
            print("Error:", p[1])
            return
        os.startfile(str(self.path.parent))

    def py_to_exe(self):
        command = [".\converter\pyinstaller", "--noconfirm", "--onefile", "--windowed", "--clean", str(self.path)]
        p = subprocess.Popen(command, stdout=sys.stdout, stderr=subprocess.PIPE, universal_newlines=True, bufsize=1, shell=True).communicate()
        if p[1]:
            print("Error:", p[1])
            return
        os.startfile(str(self.path.parent))
    
def main():
    # t = Thread(target=pip_install, daemon=True)
    # t.start()
    # t.join()
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()