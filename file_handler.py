from base64 import b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from gzip import GzipFile
from io import BytesIO


class FileHandler:
    def __init__(self, algorithm='', password=''):
        self.algorithm = algorithm
        self.password = password

        if self.algorithm == 'AES128':
            self.key_size = 16
        elif self.algorithm == 'AES256':
            self.key_size = 32
        else:
            raise Exception('Unsupported algorithm specified')

    def get_contents(self, path='', base64iv='', compressed=False, encrypted=False):
        file = open(path, 'rb')
        contents = file.read()
        file.close()

        if encrypted:
            contents = self.decrypt(contents, base64iv=base64iv)
        if compressed:
            contents = self.decompress(contents)

        return contents

    def decrypt(self, encrypted_data, base64iv=''):
        iv = b64decode(base64iv)

        iterations = 1000
        salt = bytearray(8)
        derived_key = PBKDF2(self.password, salt, self.key_size, iterations)
        cipher = AES.new(derived_key, AES.MODE_CBC, iv)

        return self._unpad(cipher.decrypt(encrypted_data))

    @staticmethod
    def decompress(compressed_data):
        io_file = BytesIO(compressed_data)
        return GzipFile(fileobj=io_file).read()

    @staticmethod
    def _unpad(value):
        return value[:-ord(value[len(value) - 1:])]
