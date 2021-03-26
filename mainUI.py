import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from addrule import addrule
from vennUI import vennUI
from findrule import findrule

class mainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('venn relation')
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        layout.addStretch(1)
        
        label = QLabel("subject - predicate - object")
        label.setAlignment(Qt.AlignCenter)
        font = label.font()
        font.setPointSize(15)
        label.setFont(font)
        self.label = label


        btn = QPushButton("규칙추가")
        btn.clicked.connect(self.onButtonClicked)
        layout.addWidget(label)
        layout.addWidget(btn)

        btn2 = QPushButton("쿼리실행")
        btn2.clicked.connect(self.onButton2Clicked)
        layout.addWidget(btn2)
        layout.addStretch(1)


        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)



    def onButtonClicked(self):
        win = vennUI()
        win.showModal()

        r = win.showModal()
        #if r:
        #    text = win.outputText()
        #    self.label.setText(text)
        #text = win.edit.text()
    def onButton2Clicked(self):
        win = findrule()
        win.showModal()

    def show(self):
        super().show()