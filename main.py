import sys
from mainUI import mainUI
from PyQt5.QtWidgets import *
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = mainUI()
    win.show()
    sys.exit(app.exec_())
    sys.executable