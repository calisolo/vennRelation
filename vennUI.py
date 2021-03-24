import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from addrule import addrule
from addrule2 import addrule2


class vennUI(QDialog):

    global radionum
    radionum =1

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('관계모델')
        self.setGeometry(100, 100, 200, 100)
        layout = QVBoxLayout()
        layout.addStretch(1)

        venn1 = QPixmap('./img/testimage.PNG')
        venn2 = QPixmap('./img/testimage2.PNG')
        venn1_img = QLabel()
        venn1_img.setPixmap(venn1)
        venn2_img = QLabel()
        venn2_img.setPixmap(venn2)
        # 벤다이어그램 이미지 임포트

        self.radio1 = QRadioButton("포함모델", self)
        self.radio1.setChecked(True)
        self.radio1.clicked.connect(self.radioButtonClicked)
        self.radio2 = QRadioButton("일부겹침모델", self)
        self.radio2.clicked.connect(self.radioButtonClicked)
        # 라디오버튼 선언및 라디오버튼 연결
        outputText = "테스트"






        subLayout1 = QHBoxLayout()
        subLayout2 = QHBoxLayout()
        subLayoutRadio = QHBoxLayout()

        btnOK = QPushButton("확인")
        btnOK.clicked.connect(self.onOKButtonClicked)
        btnCancel = QPushButton("취소")
        btnCancel.clicked.connect(self.onCancelButtonClicked)


        subLayout1.addWidget(venn1_img)
        subLayout1.addWidget(venn2_img)

        subLayoutRadio.addWidget(self.radio1)
        subLayoutRadio.addWidget(self.radio2)

        subLayout2.addWidget(btnOK)
        subLayout2.addWidget(btnCancel)
        layout.addLayout(subLayout1)
        layout.addLayout(subLayoutRadio)
        layout.addLayout(subLayout2)
        layout.addStretch(1)
        self.setLayout(layout)

    def radioButtonClicked(self):
        global radionum

        if self.radio1.isChecked():  radionum = 1
        elif self.radio2.isChecked(): radionum = 2





    def onOKButtonClicked(self):
        global radionum

        if radionum == 1: win = addrule()
        elif radionum == 2: win = addrule2()


        win.showModal()
        #print(win.tripleO) #win.tripleS tripleO로 subwindow에서 넣은것 받아오기

        self.accept()

    def onCancelButtonClicked(self):
        self.reject()




    def showModal(self):
        return super().exec_()


