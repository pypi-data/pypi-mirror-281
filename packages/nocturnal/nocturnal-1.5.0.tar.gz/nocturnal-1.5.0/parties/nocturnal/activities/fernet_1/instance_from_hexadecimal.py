

''''
	from nocturnal.activities.fernet_1.instance_from_hexadecimal import fernet_1_instance_from_hexadecimal
	fernet_1_instance = fernet_1_instance_from_hexadecimal ("")
"'''

from cryptography.fernet import Fernet

import binascii

def fernet_1_instance_from_hexadecimal (hexadecimal):
	return Fernet (binascii.unhexlify (hexadecimal))



