import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt
import random
from socket import *
from threading import *

form_class = uic.loadUiType("student_client_ui.ui")[0]


class UiInputInformation(QMainWindow, form_class):
    def __init__(self, ip, port):
        super().__init__()
        # self.student_client_socket = None
        self.setupUi(self)
        self.stacked_widget.setCurrentIndex(0)
        self.student_client_socket = None
        self.initialize_socket(ip, port)
        self.listen_thread()
        self.student_id = ""
        self.student_pw = ""
        self.student_id_pw = ""

        # 조사(1페이지) 시작 버튼
        # self.btn_student_login.clicked.connect(self.move_next_page)
        self.btn_student_login.clicked.connect(self.login_progress)
        self.btn_select_learning.clicked.connect(self.move_next_page)
        self.btn_select_quiz.clicked.connect(self.move_next_page2)
        self.btn_select_consulting.clicked.connect(self.move_next_page3)
        self.btn_learning_main.clicked.connect(self.move_before_page2)


        # 조사(1페이지) 종료 버튼
        self.btn_student_exit.clicked.connect(quit)

    def initialize_socket(self, sock_ip, sock_port):
        '''
        TCP socket을 생성하고 server와 연결
        '''
        self.student_client_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = sock_ip
        remote_port = sock_port
        print("remote_ip = ", remote_ip)
        print("remote_port = ", remote_port)
        self.student_client_socket.connect((remote_ip, remote_port))

    # def move_next_page(self):
    def login_progress(self):
        self.student_id = "@sid@" + self.te_student_id.toPlainText()
        self.student_pw = "@spw@" + self.te_student_pw.toPlainText()
        self.student_id_pw = self.student_id + "/" + self.student_pw
        print("ID : ", self.student_id)
        print("PW : ", self.student_pw)
        # self.student_client_socket.send(self.student_id.encode())
        # self.student_client_socket.send(self.student_pw.encode())
        self.student_client_socket.send(self.student_id_pw.encode())

    def move_main_page(self, so):
        while True:
            current_page = self.stacked_widget.currentIndex()
            buf = so.recv(256)
            if not buf:
                break
            data = buf.decode('utf-8')
            print("data = ", data)
            if "@login_success@" in data:
                print("로그인 합니다.")
                self.stacked_widget.setCurrentIndex(current_page + 1)
            elif "@login_fail@" in data:
                QMessageBox.question(self, "Error", "로그인 정보가 올바르지 않습니다.", QMessageBox.Ok)


    # 임시로 버튼 누를 때 다음 페이지 넘어 가기
    def move_next_page(self):
        current_page = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(current_page + 1)

    def move_next_page2(self):
        current_page = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(current_page + 2)

    def move_next_page3(self):
        current_page = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(current_page + 3)

    # 임시로 버튼 누를 때 이전 페이지 넘어 가기
    def move_before_page(self):
        current_page = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(current_page - 1)

    def move_before_page2(self):
        current_page = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(current_page - 2)

    def listen_thread(self):
        '''
        데이터 수신 Thread를 생성하고 시작한다.
        '''

        # t1 = Thread(target=self.receive_nickname, args=(self.nickname_socket,))
        login_ok_thread = Thread(target=self.move_main_page, args=(self.student_client_socket,))
        # t2 = Thread(target=self.receive_message, args=(self.client_socket,))
        # t1.start()
        login_ok_thread.start()
        # print("t1 start")
        # t2.start()
        # print("t2 start")






#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ip = "localhost"
# # port = 50005
# port = 1307
# sock.connect((ip, port))


if __name__ == "__main__":
    # ip = "127.0.0.1"
    ip = "localhost"
    port = 1307
    app = QApplication(sys.argv)
    # myWindow = UiInputInformation()
    myWindow = UiInputInformation(ip, port)
    # myChatClient.show()
    myWindow.show()
    app.exec_()
