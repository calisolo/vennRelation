import sys
import re
from PyQt5.QtWidgets import *


class findrule(QDialog):
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


        f = open("./dump/testSearch.txt", 'r')
        f2 = open("./dump/testAdded.txt", 'a')
        furtherList = ""
        tmpList = ""


        line = self.edit.text()
        relation = line.split()
        self.relationA= relation[0]
        self.relationDepth= relation[1]
        self.relationB= relation[2]
        depth = int(self.relationDepth)
        subjectDepth = ""
        objectDepth = ""
        middleDepthExist = ""
        subjectDepthExist = False
        objectDepthExist = False
        p = re.compile("[^0-9, -]")


        while True:
            line = f.readline()
            if not line: break

            triple = line.split()
            if len(triple) == 1:
                continue
            elif len(triple) == 2:
                if relation[0] == triple[0]:
                    furtherList = furtherList + triple[1] + "\n"
            elif len(triple) == 3:
                if relation[0] == triple[0]:
                    if "Depth" == triple[1][-5:]:
                        subjectDepth = triple[2]
                        subjectDepthExist = True

                if relation[2] == triple[0]:
                    if "Depth" == triple[1][-5:]:
                        objectDepth = triple[2]
                        objectDepthExist = True

        f.close()

        #depth가 존재할경우
            # referenceEntity 존재
            # referenceEntity 존재하지않고 단순 일차원 숫자



        if subjectDepthExist and objectDepthExist:
            if subjectDepth[0].isalpha():
                if objectDepth[0].isalpha():
                   if ''.join(p.findall(subjectDepth)) == ''.join(p.findall(objectDepth)):
                       print("관계발견")


            else:
                if objectDepth[0].isalpha():
                    print("nothing")
                else:
                    if subjectDepth > objectDepth:
                        print(relation[2] + " 는 " + relation[0] + "에 포함됨")
                    elif subjectDepth < objectDepth:
                        print(relation[0] + " 는 " + relation[2] + "에 포함됨")




        while depth > 0:

            tmpList = furtherList
            furtherList = ""
            cnt = tmpList.count("\n")
            relationList = tmpList.split()
            i = 0

            while cnt > 0:
                self.relationA = relationList[i]
                print(self.relationA)

                f = open("./dump/testSearch.txt", 'r')

                while True:  #파일 오픈후 한바퀴
                    line = f.readline()
                    if not line: break

                    triple = line.split()
                    if len(triple) == 1:
                        continue
                    elif len(triple) == 2:
                        if self.relationA == triple[0]:
                            furtherList = furtherList + triple[1] + "\n" # 다음depth를 리스트에 합함
                            if self.relationB == triple[1]:
                               print("really find")




                cnt = cnt - 1
                i = i + 1
                f.close()

            depth = depth - 1

        #뎁스남아있는한루프
            #둘째단어리스트를쪼개서루프
            #둘째단어를첫단어로대체
                #파일다읽을때까지루프
                #한줄씩비교해서 첫단어 똑같은것 매칭
        self.accept()


    def onCancelButtonClicked(self):
        self.reject()

    def showModal(self):
        return super().exec_()