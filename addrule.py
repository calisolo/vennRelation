import sys
import re
from PyQt5.QtWidgets import *


class addrule(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        self.setWindowTitle('Sub Window')
        self.setGeometry(100, 100, 300, 100)
        layout = QVBoxLayout()
        layout.addStretch(1)
        edit = QLineEdit()
        font = edit.font()
        font.setPointSize(20)
        edit.setFont(font)
        self.edit = edit
        subLayout = QHBoxLayout()

        btnOK = QPushButton("OK")
        btnOK.clicked.connect(self.onOKButtonClicked)
        btnCancel = QPushButton("Cancel")
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
        objectDepthValue = -1
        skipS = 0
        skipO = 0
        p = re.compile("[^0-9, -]")


        # 포함 s-p-o 정의
        # 1)s-p가 존재시 o depthvalue 에 반영값대입
        # 2)o-p가 존재시 s depthvalue에 반영값대입
        # 둘다 없을경우 0 -1 대입
        # 이미 있는값이 1차원일경우 레퍼런스값 추가한 이차원값대입
        # 이미있는값이 2차원일경우 받아서 -1대입

        while True:
            line = f.readline()
            if not line: break

            dumpTriple = line.split()
            if len(dumpTriple) == 3:
                if self.tripleS == dumpTriple[0]:
                    if self.tripleP + "Depth" == dumpTriple[1]:
                        if dumpTriple[2][0].isalpha():

                           #print(int(dumpTriple[2].lstrip(str(p.findall(dumpTriple[2]))))-1)
                           #print(''.join(p.findall(dumpTriple[2])))
                           objectDepthValue= ''.join(p.findall(dumpTriple[2])) + str(int(dumpTriple[2].lstrip(str(p.findall(dumpTriple[2]))))-1)
                           subjectDepthValue = dumpTriple[2]
                        else:
                            objectDepthValue = str(int(dumpTriple[2]) - 1)
                            subjectDepthValue = dumpTriple[2]

                        skipS =1
                        break

                if self.tripleO == dumpTriple[0]:
                    if self.tripleP + "Depth" == dumpTriple[1]:
                        if dumpTriple[2][0].isalpha():

                           #print(int(dumpTriple[2].lstrip(str(p.findall(dumpTriple[2]))))-1)
                           #print(''.join(p.findall(dumpTriple[2])))
                           subjectDepthValue= ''.join(p.findall(dumpTriple[2])) + str(int(dumpTriple[2].lstrip(str(p.findall(dumpTriple[2]))))+1)
                           objectDepthValue = dumpTriple[2]
                        else:
                           subjectDepthValue = str(int(dumpTriple[2]) + 1)
                           objectDepthValue = dumpTriple[2]



                        skipO = 1
                        break

        f.close()






        definedData = triple[0] + " " + triple[1] + " " + triple[2] + "\n"
        subjectDepth = triple[0] + " " + triple[1] + "Depth " + str(subjectDepthValue)  + "\n"
        objectDepth = triple[2] + " " + triple[1] + "Depth " + str(objectDepthValue)  + "\n"


        print(subjectDepth + objectDepth + "relation defined")

        f2.write("".join(definedData))
        if skipS == 0:
            f2.write("".join(subjectDepth))
        if skipO ==0:
            f2.write("".join(objectDepth))

        self.accept()

    def onCancelButtonClicked(self):
        self.reject()

    def showModal(self):
        return super().exec_()