







'''
	from nocturnal.activities.fernet_1.key_produce import produce_fernet_1_key

	fernet_key = produce_fernet_1_key ({
		"write_outputs": "yes",
		"kind": "hex",
		
		"outputs": {
			"fernet_key_path": ""
		}
	});
'''

''''
	kind:
		instance
'''

''''
	@keys
		@enzymes
"'''

import rsa
import json

from cryptography.fernet import Fernet
from base64 import b64encode, b64decode

import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import os
from os.path import dirname
import binascii

def generate_fernet_key_01 ():
	password = "password".encode ()

	#
	#	maybe this is like a key from os.urandom (16) 
	#
	salt = b'salt_'

	kdf = PBKDF2HMAC (
		algorithm		=	hashes.SHA256 (),
		length			=	32,
		salt			=	salt,
		iterations		=	100000,
		backend			=	default_backend ()
	)

	key = base64.urlsafe_b64encode (kdf.derive (password)) 
	
	return key;
	
# option 2
def generate_fernet_key_02 (): 
	return Fernet.generate_key ()


def produce_fernet_1_key (packet):
	write_outputs = packet ["write_outputs"]
	
	if ("kind" in packet):
		kind = packet ["kind"]
	else:
		kind = "instance"

	#fernet_key = generate_fernet_key_01 ()
	fernet_key = generate_fernet_key_02 ()
	print ("fernet_key:", fernet_key)

	if (write_outputs == "yes"):
		outputs = packet ["outputs"]
	
		os.makedirs (dirname (outputs ["fernet_key_path"]), exist_ok = True)
		
		with open (outputs ["fernet_key_path"], 'w') as FP:
			os.chmod (outputs ["fernet_key_path"], 0o777)
			FP.write (json.dumps ({
				"fernet_key": fernet_key.hex ()
			}, indent = 4))
	
	if (kind == "hex"):
		hexadecimal = binascii.hexlify (fernet_key).decode ();
		fernet_key_decoded = binascii.unhexlify (hexadecimal)
	
		assert (
			fernet_key ==
			fernet_key_decoded
		), [
			fernet_key,
			fernet_key_decoded
		]
	
		#return fernet_key.hex ()
		return binascii.hexlify (fernet_key).decode ();
	
	return Fernet (fernet_key)