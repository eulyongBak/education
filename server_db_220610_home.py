from random import random
from socket import *
from threading import *
import pymysql
import random
import time

class ServerDB:
    def __init__(self):
        # 변수 초깃값 설정
        self.msg_sock = None
        self.std_addr = None
        # self.connection = None
        # self.cursor = None
        self.receive_msg = ""
        self.receive_student_id_pw = ""
        self.receive_id_pw = ""
        self.receive_student_id = ""
        self.receive_student_pw = ""
        self.receive_teacher_id_pw = ""
        self.receive_teacher_id = ""
        self.receive_teacher_pw = ""
        self.sql_result_row = ""
        self.login_accept_msg = ""
        self.sql_result = []
        self.sql_result_list = []

        # self.s_sock = socket(AF_INET, SOCK_STREAM)


        # 서버 DB 스레드
        # th_id_pw_db_check = Thread(target=self.recieve_id_pw_db_check)
        # th_id_pw_db_check.start()
        # 클라이언트 메시지 수신 소켓 스레드
        th_accept_student_sock = Thread(target=self.receive_msg_sock)
        th_accept_student_sock.start()

        # 단어 학습 스레드
        # th_learn_eng_word = Thread(target=self.accept_student_eng_sock)
        # th_learn_eng_word.start()

        # 선생 클라이언트 스레드
        # th_accept_teacher_sock = Thread(target=self.accept_teacher_sock)
        # th_accept_teacher_sock.start()

        # DB 접속
        # self.connection = pymysql.connect(
        #     host='10.10.20.121', port=3306, user='root', password='1234',
        #     db='EDUCATION', charset='utf8')
        # # 커서 가져오기 (연결할 DB와 상화작용하기 위해서 cursor 객체 생성필요)
        # self.cursor = self.connection.cursor()

    def receive_msg_sock(self):
        while True:
            # student_socket = socket()
            student_socket = socket(AF_INET, SOCK_STREAM)
            student_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            student_socket.bind(("localhost", 1307))
            student_socket.listen()
            self.msg_sock, self.std_addr = student_socket.accept()
            # th_std_id_pw = Thread(target=self.receive_id_pw_process, args=(self.msg_sock,))
            # th_std_id_pw.start()
            # th_learn_eng_word = Thread(target=self.send_english_word, args=(self.msg_sock,))
            # th_learn_eng_word.start()
            th_recv_msg_proc = Thread(target=self.receive_msg_process, args=(self.msg_sock,))
            th_recv_msg_proc.start()

    # def accept_student_eng_sock(self):
    #     student_eng_sock = socket()
    #     student_eng_sock.bind(("localhost", 1308))
    #     student_eng_sock.listen()
    #     self.eng_word_sock, self.eng_word_addr = student_eng_sock.accept()
    #     th_eng_word = Thread(target=self.send_english_word, args=(self.eng_word_sock,))
    #     th_eng_word.start()

    def receive_msg_process(self, c_socket):
        while True:
            self.receive_msg = c_socket.recv(1024).decode()
            print("클라이언트 수신 MSG :", self.receive_msg)
            if "@sid@" in self.receive_msg:
                self.receive_id_pw_process()
                # break
            elif "@tid@" in self.receive_id_pw:
                self.receive_id_pw_process()
                # break
            elif "@learn_eng@" in self.receive_msg:
                print("@learn_eng@ 메시지 받음")
                self.send_english_word()
                # break

    # def receive_id_pw_process(self, c_socket):
    def receive_id_pw_process(self):
        # self.receive_id_pw = c_socket.recv(1024).decode()
        # print("클라이언트 수신 MSG1 :", self.receive_id_pw)
        # self.receive_id_pw가 학생 클라이언트 로그인 정보일 경우
        # if "@sid@" in self.receive_id_pw:
        if "@sid@" in self.receive_msg:
            # self.receive_student_id_pw = self.receive_id_pw.split("/")
            self.receive_student_id_pw = self.receive_msg.split("/l/")
            print("클라이언트한테 수신 받은 ID/PW (리스트) : ", self.receive_student_id_pw)
            self.receive_student_id = (self.receive_student_id_pw[0])[5:]
            print("ID : ", self.receive_student_id)
            # self.receive_student_pw = (self.receive_student_id_pw[1])[5:]
            self.receive_student_pw = (self.receive_student_id_pw[1])[5:]
            print("PW : ", self.receive_student_pw)
        # 선생 클라이언트 로그인 시 ID/PW
        # elif "@tid@" in self.receive_id_pw:
        elif "@tid@" in self.receive_msg:
            self.receive_teacher_id_pw = self.receive_msg.split("/l/")
            print("클라이언트한테 수신 받은 ID/PW (리스트) : ", self.receive_teacher_id_pw)
            # self.receive_teacher_id = (self.receive_teacher_id_pw[0])[5:]
            self.receive_teacher_id = (self.receive_teacher_id_pw[0])[5:]
            print("ID : ", self.receive_teacher_id)
            # self.receive_teacher_pw = (self.receive_teacher_id_pw[1])[5:]
            self.receive_teacher_pw = (self.receive_teacher_id_pw[1])[5:]
            print("PW : ", self.receive_teacher_pw)
        # elif "@learn_eng@" in self.receive_id_pw:
        #     print("@learn_eng@ 메시지 받음")

        # DB 접속
        connection = pymysql.connect(
            # host='10.10.20.121', port=3306, user='root', password='1234',
            host='localhost', port=3306, user='root', password='1234',
            db='EDUCATION', charset='utf8')
        # 커서 가져오기 (연결할 DB와 상화작용하기 위해서 cursor 객체 생성필요)
        cursor = connection.cursor()
        # SQL 문 만들기
        sql = 'SELECT * FROM MEMBER'
        # self.cursor.execute(sql)  # sql문 실행
        cursor.execute(sql)  # sql문 실행
        # self.sql_result = cursor.fetchall()
        sql_result = cursor.fetchall()
        for sql_result_row in sql_result:
        # for sql_result_row in self.sql_result:
            print(sql_result_row)
            # self.sql_result_list.append(sql_result_row)
            if sql_result_row[2] == self.receive_student_id and \
                    sql_result_row[3] == self.receive_student_pw:
                self.login_accept_msg = "@login_success@"
                print("DB 내 학생 ID, PW 있음. 로그인 절차 수행")
                break
            else:
                self.login_accept_msg = "@login_fail@"
                print("DB 내 학생 ID, PW 없음. 로그인 할 수 없음.")
        print("self.login_accept_msg = ", self.login_accept_msg )
        self.msg_sock.send(self.login_accept_msg.encode())
        # self.connection.close()
        connection.close()
        # self.send_english_word()

    def send_english_word(self):
        # print("send_english_word 실행 확인")
        # self.receive_eng_word = c_socket.recv(1024).decode()
        # print("클라이언트 수신 MSG2 :", self.receive_id_pw)
        # self.receive_id_pw가 학생 클라이언트 로그인 정보일 경우
        # if "@sid@" in self.receive_msg:
        #     self.receive_student_id_pw = self.receive_msg.split("/")
        #     print("클라이언트한테 수신 받은 ID/PW (리스트) : ", self.receive_student_id_pw)
        #     self.receive_student_id = (self.receive_student_id_pw[0])[5:]
        #     print("ID : ", self.receive_student_id)
        #     self.receive_student_pw = (self.receive_student_id_pw[1])[5:]
        #     print("PW : ", self.receive_student_pw)
        # DB 접속
        connection = pymysql.connect(
            host='localhost', port=3306, user='root', password='1234',
            # host='10.10.20.121', port=3306, user='root', password='1234',
            db='EDUCATION', charset='utf8')
        # 커서 가져오기 (연결할 DB와 상화작용하기 위해서 cursor 객체 생성필요)
        cursor = connection.cursor()
        # SQL 문 만들기
        sql = 'SELECT * FROM ENGLISH'
        cursor.execute(sql)  # sql문 실행
        # self.cursor.execute(sql)  # sql문 실행
        # self.cursor.execute(sql)  # sql문 실행
        # self.sql_result = cursor.fetchall()
        sql_result = cursor.fetchall()
        # for sql_result_row in self.sql_result:
        # for sql_result_row in sql_result:
        #     print(sql_result_row)
        # print(type(sql_result))
        for i in range(3):
            random_eng_word = random.choice(sql_result)
            print("랜덤으로 뽑은 영단어 : ", random_eng_word)
            send_eng_word = str(random_eng_word[0]) + "/w/" + random_eng_word[1] + "/w/" + random_eng_word[2]
            # send_eng_word = "@word@"+str(random_eng_word[0]) + "/" + random_eng_word[1] + "/" + random_eng_word[2]
            print("학생 클라이언트로 보낼 영단어 : ", send_eng_word)
            time.sleep(0.5)
            self.msg_sock.send(send_eng_word.encode())
            # self.eng_word_sock.send(send_eng_word.encode())
        connection.close()
        # self.connection.close()


    # def recieve_id_pw_db_check(self):
    #     # 접속
    #     connection = pymysql.connect(
    #         host='10.10.20.121', port=3306, user='root', password='1234',
    #         db='EDUCATION', charset='utf8')
    #     # 커서 가져오기 (연결할 DB와 상화작용하기 위해서 cursor 객체 생성필요)
    #     cursor = connection.cursor()
    #     # SQL 문 만들기
    #     sql = 'SELECT * FROM MEMBER'
    #     cursor.execute(sql)  # sql문 실행
    #     self.sql_result = cursor.fetchall()
    #     for sql_result_row in self.sql_result:
    #         print(sql_result_row)
    #         self.sql_result_list.append(sql_result_row)
    #     # for self.sql_result_row in sql_result:
    #     #     print(self.sql_result_row)
    #     #     if self.sql_result_row[2] == self.receive_student_id:
    #     #         print("DB 내 학생 ID 있음. 로그인 절차 수행")
    #     #         if self.sql_result_row[3] == self.receive_student_pw:
    #     #             print("DB 내 학생 PW 있음. 로그인 절차 수행")
    #     connection.close()


    # def accept_teacher_sock(self):
    #     while True:
    #         sock = socket()
    #         sock.bind(('', self.port_list.pop()))
    #         sock.listen()
    #         c_sock, c_addr = sock.accept()
    #         th_msg = Thread(target=self.recieve_message, args=(c_sock,))
    #         th_msg.start()
    #         if len(self.port_list) == 0:
    #
    # def send_gui(self, final_received_message):
    #     self.gui_sock.send(final_received_message.encode())


if __name__ == "__main__":
    ServerDB()
