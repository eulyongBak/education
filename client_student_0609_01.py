import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt
import random
from socket import *
from threading import *

form_class = uic.loadUiType("student_client_ui.ui")[0]


class UiInputInformation(QMainWindow, form_class):
    # class UiInputInformation(q_ip, u_port1, u_port2):
    def __init__(self, ip, port):
        super().__init__()
        # self.student_client_socket = None
        self.setupUi(self)
        self.stacked_widget.setCurrentIndex(0)
        self.student_client_socket = None
        # self.english_word_socket = None
        # self.initialize_socket(ip, port1, port2)
        self.initialize_socket(ip, port)
        self.listen_thread()
        self.student_id = ""
        self.student_pw = ""
        self.student_id_pw = ""
        self.word = []

        # 로그인 버튼
        self.btn_student_login.clicked.connect(self.login_progress)
        # self.btn_student_login.clicked.connect(self.move_next_page)
        # 영단어 학습 진입 버튼
        self.btn_select_learning.clicked.connect(self.learning_english_word)
        # 퀴즈 버튼
        self.btn_select_quiz.clicked.connect(self.move_next_page2)
        self.btn_select_consulting.clicked.connect(self.move_next_page3)
        self.btn_learning_before.clicked.connect(self.move_before_page)
        self.btn_learning_main.clicked.connect(self.move_before_page2)

        # 로그인 화면에서 종료 버튼
        self.btn_student_exit.clicked.connect(quit)

    # def initialize_socket(self, sock_ip, sock_port1, sock_port2):
    def initialize_socket(self, sock_ip, sock_port):
        '''
        TCP socket을 생성하고 server와 연결
        '''
        self.student_client_socket = socket(AF_INET, SOCK_STREAM)
        # self.english_word_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = sock_ip
        remote_port = sock_port
        # remote_port1 = sock_port1
        # remote_port2 = sock_port2
        # print("remote_ip = ", remote_ip)
        # print("remote_port = ", remote_port)
        # self.student_client_socket.connect((remote_ip, remote_port1))
        # self.english_word_socket.connect((remote_ip, remote_port2))
        self.student_client_socket.connect((remote_ip, remote_port))
        # self.english_word_socket.connect((remote_ip, remote_port))

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

    def receive_data_process(self, so):
        while True:
            current_page = self.stacked_widget.currentIndex()
            buf = so.recv(256)
            if not buf:
                break
            msg_data = buf.decode('utf-8')
            print("서버로부터 수신받은 msg_data = ", msg_data)
            if "@login_success@" in msg_data:
                print("로그인 합니다.")
                self.stacked_widget.setCurrentIndex(current_page + 1)
            elif "@login_fail@" in msg_data:
                QMessageBox.question(self, "Error", "로그인 정보가 올바르지 않습니다.", QMessageBox.Ok)
            elif "@word@" in msg_data:
                # self.word += msg_data.split("@word@")
                self.word.append(msg_data[6:])
                print("word : ", self.word)

    # def learning_english_word(self, so):
    def learning_english_word(self):
        str1 = "@learn_eng@"
        self.student_client_socket.send(str1.encode())

    def listen_thread(self):
        '''
        데이터 수신 Thread를 생성하고 시작한다.
        '''

        login_ok_thread = Thread(target=self.receive_data_process, args=(self.student_client_socket,))
        login_ok_thread.start()
        # receive_eng_word = Thread(target=self.learning_english_word, args=(self.english_word_socket,))
        # receive_eng_word.start()

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


if __name__ == "__main__":
    # ip = "127.0.0.1"
    ip = "localhost"
    port = 1307
    # port1 = 1307
    # port2 = 1308
    app = QApplication(sys.argv)
    # myWindow = UiInputInformation()
    # myWindow = UiInputInformation(ip, port1, port2)
    myWindow = UiInputInformation(ip, port)
    # myChatClient.show()
    myWindow.show()
    app.exec_()
