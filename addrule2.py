import sys
from PyQt5.QtWidgets import *


class addrule2(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        self.setWindowTitle('Sub Window')
        self.setGeometry(100, 100, 200, 100)
        layout = QVBoxLayout()
        layout.addStretch(1)
        edit = QLineEdit()
        font = edit.font()
        font.setPointSize(20)
        edit.setFont(font)
        self.edit = edit
        subLayout = QHBoxLayout()

        btnOK = QPushButton("확인")
        btnOK.clicked.connect(self.onOKButtonClicked)
        btnCancel = QPushButton("취소")
        btnCancel.clicked.connect(self.onCancelButtonClicked)
        layout.addWidget(edit)

        subLayout.addWidget(btnOK)
        subLayout.addWidget(btnCancel)
        layout.addLayout(subLayout)
        layout.addStretch(1)
        self.setLayout(layout)

    def onOKButtonClicked(self):


        f = open("./dump/simplifiedEntity.txt", 'r')
        f2 = open("./dump/simplifiedEntity.txt", 'a')


        lineInput = self.edit.text()
        triple = lineInput.split()
        self.tripleS= triple[0]
        self.tripleP= triple[1]
        self.tripleO= triple[2]


        subjectDepthValue = 0
        objectDepthValue = 0
        skipS =0
        skipO =0


        # 일부겹침 s-p-o 정의
        # 1)s-p가 존재시 o depthvalue 에 같은값대입
        # 2)o-p가 존재시 s depthvalue에 같은값대입
        # 둘다 없을경우 0 0 대입
        # 둘다 있으며 서로 다른값일경우 둘중 이차원값이 있는쪽으로 보정후 더 많은값이 쏠린쪽으로 통일

        while True:
            line = f.readline()
            if not line: break

            dumpTriple = line.split()
            if len(dumpTriple) == 3:
                if self.tripleS == dumpTriple[0]:
                    if self.tripleP+"Depth" == dumpTriple[1]:
                        objectDepthValue = dumpTriple[2]
                        subjectDepthValue = dumpTriple[2]
                        skipS = 1
                        break

                if self.tripleO == dumpTriple[0]:
                    if self.tripleP+"Depth" == dumpTriple[1]:
                        subjectDepthValue = dumpTriple[2]
                        objectDepthValue = dumpTriple[2]
                        skipO = 1
                        break


        f.close()



        definedData = triple[0] + " " + triple[1] + " " + triple[2] + "\n"

        subjectDepth = triple[0] + " " + triple[1] + "Depth " + str(subjectDepthValue) + "\n"

        objectDepth = triple[2] + " " + triple[1] + "Depth " + str(objectDepthValue) + "\n"

        print(subjectDepth + objectDepth + "relation defined")




        f2.write("".join(definedData))

        if skipS == 0:
            f2.write("".join(subjectDepth))
        if skipO == 0:
            f2.write("".join(objectDepth))

        self.accept()

    def onCancelButtonClicked(self):
        self.reject()

    def showModal(self):
        return super().exec_()