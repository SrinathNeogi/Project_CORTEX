# main.py

import torch 
import sys
from PyQt5.QtWidgets import QApplication
from UI.main_window3 import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()