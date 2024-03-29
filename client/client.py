import socket
import json
import random, string
from random import randint
from hashlib import sha3_256
import hmac
import conf
import ssl


HOST = conf.SERVER_IP
PORT = conf.SERVER_PORT
DEBUG_MODE = conf.DEBUG_MODE
CALL_NUMBER = conf.CALL_NUMBER
TRUSTED_CERT = conf.TRUSTED_CERT
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

    def __init__(self, host='127.0.0.1', port=55333, trusted_cert="./dummy_certs/certificate.pem"):
        self.host = host
        self.port = port
        self.trusted_cert = trusted_cert

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.load_verify_locations(trusted_cert)
    
    def send_request(self, request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            with self.context.wrap_socket(s, server_hostname="ST17") as sock:
                sock.connect((self.host, self.port))
                dumped_data = json.dumps(request)
                sock.sendall(bytes(dumped_data, encoding="utf-8"))
                response = sock.recv(1024)
                return response

    def auth(self, user, password, mensaje):
        print('Starting Auth')
        nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        message = {"user": user, "password": password, "message": mensaje}
        hmac = generate_hmac(self.key, message, nonce)
        data = {"message": message, "nonce": nonce, "hmac": hmac}
        json_response = self.send_request(data)
        response = json.loads(json_response.decode('utf8'))
        print(str(response))
        print('Auth complete')


if __name__ == "__main__":
    for i in range(0, CALL_NUMBER):
        try:
            cliente = Client(HOST, PORT, TRUSTED_CERT)
            cliente.auth("test","tes", "test")
        except:
            pass






