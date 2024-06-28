

''''
	from nocturnal.activities.fernet_1.instance_to_hexadecimal import fernet_1_instance_to_hexadecimal
	fernet_1_hexadecimal = fernet_1_instance_to_hexadecimal ("")
"'''

from cryptography.fernet import Fernet

import binascii

def fernet_1_instance_to_hexadecimal (fernet_key):
	return binascii.hexlify (fernet_key).decode ()