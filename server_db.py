from socket import *
from threading import *
import pymysql

class ServerDB:
    def __init__(self):
        self.receive_student_id_pw = ""
        self.receive_id_pw = ""
        self.receive_student_id = ""
        self.receive_student_pw = ""
        self.sql_result_row = ""
        self.sql_result = []
        self.sql_result_list = []
        self.login_accept_msg = ""
        # self.s_sock = socket(AF_INET, SOCK_STREAM)


        # 서버 DB 스레드
        # th_id_pw_db_check = Thread(target=self.recieve_id_pw_db_check)
        # th_id_pw_db_check.start()
        # 학생 클라이언트 스레드
        th_accept_student_sock = Thread(target=self.accept_student_sock)
        th_accept_student_sock.start()
        # 선생 클라이언트 스레드
        # th_accept_teacher_sock = Thread(target=self.accept_teacher_sock)
        # th_accept_teacher_sock.start()


    def accept_student_sock(self):
        while True:
            # student_socket = socket()
            student_socket = socket(AF_INET, SOCK_STREAM)
            student_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            student_socket.bind(("localhost", 1307))
            student_socket.listen()
            self.std_sock, self.std_addr = student_socket.accept()
            th_std = Thread(target=self.recieve_id_pw, args=(self.std_sock,))
            th_std.start()

    def recieve_id_pw(self, c_socket):
        self.receive_id_pw = c_socket.recv(1024).decode()
        print(self.receive_id_pw)
        # self.receive_id_pw가 학생 클라이언트 로그인 정보일 경우
        self.receive_student_id_pw = self.receive_id_pw.split("/")
        print("receive_student_id_pw = ", self.receive_student_id_pw)
        self.receive_student_id = (self.receive_student_id_pw[0])[5:]
        print("ID : ", self.receive_student_id)
        self.receive_student_pw = (self.receive_student_id_pw[1])[5:]
        print("PW : ", self.receive_student_pw)

        # DB 접속
        connection = pymysql.connect(
            host='10.10.20.121', port=3306, user='root', password='1234',
            db='EDUCATION', charset='utf8')
        # 커서 가져오기 (연결할 DB와 상화작용하기 위해서 cursor 객체 생성필요)
        cursor = connection.cursor()
        # SQL 문 만들기
        sql = 'SELECT * FROM MEMBER'
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
        self.std_sock.send(self.login_accept_msg.encode())

        # connection.close()

        # if sql_result_row[2] == self.receive_student_id:
        #     print("DB 내 학생 ID 있음. 로그인 절차 수행")
        #     if sql_result_row[3] == self.receive_student_pw:
        #         self.login_accept_msg = "@login_success@"
        #         print("DB 내 학생 PW 있음. 로그인 절차 수행")
        #         self.std_sock.send(self.login_accept_msg.encode())
        # else:
        #     self.login_accept_msg = "@login_fail@"
        #     print("DB 내 학생 PW 없음. 로그인 절차 수행 못함")
        #     self.std_sock.send(self.login_accept_msg.encode())


        # for row in self.sql_result_list:
        #     print(row)
        #     if row[2] == self.receive_student_id:
        #         print("DB 내 학생 ID 있음. 로그인 절차 수행")
        #         if row[3] == self.receive_student_pw:
        #             print("DB 내 학생 PW 있음. 로그인 절차 수행")

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
    # 심재정입니다. 커밋 확인용 주석입니다.
