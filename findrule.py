import sys
import re
import time
from PyQt5.QtWidgets import *


class findrule(QDialog):
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

        start = time.time()


        f = open("./dump/simplifiedEntity.txt", 'r')
        furtherList = ""
        tmpList = ""


        line = self.edit.text()
        relation = line.split()

        if len(relation) == 1:
            self.relationA= relation[0]
        elif len(relation) == 2:
            self.relationA = relation[0]
            self.relationDepth= relation[1]
        elif len(relation) == 3:
            self.relationA = relation[0]
            self.relationDepth = relation[1]
            self.relationB= relation[2]

        subjectDepth = ""
        objectDepth = ""
        subjectPredicate = "no allocated"
        objectPredicate ="didn't allocated"

        middleDepthExist = ""
        queryEducationType = False
        subjectDepthExist = False
        objectDepthExist = False
        p = re.compile("[^0-9, -]")
        result = ""
        finishloop = False
        depth = 0


        if relation[0] == '?' or relation[1] == '?' or relation[2] == '?':
            queryEducationType = True

            if relation[0] == '?':
                if len(relation) ==2:
                    print("object: "+ relation[1] + " searching")
                elif len(relation) ==3:
                    print(relation[1] +"<- predicate " + relation[2] +"<- object  subject searching...")

            elif relation[1] == '?':
                print(relation[0] +" <- subject       predicate & object searching..." )

            elif relation[2] == '?':
                print(relation[0] +" <- subject   " +relation[1] +" <- predicate    object searching...")



        while True:
            if queryEducationType ==False: break
            line = f.readline()
            if not line: break

            triple = line.split()
            if len(triple) == 1:
                continue


            if relation[0] == '?':

                if len(triple) ==2:
                    if relation[1] == triple[1]:
                        print(triple[0])


                elif len(triple) ==3:
                    if len(relation)==2:
                        if relation[1] ==triple[2]:
                            print(triple[0])


                    elif len(relation)==3:
                        if relation[1] == triple[1]  and relation[2] == triple[2]:
                            print(triple[0])


            # predicate를 찾는 상황은 가정하지않으므로 무조건 object찾는것임

            elif relation[1] == '?':

                if len(triple) == 2:
                    if relation[0] == triple[0]:
                        print(triple[1])

                elif len(triple) ==3:
                    if relation[0] == triple[0]:
                        print(triple[1] +" " + triple[2])


            elif relation[2] == '?':
                if len(triple) == 2:
                    continue

                elif len(triple) == 3:
                    if relation[0] == triple[0] and relation[1] == triple[1]:
                        print(triple[2])






        while True:
            if queryEducationType: break

            line = f.readline()
            if not line: break




            triple = line.split()
            if len(triple) == 1:
                continue
            elif len(triple) == 2:
                if relation[0] == triple[0]:
                    if relation[2] ==triple[1]:
                        print(relation[2]+ " is directly connected to  " + relation[0])

                        finishloop = True
                    else:
                        furtherList = furtherList + triple[1] + "\n"
            elif len(triple) == 3:
                if relation[0] == triple[0]:
                    if "Depth" == triple[1][-5:]:
                        subjectDepth = triple[2]
                        subjectPredicate = triple[1]
                        subjectDepthExist = True

                    elif relation[2] ==triple[2]:
                        print(relation[2] + " is connected to " + relation[0] + " through "+triple[1] )

                        finishloop = True

                    else:
                        furtherList = furtherList + triple[2] + "\n"

                if relation[2] == triple[0]:
                    if "Depth" == triple[1][-5:]:
                        objectDepth = triple[2]
                        objectPredicate = triple[1]
                        objectDepthExist = True
                    else:
                        furtherList = furtherList + triple[2] + "\n"


        f.close()

        #depth가 존재할경우
            # referenceEntity 존재
            # referenceEntity 존재하지않고 단순 일차원 숫자


        if subjectPredicate == objectPredicate:
          if subjectDepthExist and objectDepthExist:
            if subjectDepth[0].isalpha():
                if objectDepth[0].isalpha():
                   if ''.join(p.findall(subjectDepth)).rstrip('+,-') == ''.join(p.findall(objectDepth)).rstrip('+,-'): #depth의 reference값 동일
                     if int(subjectDepth.lstrip(str(p.findall(subjectDepth)))) > int(objectDepth.lstrip(str(p.findall(objectDepth)))):
                         f = open("./dump/simplifiedEntity.txt", 'r')

                         while True:
                             line = f.readline()
                             if not line: break

                             triple = line.split()
                             if len(triple) == 3:
                                 if triple[1] == subjectPredicate:
                                     if triple[2][0].isalpha():
                                         if int(triple[2].lstrip(str(p.findall(triple[2])))) > int(subjectDepth.lstrip(str(p.findall(subjectDepth)))):
                                             continue
                                         elif int(triple[2].lstrip(str(p.findall(triple[2])))) < int(objectDepth.lstrip(str(p.findall(objectDepth)))):
                                             continue

                                         result = result + triple[0] + " " + triple[2] + "\n"
                                     else:
                                         continue

                         f.close()


                         print (relation[2] +" is included to " + relation[0])

                         finishloop = True

                     elif int(subjectDepth.lstrip(str(p.findall(subjectDepth)))) < int(objectDepth.lstrip(str(p.findall(objectDepth)))):
                         f = open("./dump/simplifiedEntity.txt", 'r')

                         while True:
                             line = f.readline()
                             if not line: break

                             triple = line.split()
                             if len(triple) == 3:
                                 if triple[1] == subjectPredicate:
                                     if triple[2][0].isalpha():
                                         if int(triple[2].lstrip(str(p.findall(triple[2])))) < int(subjectDepth.lstrip(str(p.findall(subjectDepth)))):
                                             continue
                                         elif int(triple[2].lstrip(str(p.findall(triple[2])))) > int(objectDepth.lstrip(str(p.findall(objectDepth)))):
                                             continue

                                         result = result + triple[0] + " " + triple[2] + "\n"
                                     else:
                                         continue

                         f.close()


                         print (relation[0] +" is included to " + relation[2] )
                         print (result)

                         finishloop = True




            else:
                if objectDepth[0].isalpha():
                    print("no identical [predicate Depth] exist")
                else:
                    if subjectDepth > objectDepth:


                        f = open("./dump/simplifiedEntity.txt", 'r')

                        while True:
                            line = f.readline()
                            if not line: break


                            triple = line.split()
                            if len(triple) == 3:
                                if triple[1] == subjectPredicate:
                                    if triple[2][0].isalpha():
                                        continue
                                    else:
                                        if triple[2] > subjectDepth:
                                            continue
                                        elif triple[2] < objectDepth:
                                            continue

                                        result = result + triple[0] + " " + triple[2] +"\n"

                        f.close()

                        print(relation[2] + " is included to  " + relation[0] )
                        print(result)
                        finishloop= True








                    elif subjectDepth < objectDepth:


                        f = open("./dump/simplifiedEntity.txt", 'r')

                        while True:
                            line = f.readline()
                            if not line: break

                            triple = line.split()
                            if len(triple) == 3:
                                if triple[1] == objectPredicate:
                                    if triple[2][0].isalpha():
                                        continue
                                    else:
                                        if triple[2] > objectDepth:
                                            continue
                                        elif triple[2] < subjectDepth:
                                            continue

                                        result = result + triple[0] + " " + triple[2] + "\n"

                        f.close()
                        print(relation[0] + " is included to  " + relation[2])
                        print(result)



        if queryEducationType== False:
            depth = int(self.relationDepth)

        totalDepth = depth

        while depth > 0:

            tmpList = furtherList
            furtherList = ""
            cnt = tmpList.count("\n")
            relationList = tmpList.split()
            i = 0

            if finishloop:
                break


            currentDepth = totalDepth - depth + 1

            print("depth "+ str(currentDepth) +" searching... \n")





            while cnt > 0:
                self.relationA = relationList[i]

                if finishloop:
                    break


                print("using subject : "+ self.relationA)

                f = open("./dump/simplifiedEntity.txt", 'r')

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
                               finishloop = True
                               print("Found the relation!")
                               print("Previous path: "+ triple[0] + "  Found: "+ triple[1])
                               break
                    elif len(triple) ==3:
                        if self.relationA ==triple[0]:
                            furtherList = furtherList + triple[2] + "\n"
                            if self.relationB == triple[2]:
                                finishloop = True
                                print("Found the relation!")
                                print("Previous path: "+ triple[0] + "  Found: " + triple[2] )
                                break





                cnt = cnt - 1
                i = i + 1
                f.close()

            depth = depth - 1


        #뎁스남아있는한루프
            #둘째단어리스트를쪼개서루프
            #둘째단어를첫단어로대체
                #파일다읽을때까지루프
                #한줄씩비교해서 첫단어 똑같은것 매칭
        print("Program finished")
        print("time : ", time.time() - start)

        self.accept()


    def onCancelButtonClicked(self):
        self.reject()

    def showModal(self):
        return super().exec_()