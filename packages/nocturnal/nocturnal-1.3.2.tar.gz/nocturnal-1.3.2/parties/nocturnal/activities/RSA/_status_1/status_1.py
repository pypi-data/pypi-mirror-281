

'''
	python3 status.proc.py "activities/RSA/_status_1/status_1.py"
'''

#/
#
from cryptography.fernet import Fernet
import rsa
#
#
from nocturnal.activities.RSA.keys_create import create_RSA_keys
from nocturnal.activities.RSA.key_scan_public import scan_RSA_public_key
from nocturnal.activities.RSA.key_scan_private import scan_RSA_private_key
from nocturnal.activities.RSA.crypt_decrypt_strand import decrypt_RSA_strand
from nocturnal.activities.RSA.crypt_encrypt_strand import encrypt_RSA_strand
	
#
from nocturnal.activities.FS.file.delete_abandon import delete_abandon_file	
from nocturnal.activities.FS.directory.delete_abandon import delete_abandon_directory
#
#
import ships.paths.directory.check_equality as check_equality
#
#
from os.path import dirname, join, normpath
import pathlib
import sys
#
#\

this_folder = pathlib.Path (__file__).parent.resolve ()
RSA_private_key_path = str (normpath (join (this_folder, "variance/RSA.private_key.JSON")))
RSA_public_key_path = str (normpath (join (this_folder, "variance/RSA.public_key.JSON")))

def check_1 ():
	delete_abandon_file (RSA_private_key_path)
	delete_abandon_file (RSA_public_key_path)
	
	gains = create_RSA_keys ({
		"key_size": 2048,
		
		"write_keys": "yes",
		"write_keys_to_paths": {
			"RSA_private_key": RSA_private_key_path,
			"RSA_public_key": RSA_public_key_path
		}
	});

	RSA_public_key = scan_RSA_public_key (RSA_public_key_path);
	RSA_public_key_hexadecimal_strand = rsa.PublicKey.save_pkcs1 (
		RSA_public_key, 
		format = 'DER'
	).hex ().upper ()
	RSA_public_key_2 = rsa.PublicKey.load_pkcs1 (
		bytes.fromhex (RSA_public_key_hexadecimal_strand.lower ()), 
		format = 'DER'
	)
	RSA_public_key_hexadecimal_strand_2 = rsa.PublicKey.save_pkcs1 (
		RSA_public_key_2, 
		format = 'DER'
	).hex ().upper ()
	assert (
		RSA_public_key_hexadecimal_strand == 
		RSA_public_key_hexadecimal_strand_2
	), [
		RSA_public_key_hexadecimal_strand,
		RSA_public_key_hexadecimal_strand_2
	]
	
	RSA_private_key = scan_RSA_private_key (RSA_private_key_path);
	RSA_private_key_hexadecimal_strand = rsa.PrivateKey.save_pkcs1 (
		RSA_private_key, 
		format = 'DER'
	).hex ().upper ()
	RSA_private_key_2 = rsa.PrivateKey.load_pkcs1 (
		bytes.fromhex (RSA_private_key_hexadecimal_strand.lower ()), 
		format = 'DER'
	)
	RSA_private_key_hexadecimal_strand_2 = rsa.PrivateKey.save_pkcs1 (
		RSA_private_key_2, 
		format = 'DER'
	).hex ().upper ()
	assert (
		RSA_private_key_hexadecimal_strand == 
		RSA_private_key_hexadecimal_strand_2
	), [
		RSA_private_key_hexadecimal_strand,
		RSA_private_key_hexadecimal_strand_2
	]
	
	
	
	print ("RSA_public_key:", RSA_public_key)
	
	#/
	#	
	#	encrypt and decrypt
	#		RSA encrypts differently each time maybe..
	#
	strand_bytes = b'notes'
	encrypted_strand_bytes = encrypt_RSA_strand ({
		"RSA_public_key_hexadecimal_strand": RSA_public_key_hexadecimal_strand,
		"strand_bytes": strand_bytes
	});
	decrypted_strand_bytes = decrypt_RSA_strand ({
		"RSA_private_key_hexadecimal_strand": RSA_private_key_hexadecimal_strand,
		"encrypted_strand_bytes": encrypted_strand_bytes
	});
	#
	#\
	
	assert (strand_bytes == decrypted_strand_bytes), [
		strand_bytes,
		decrypted_strand_bytes
	]

	
checks = {
	'check 1': check_1
}