

'''
	python3 status.proc.py "activities/RSA_fernet_1/_status/status_1.py"
'''


#/
#
from cryptography.fernet import Fernet
import rsa
#
#
from nocturnal.activities.RSA_fernet_1.keys_produce import produce_RSA_and_fernet_keys
from nocturnal.activities.RSA_fernet_1.keys_scan import scan_keys
from nocturnal.activities.RSA_fernet_1.crypt_encrypt import crypt_encrypt_RSA_fernet
from nocturnal.activities.RSA_fernet_1.crypt_decrypt import crypt_decrypt_RSA_fernet
#
from nocturnal.activities.FS.file.delete_abandon import delete_abandon_file	
from nocturnal.activities.FS.directory.delete_abandon import delete_abandon_directory
#
from nocturnal.activities.FS.file.scan import scan_file
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


def check_1 ():
	this_folder = pathlib.Path (__file__).parent.resolve ()
	original_strand_path = str (normpath (join (this_folder, "constants/strand.HTML")))
	keys_path = str (normpath (join (this_folder, "variance/keys.JSON")))
	strand_fernet = str (normpath (join (this_folder, "variance/strand.HTML.fernet")))
	decrypted_strand_path = str (normpath (join (this_folder, "variance/strand.HTML.fernet.decrypt")))

	print ('producing keys')

	keys = produce_RSA_and_fernet_keys ({
		"write_keys": "yes",
		"keys_path": keys_path
	});


	#print ("keys:", keys)
	fernet_key = keys ["fernet"]
	fernet_RSA_key = keys ["fernet.RSA"]
	RSA_public_key = keys ["RSA"] ["public"]
	RSA_private_key = keys ["RSA"] ["private"]

	crypt_encrypt_RSA_fernet ({
		"fernet_key hexadecimal": fernet_key,
		
		"original_path": original_strand_path,
		"encrypted_path": strand_fernet
	});

	fernet_key = crypt_decrypt_RSA_fernet ({
		"fernet.RSA hexadecimal": fernet_RSA_key,
		"RSA_private hexadecimal": RSA_private_key,

		"encrypted_path": strand_fernet,
		"decrypted_path": decrypted_strand_path
	});

	assert (
		scan_file ({ "path": original_strand_path }) ==
		scan_file ({ "path": decrypted_strand_path })
	)

	print ('equality ensured')



checks = {
	'check 1': check_1
}

