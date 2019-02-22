# https://stackoverflow.com/questions/40059654/python-convert-a-bytes-array-into-json-format
# https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/

import json
import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class Message:

    public_key = None
    private_key = None

    def __init__(self):
        self.iKeys()
        # self.iOpen()
        print(self.public_key)
        print(self.private_key)
        pass

    def iKeys(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

        pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        with open('private_key.pem', 'wb') as f:
            f.write(pem)

        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open('public_key.pem', 'wb') as f:
            f.write(pem)

    def iOpen(self):
        with open("private_key.pem", "rb") as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        with open("public_key.pem", "rb") as key_file:
            self.public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )

    def iEncript(self, message, encode_ = True):
        # message = b'encrypt me!'
        if encode_:
            message = message.encode()

        encrypted = self.public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted

    def iDecrypt(self, encrypted, decode_ = True):
        original_message = self.private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        if decode_:
            original_message = original_message.decode()

        return original_message

    def convert(self, data, action = 'byte_to_json', unicode = 'utf-8'):
        if action == "byte_to_json":
            json_ = data.decode('utf8').replace("'", '"')
            data_ = json.loads(json_)
            return json.dumps(data_, indent=4, sort_keys=True)
        elif action == "json_to_byte":
            text = json.dumps(data)
            return bytes(text, unicode)
        pass

