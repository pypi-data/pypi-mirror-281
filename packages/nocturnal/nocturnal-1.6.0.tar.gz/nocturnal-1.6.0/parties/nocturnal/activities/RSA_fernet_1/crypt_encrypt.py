
''''
	from nocturnal.activities.RSA_fernet_1.crypt_encrypt import crypt_encrypt_RSA_fernet
	crypt_encrypt_RSA_fernet ({
		"fernet_key_hex": "",
		
		"original_path": "",
		"encrypted_path": ""
	});
"'''

import rsa

from cryptography.fernet import Fernet
from nocturnal.activities.FS.file.etch import etch_file
from nocturnal.activities.FS.file.scan import scan_file
	

def crypt_encrypt_RSA_fernet (packet):
	fernet_key_hex = packet ["fernet_key hexadecimal"]	
	fernet_key = Fernet (bytes.fromhex (fernet_key_hex))
	
	original_path = packet ["original_path"]
	encrypted_path = packet ["encrypted_path"]

	original_strand = scan_file ({
		"path": original_path
	})

	cipher_text = fernet_key.encrypt (original_strand)
	
	etch_file ({
		"path": encrypted_path,
		"strand": cipher_text
	})
	
	return cipher_text