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
        self.button_action()
        self.student_id = ""
        self.student_pw = ""
        self.student_id_pw = ""
        self.temp_one_word = ""
        self.one_word_dic = {}
        self.word_list = []
        # self.word_list_index = 0
        self.number = 0
        # self.word_list_len = len(self.word_list)
        self.score_all_list = []
        self.msgbodx_quiz_submit = None

    def button_action(self):
        # while True:
        # 로그인
        # 로그인 버튼
        self.btn_student_login.clicked.connect(self.login_progress)
        # self.btn_student_login.clicked.connect(self.move_next_page)
        # 로그인 - 종료 버튼
        self.btn_student_exit.clicked.connect(quit)

        # 메인 메뉴
        # 메인 => 영단어 학습 버튼
        self.btn_select_learning.clicked.connect(self.request_msg_learning_english_word)
        # 메인 => 퀴즈 메뉴 버튼
        self.btn_select_quiz.clicked.connect(self.request_msg_quiz_english_word)
        # 메인메뉴 => 상담하기 이동 버튼
        self.btn_select_consulting.clicked.connect(self.move_next_page3)
        # 메인 => 종료 버튼
        # self.btn_select_quiz.clicked.connect(self.move_quiz_page)
        # quit

        # 영단어 학습 - 이전 영단어 보기 단어 버튼
        self.btn_learning_before.clicked.connect(lambda: self.learning_english_word_before_next("before"))
        # 영단어 학습 - 다음 영단어 보기 단어 버튼
        self.btn_learning_next.clicked.connect(lambda: self.learning_english_word_before_next("next"))
        # 영단어 학습 => 퀴즈 메뉴 이동 버튼
        self.btn_goto_quiz.clicked.connect(self.request_msg_quiz_english_word)
        # self.btn_goto_quiz.clicked.connect(self.move_learning_english_to_quiz_page)
        # 영단어 학습 => 메인 메뉴 이동 버튼
        self.btn_learning_main.clicked.connect(self.move_main_page)

        # 퀴즈
        # 퀴즈 - 이전 영단어 보기 버튼
        self.btn_quiz_before.clicked.connect(lambda: self.quiz_english_word_before_next("before"))
        # 퀴즈 - 다음 영단어 보기 버튼
        self.btn_quiz_next.clicked.connect(lambda: self.quiz_english_word_before_next("before"))
        # 퀴즈 - 정답 확인 버튼
        self.btn_quiz_answer.clicked.connect(self.quiz_answer_check)
        # 퀴즈 - 제출(채점) 버튼    // 서버에 결과 전송 (DB에 CREATE SQL 사용)
        self.btn_quiz_submit.clicked.connect(self.quiz_english_word_submit)

        # 퀴즈 => 메인 메뉴 이동 버튼
        self.btn_quiz_main.clicked.connect(self.move_main_page)

        # 상담하기 => 메인 메뉴 이동 버튼
        self.btn_learning_main.clicked.connect(self.move_before_page2)

    # TCP socket을 생성하고 server와 연결
    # def initialize_socket(self, sock_ip, sock_port1, sock_port2):
    def initialize_socket(self, sock_ip, sock_port):
        self.student_client_socket = socket(AF_INET, SOCK_STREAM)
        # self.english_word_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = sock_ip
        remote_port = sock_port
        # print("remote_ip = ", remote_ip)
        # print("remote_port = ", remote_port)
        self.student_client_socket.connect((remote_ip, remote_port))
        # self.english_word_socket.connect((remote_ip, remote_port))

    # 데이터 수신 스레드를 생성하고 시작한다.
    def listen_thread(self):
        login_ok_thread = Thread(target=self.receive_data_process, args=(self.student_client_socket,))
        login_ok_thread.start()
        # receive_eng_word = Thread(target=self.learning_english_word, args=(self.english_word_socket,))
        # receive_eng_word.start()

    # 로그인 버튼 수행 - 서버에 ID/PW 송신
    # def move_next_page(self):
    def login_progress(self):
        self.student_id = "$sid$" + self.le_student_id.text()
        self.student_pw = "$spw$" + self.le_student_pw.text()
        self.student_id_pw = self.student_id + "/l/" + self.student_pw
        print("ID : ", self.student_id)
        print("PW : ", self.student_pw)
        self.student_client_socket.send(self.student_id_pw.encode())

    # 서버에 영단어 학습 DB 데이터 요청
    def request_msg_learning_english_word(self):
        while True:
            send_learn_eng_msg = "$learn_eng$"
            # send_learn_eng_msg = "@learn_eng@"
            self.student_client_socket.send(send_learn_eng_msg.encode())
            print("request_msg_learning_english_word 실행 확인")
            break

    # 서버에 영단어 퀴즈 DB 데이터 요청
    def request_msg_quiz_english_word(self):
        while True:
            # send_learn_eng_msg = "@quiz_eng@"
            send_learn_eng_msg = "$quiz_eng$"
            self.student_client_socket.send(send_learn_eng_msg.encode())
            print("request_msg_quiz_english_word 실행 확인")
            break

    # 서버로 수신 받은 데이터 수행 작업
    def receive_data_process(self, so):
        # current_page = self.stacked_widget.currentIndex()
        while True:
            buf = so.recv(1024)
            if not buf:
                break
            msg_data = buf.decode('utf-8')
            print("서버로부터 수신 받은 msg_data = ", msg_data)
            if "@login_success@" in msg_data:
                print("로그인 합니다.")
                self.stacked_widget.setCurrentIndex(1)
                # self.stacked_widget.setCurrentIndex(current_page + 1)
            elif "@login_fail@" in msg_data:
                QMessageBox.question(self, "Error", "로그인 정보가 올바르지 않습니다.", QMessageBox.Ok)
            # elif "@word@" in msg_data:
            elif "/lw/" in msg_data:
                # self.word += msg_data.split("@word@")
                # self.word.append(msg_data[6:])
                self.temp_one_word = msg_data.split("/lw/")
                print("수신 받은 영단어 쪼개기(영단어, 학습) : ", self.temp_one_word)
                self.word_list.append(self.temp_one_word)
                # self.word_list.append(self.one_word_dic)
                # print("영단어 학습 리스트(%d) : " % self.word_list_len, self.word_list)
                print("영단어 학습 리스트(%d) : " % len(self.word_list), self.word_list)
                # self.word_list_index = self.word_list.index(0)
                self.stacked_widget.setCurrentIndex(2)
                self.move_learning_english_word()
            elif "/qw/" in msg_data:
                # self.word += msg_data.split("@word@")
                # self.word.append(msg_data[6:])
                self.temp_one_word = msg_data.split("/qw/")
                print("수신 받은 영단어 쪼개기(영단어, 퀴즈) : ", self.temp_one_word)
                self.word_list.append(self.temp_one_word)
                # self.word_list.append(self.one_word_dic)
                print("영단어 퀴즈 리스트(%d) : " % len(self.word_list), self.word_list)
                # print("영단어 퀴즈 리스트(%d) : " % self.word_list_len, self.word_list)
                # self.word_list_index = self.word_list.index(0)
                self.number = 0
                self.stacked_widget.setCurrentIndex(3)
                self.move_quiz_word()

    # 메인 메뉴 => 퀴즈 메뉴로 이동 버튼(첫 화면)
    def move_quiz_word(self):
        self.number = 0
        self.lbl_quiz_word.setText(self.word_list[self.number][1])
        # self.quiz_answer_check()

    # 영단어 학습 - 영어 단어 라벨에 처음 출력(영단어 리스트 0번 요소 단어/뜻)
    # def learning_english_word(self, num):
    def move_learning_english_word(self):
        # self.lbl_learning_word.setText(self.word_list[self.word_list_index][1])
        # self.lbl_learning_word.setText(self.word_list[num][1])
        self.lbl_learning_word.setText(self.word_list[self.number][1])
        # self.lbl_learning_word.setText(self.word_list[0][1])
        # self.lbl_learning_meaning.setText(self.word_list[self.word_list_index][2])
        # self.lbl_learning_meaning.setText(self.word_list[num][2])
        self.lbl_learning_meaning.setText(self.word_list[self.number][2])
        # self.lbl_learning_meaning.setText(self.word_list[0][2])

    # 영단어 학습 - 다음 단어 버튼 리스트 내 영단어 뺑뺑이 돌리기
    # 영단어 리스트 0번 요소(단어/뜻) =>...=> 마지막 요소 => 0번요소 반복
    # def learning_english_word_next(self, num):
    # def learning_english_word_next(self, btn_word):
    def learning_english_word_before_next(self, btn_word):
        if "before" in btn_word:
            if self.number <= 0:
                self.number = len(self.word_list)
            self.number -= 1
        elif "next" in btn_word:
            self.number += 1
            if self.number == len(self.word_list):
                self.number = 0
        # self.number = 1
        # self.lbl_learning_word.setText(self.word_list[self.word_list_index+1][1])
        # self.lbl_learning_word.setText(self.word_list[num][1])
        self.lbl_learning_word.setText(self.word_list[self.number][1])
        # self.lbl_learning_word.setText(self.word_list[1][1])
        # self.lbl_learning_meaning.setText(self.word_list[self.word_list_index+1][2])
        # self.lbl_learning_meaning.setText(self.word_list[num][2])
        self.lbl_learning_meaning.setText(self.word_list[self.number][2])
        # self.lbl_learning_meaning.setText(self.word_list[1][2])

    # 영단어 학습 - 메인 메뉴로 이동 버튼
    def move_main_page(self):
        self.stacked_widget.setCurrentIndex(1)
        # for i in range(self.word_list_len):
        for i in range(len(self.word_list)):
            self.word_list.pop()
        print("move_main_page 내 영단어 리스트 초기화 : ", self.word_list)

    # 퀴즈 - 답 체크
    def quiz_answer_check(self):
        print("len(self.word_list) = ", len(self.word_list))
        if self.le_quiz_answer.text() in self.word_list[self.number][2]:
            print("정답!(" + self.word_list[self.number][2] + ")")
            self.lbl_quiz_answer.setText("정답!(" + self.word_list[self.number][2] + ")")
            score_one_temp = self.word_list[self.number][0] + "/si/" + self.word_list[self.number][1] \
                             + "/si/" + self.word_list[self.number][2] + "/si/" + "$answer$o$"
            print("정답 정보 : ", score_one_temp)
            self.score_all_list.append(score_one_temp)
            # score_one_list = [self.word_list[self.number][0], self.word_list[self.number][1],
            #                   self.word_list[self.number][2], "o"]
            # print("정답 정보 : ", score_one_list)
            # self.score_all_list.append(score_one_list)
            # 중복된 데이터 체크 -- 현재 미구현
            # if self.score_all_list[self.number][0] == self.word_list[self.number][0]:
            #     print("중복된 데이터 score_all_list 리스트에서 제거(pop)")
            #     self.score_all_list.pop(self.number)
            if len(self.score_all_list) > len(self.word_list):
                print("word_list 길이 보다 길 수 없음(pop)")
                self.score_all_list.pop(self.number)
        else:
            print("오답!(" + self.word_list[self.number][2] + ")")
            self.lbl_quiz_answer.setText("오답! (" + self.word_list[self.number][2] + ")")
            score_one_temp = self.word_list[self.number][0] + "/si/" + self.word_list[self.number][1] \
                             + "/si/" + self.word_list[self.number][2] + "/si/" + "$answer$x$"
            print("오답 정보 : ", score_one_temp)
            self.score_all_list.append(score_one_temp)
            # score_one_list = [self.word_list[self.number][0], self.word_list[self.number][1],
            #                   self.word_list[self.number][2], "x"]
            # print("오답 정보 : ", score_one_list)
            # self.score_all_list.append(score_one_list)
            # 중복된 데이터 체크 -- 현재 미구현
            # if self.score_all_list[self.number][0] == self.word_list[self.number][0]:
            #     print("중복된 데이터 score_all_list 리스트에서 제거(pop)")
            #     self.score_all_list.pop(self.number)
            if len(self.score_all_list) > len(self.word_list):
                print("word_list 길이 보다 길 수 없음(pop)")
                self.score_all_list.pop(self.number)
        print("점수 리스트(%d) : " % len(self.score_all_list), self.score_all_list)

    # 영단어 학습 => 퀴즈 메뉴 이동 버튼	// 아직 잘 안됨
    def move_learning_english_to_quiz_page(self):
        # self.stacked_widget.setCurrentIndex(3)
        # for i in range(self.word_list_len):
        for i in range(len(self.word_list)):
            self.word_list.pop()
        print("영어단어 리스트 초기화 : ", self.word_list)
        # # 서버에 영단어 학습 메시지 송신
        self.request_msg_quiz_english_word()
        print("영단어 학습 => 퀴즈 request_msg_quiz_english_word 실행 확인")
        # self.number = 0
        # self.lbl_quiz_word.setText(self.word_list[self.number][1])
        # # self.quiz_answer_check()
        # # if self.le_quiz_meaning.text() in self.word_list[self.number][2]:
        # #     print("정답!!!")
        # #     self.lbl_answer.setText("정답!!!" + self.word_list[self.number][2])
        # # else:
        # #     print("오답!!!")
        # #     self.lbl_answer.setText("오답!!!" + self.word_list[self.number][2])
        # # self.lbl_learning_meaning.setText(self.word_list[self.number][2])

    # def move_quiz_page(self):
    #     # self.stacked_widget.setCurrentIndex(3)
    #     # for i in range(self.word_list_len):
    #     # 서버에 영단어 학습 메시지 송신
    #     self.request_msg_quiz_english_word()
    #     self.number = 0
    #     self.lbl_quiz_word.setText(self.word_list[self.number][1])
    #     # self.quiz_answer_check()

    # 퀴즈 - 영단어 이전/다음 보기 버튼
    # def quiz_english_word_before(self):
    def quiz_english_word_before_next(self, btn_word):
        if "before" in btn_word:
            if self.number <= 0:
                self.number = len(self.word_list)
            self.number -= 1
        elif "next" in btn_word:
            self.number += 1
            if self.number == len(self.word_list):
                self.number = 0
        self.le_quiz_answer.setText("")
        self.lbl_quiz_answer.setText("")
        self.lbl_quiz_word.setText(self.word_list[self.number][1])

    def quiz_english_word_submit(self):
        print("quiz_english_word_submit 실행")
        print("서버에 보낼 점수 리스트(%d) : " % len(self.score_all_list), self.score_all_list)
        # 정답 정보: 299 / si / head / si / 머리$answer_o$
        # 점수 리스트(3): ['301/si/heart/si/마음/상징$answer_x$', '49/si/bear/si/곰$answer_o$', '299/si/head/si/머리$answer_o$']
        self.msgbodx_quiz_submit = QMessageBox.question(self, '채점 결과 제출', "제출하시겠습니까?",
                                                        QMessageBox.Yes | QMessageBox.No)
        if self.msgbodx_quiz_submit == QMessageBox.Yes:
            print('Yes clicked.')
            self.stacked_widget.setCurrentIndex(1)
            for send_quiz_eng_msg in self.score_all_list:
                print("type send_quiz_eng_msg = ", type(send_quiz_eng_msg))
                self.student_client_socket.send(send_quiz_eng_msg.encode())
                print("서버로 보낼 채점 데이터 : ", send_quiz_eng_msg)
        elif self.msgbodx_quiz_submit == QMessageBox.No:
            print('No clicked.')

        # DB 고쳐야 할 것들
        # 621 / si / sorry / si / 슬픈 / 유감의$answer_x$


        # self.number -= 1
        # if self.number == len(self.word_list):
        #     self.number = 0
        # self.lbl_quiz_word.setText(self.word_list[self.number][1])
        # self.quiz_answer_check()
        # self.lbl_quiz_word.setText(self.word_list[self.number][1])
        # self.te_quiz_meaning.setText(self.word_list[self.number][2])
        # if self.te_quiz_meaning.text() in self.word_list[self.number][2]:
        #     print("정답!!!")
        #     self.lbl_answer.setText(self.word_list[self.number][2])
        # else:
        #     print("오답!!!")

    # 퀴즈 - 영단어 다음 보기 버튼
    # def quiz_english_word_next(self):
    #     self.number += 1
    #     if self.number == len(self.word_list):
    #         self.number = 0
    #     self.lbl_quiz_word.setText(self.word_list[self.number][1])
    #     self.quiz_answer_check()
    #     # self.lbl_quiz_word.setText(self.word_list[self.number][1])
    #     # self.te_quiz_meaning.setText(self.word_list[self.number][2])
    #     # if self.te_quiz_meaning.text() in self.word_list[self.number][2]:
    #     #     print("정답!!!")
    #     #     self.lbl_answer.setText(self.word_list[self.number][2])
    #     # else:
    #     #     print("오답!!!")

    # def learning_english_word_before(self, num):
    # def learning_english_word_before(self):
    #     self.number -= 1
    #     if self.number == 0:
    #         self.number = 0
    #     # self.number = 1
    #     # self.lbl_learning_word.setText(self.word_list[self.word_list_index-1][1])
    #     # self.lbl_learning_word.setText(self.word_list[num][1])
    #     # self.lbl_learning_word.setText(self.word_list[self.number-1][1])
    #     self.lbl_learning_word.setText(self.word_list[0][1])
    #     # self.lbl_learning_meaning.setText(self.word_list[self.word_list_index-1][2])
    #     # self.lbl_learning_meaning.setText(self.word_list[num][2])
    #     # self.lbl_learning_meaning.setText(self.word_list[self.number-1][2])
    #     self.lbl_learning_meaning.setText(self.word_list[0][2])

    # 임시로 버튼 누를 때 다음 페이지 넘어 가기
    def move_next_page(self):
        current_page = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(current_page + 1)

    # def move_next_page2(self):
    #     current_page = self.stacked_widget.currentIndex()
    #     self.stacked_widget.setCurrentIndex(current_page + 2)

    def move_next_page3(self):
        current_page = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(current_page + 3)

    # 임시로 버튼 누를 때 이전 페이지 넘어 가기
    def move_before_page(self):
        self.stacked_widget.setCurrentIndex(1)

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
