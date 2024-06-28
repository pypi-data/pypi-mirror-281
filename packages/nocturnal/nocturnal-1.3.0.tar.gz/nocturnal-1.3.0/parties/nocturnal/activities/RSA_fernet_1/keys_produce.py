
'''
	from nocturnal.activities.RSA_fernet_1.keys_produce import produce_RSA_and_fernet_keys

	fernet_key = produce_RSA_and_fernet_keys ({
		"write_keys": "yes",
		"keys_path": ""
	});
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
#
from nocturnal.activities.fernet_1.key_produce import produce_fernet_1_key
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
import os
import json
#
#\

def produce_RSA_and_fernet_keys (packet):
	write_keys = packet ["write_keys"]

	RSA_keys = create_RSA_keys ({
		"key_size": 2048,
		"write_keys": "no"
	});
	RSA_public_key = RSA_keys ["RSA_public_key"];
	RSA_private_key = RSA_keys ["RSA_private_key"];
	
	fernet_1_key = produce_fernet_1_key ({
		"write_outputs": "no",
		"kind": "hex"
	})
	
	print ("fernet_1_key hexadecimal:", fernet_1_key)
	
	#fernet_1_key_binary = fernet_1_key.encode ('utf-8')
	fernet_1_key_binary = fernet_1_key.encode ()

	
	
	RSA_public_key_instance = rsa.PublicKey.load_pkcs1 (
		bytes.fromhex (RSA_public_key), 
		format = 'DER'
	)
	
	fernet_1_key_RSA = rsa.encrypt (
		fernet_1_key_binary, 
		RSA_public_key_instance
	).hex ()

	print ("fernet_1_key_RSA hex:", fernet_1_key_RSA)


	keys = {
		"fernet": fernet_1_key,
		"fernet.RSA": fernet_1_key_RSA,
		"RSA": {
			"public": RSA_public_key,
			"private": RSA_private_key
		}
	}
	
	#print ("keys:", keys)
	
	if (write_keys == "yes"):
		keys_path = packet ["keys_path"]
	
		with open (keys_path, 'w') as FP:
			os.chmod (keys_path, 0o777)
			FP.write (json.dumps (keys, indent = 4))
		
	return keys;