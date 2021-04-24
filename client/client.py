import socket
import json
import random, string
from random import randint
from hashlib import sha3_256
import hmac
import conf


HOST = conf.SERVER_IP
PORT = conf.SERVER_PORT
DEBUG_MODE = conf.DEBUG_MODE
CALL_NUMBER = conf.CALL_NUMBER
ENCODING = 'utf-8'




def generate_hmac(key, message, nonce):
        encoded_key = repr(key).encode(ENCODING)
        body = str(message) + nonce
        raw_body = body.encode(ENCODING)
        hashed = hmac.new(encoded_key, raw_body, sha3_256)
        return hashed.hexdigest()


class Client:

    # 256 bits random number
    key = 108079546209274483481442683641105470668825844172663843934775892731209928221929

    def __init__(self, host='127.0.0.1', port=55333):
        self.host = host
        self.port = port
    
    def send_request(self, request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            dumped_data = json.dumps(request)
            s.sendall(bytes(dumped_data, encoding="utf-8"))
            response = s.recv(1024)
            return response

    def send_money(self, account1, account2, money):
        print('Starting transaction')
        nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        message = {"account1": account1, "account2": account2, "money": money}
        hmac = generate_hmac(self.key, message, nonce)
        data = {"message": message, "nonce": nonce, "hmac": hmac}
        json_response = self.send_request(data)
        response = json.loads(json_response.decode('utf8'))
        print(str(response))
        print('Transaction complete')


if __name__ == "__main__":
    client = Client(HOST, PORT)
    max_call = CALL_NUMBER
    i = 0
    while i < max_call:
        i += 1
        account1 = ''.join(["{}".format(randint(0, 9)) for num in range(0, 6)])
        account2 = ''.join(["{}".format(randint(0, 9)) for num in range(0, 6)])
        money = str(randint(100, 999))
        client.send_money(account1, account2, money)

    #while True:
    #    pass



