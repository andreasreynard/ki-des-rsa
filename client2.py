import socket
from threading import Thread
import index_key
import pka
from datetime import datetime
import secrets
import json

class Client:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect(('127.0.0.1', 2024))
        self.talk_to_server()

    def talk_to_server(self):
        self.socket.send('client2'.encode())
        Thread(target = self.receive_message).start()

    def receive_message(self):
        while True:
            result = json.loads(self.socket.recv(1024).decode())
            enc_message, enc_key2, nonce1 = result[0], result[1:-1], result[-1]
            private_key2, public_key1 = self.get_keys(0)
            enc_key1 = []
            for char in enc_key2:
                enc_key1.append(pka.better_pow(char, private_key2))
            cur_key = ''
            for char in enc_key1:
                cur_key += hex(pka.better_pow(char, public_key1))[2:]
            server_inbox = bytes.fromhex(index_key.decrypt(enc_message, index_key.key(cur_key))).decode('utf-8')
            print(f'Client2 received message: {server_inbox}, with Nonce1: {nonce1}')
            self.send_message(nonce1)

    def send_message(self, nonce1):
        while True:
            client_input = input('')
            cur_key = '111444ff77888555'
            enc_message = index_key.encrypt(client_input.encode('utf-8').hex(), index_key.key(cur_key))
            private_key2, public_key1 = self.get_keys(1)
            nonce = secrets.token_hex(16)
            enc_key1 = []
            for char in cur_key:
                enc_key1.append(pka.better_pow(int(char, 16), private_key2))
            encrypts = [enc_message]
            for char in enc_key1:
                encrypts.append(pka.better_pow(char, public_key1))
            encrypts.append(nonce1)
            encrypts.append(nonce)
            print(f"Client2 sent message encrypted with Client1's public key to Client1: [{nonce1} || {nonce}]")
            self.socket.send(json.dumps(encrypts).encode())

    def get_keys(self, requested):
        # Generate keys
        private_key2 = pka.gen_keys(2)[0]
        public_key1 = pka.gen_keys(1)[1]
        if requested == 0:
            # Client2 requests Client1's public key from the PKA
            request = "Get Client1's public key || Timestamp: " + datetime.now().isoformat()
            print(request)
            # Verify PKA's response
            print(f"Client1's public key verified from PKA: {pka.verified()} [{public_key1} || {request}]")
        return private_key2, public_key1

def final_step(encrypts):
    enc_nonce, enc_key2 = encrypts[0], encrypts[1:]
    private_key2, public_key1 = Client().get_keys(1)
    enc_key1 = []
    for char in enc_key2:
        enc_key1.append(pka.better_pow(char, private_key2))
    cur_key = ''
    for char in enc_key1:
        cur_key += hex(pka.better_pow(char, public_key1))[2:]
    final_nonce = index_key.decrypt(enc_nonce, index_key.key(cur_key))
    print(f'Client1, your partner Client2 verified Nonce2: {final_nonce}. Mutual authentication complete!')

if __name__ == '__main__':
    Client()
