import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
connect_class = uic.loadUiType("teacherLogInPage.ui")[0]

#UI 규격 geometry: 800x600
#로그인 페이지 클래스
class logInPage(QMainWindow, connect_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.log_in_btn.clicked.connect(self.logInButtonMethod)
        self.exit_btn.clicked.connect(self.exitButtonMethod)

    def logInButtonMethod(self) :
        print("log in Clicked")

    def exitButtonMethod(self) :
        print("exit Clicked")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = logInPage()
    myWindow.show()
    app.exec_()