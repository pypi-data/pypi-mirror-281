
''''
	from nocturnal.activities.RSA_fernet_1.crypt_decrypt import crypt_decrypt_RSA_fernet
	fernet_key = crypt_decrypt_RSA_fernet ({
		"fernet.RSA hexadecimal": "",
		"RSA_private hexadecimal": "",

		"encrypted_path": "",
		"decrypted_path": ""
	});
"'''

''''
	moves:
		load the private key
		
		decrypt the fernet key
"'''

#/
#
from nocturnal.activities.FS.file.scan import scan_file
from nocturnal.activities.FS.file.etch import etch_file
#
#
from nocturnal.activities.fernet_1.instance_from_hexadecimal import fernet_1_instance_from_hexadecimal
#
#
from cryptography.fernet import Fernet
import rsa
#
#\


def crypt_decrypt_RSA_fernet (packet):
	fernet_RSA_hex = packet ["fernet.RSA hexadecimal"]
	RSA_private_hex = packet ["RSA_private hexadecimal"]
	encrypted_path = packet ["encrypted_path"]
	decrypted_path = packet ["decrypted_path"]
	
	RSA_private_key = rsa.PrivateKey.load_pkcs1 (
		bytes.fromhex (RSA_private_hex), 
		format = 'DER'
	)
	
	fernet_1_key_RSA_binary_string = bytes.fromhex (fernet_RSA_hex)
	
	print ("fernet RSA bytes:", fernet_1_key_RSA_binary_string)

	fernet_1_key_RSA_binary_string = rsa.decrypt (
		fernet_1_key_RSA_binary_string, 
		RSA_private_key
	)
	print ("fernet_1_key_RSA_binary_string:", fernet_1_key_RSA_binary_string)

	fernet_1_key_RSA_hexadecimal_string = fernet_1_key_RSA_binary_string.decode ()
	print ("fernet_1_key_RSA_hexadecimal_string:", fernet_1_key_RSA_hexadecimal_string)

	fernet_1_instance = fernet_1_instance_from_hexadecimal (fernet_1_key_RSA_hexadecimal_string)
	
	#decrypted_fernet_key = Fernet (decrypted_fernet_key_binary)
	print ("fernet_1_instance:", fernet_1_instance)
	
	
	encrypted_strand_bytes = scan_file ({
		"path": encrypted_path
	})
	
	
	decrypted_strand_bytes = fernet_1_instance.decrypt (encrypted_strand_bytes)
	
	# Fernet (bytes.fromhex (fernet_key_hex))
	
	
	
	print ("encrypted_strand_bytes:", encrypted_strand_bytes)
	print ("decrypted_strand_bytes:", decrypted_strand_bytes)

	
	
	etch_file ({
		"path": decrypted_path,
		"strand": decrypted_strand_bytes
	})
	
	return decrypted_strand_bytes