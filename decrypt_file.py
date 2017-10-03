#!/usr/bin/env python
import sys
from file_handler import FileHandler

if len(sys.argv) < 5 or sys.argv[1] == '-h':
    print('Usage:')
    print('... <password> <base64-iv> <algorithm:[AES128|AES256]> <compressed:[y|n]> /path/to/file')
    print('For the base64-iv you need to find the value of the cb-encryptioninfo header. It will '
          'have a semi-colon seperated string like: 1;190728;AES;256;kgAAAAAAwlXSWZGeLJlaWg==;;;')
    print('The 5th item is the base64 encoded "IV" value which is kgAAAAAAwlXSWZGeLJlaWg== in '
          'this case. You will need this to decrypt the file (it is different for each file).')
    exit()

password = sys.argv[1]  # Cloudberry client-side encryption password
base64iv = sys.argv[2]  # Base64 IV from 'cb-encryptioninfo' metadata header
algorithm = sys.argv[3].upper()  # AES128 or AES256
compressed = sys.argv[4].lower() == 'y'
file_to_decrypt = sys.argv[5]

encrypted_file = open(file_to_decrypt, 'rb')
encrypted_data = encrypted_file.read()
encrypted_file.close()

file_handler = FileHandler(algorithm=algorithm, password=password)
decrypted_data = file_handler.get_contents(path=file_to_decrypt, base64iv=base64iv, compressed=True,
                                           encrypted=True)

decrypted_file = open(file_to_decrypt, 'wb')
decrypted_file.write(decrypted_data)
decrypted_file.close()
