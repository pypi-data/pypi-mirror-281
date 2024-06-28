

'''
	from nocturnal.activities.RSA.key_create import create_RSA_key
	gains = create_RSA_key ({
		"key_size": 2048,
		
		"write_keys": "yes",
		"write_keys_to_paths": {
			"RSA_private_key": "",
			"RSA_public_key": 	""
		}
	});
'''

'''	
	#
	#	https://stuvel.eu/python-rsa-doc/usage.html#time-to-generate-a-key
	#
	#
	key_size: 
		4096 (24.4 seconds)
			512 - 11 = 501 byte limit per encrypt
		
		3072 (1.60 seconds)
		
		2048 (6.55 seconds)
			256 - 11 = 245 byte limit per encrypt
		
'''

'''
	@public
		@hot
	
	@private
		@cold
		@secret
		
	@inputs
		@from
		
	
	@outputs
		@to
'''

'''
	formats:
'''

#/
#
import rsa
#
#
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode
#
#
import os
from os.path import dirname
import json
#
#\

def write_RSA_private_key (
	RSA_private_key_path,
	RSA_private_key
):
	os.makedirs (dirname (RSA_private_key_path), exist_ok = True)
	with open (RSA_private_key_path, 'w', encoding='utf-8') as FP:
		json.dump ({
			"RSA_private_key": RSA_private_key
		}, FP, indent = 4)

		
def write_RSA_public_key (
	RSA_public_key_path,
	RSA_public_key
):
	os.makedirs (dirname (RSA_public_key_path), exist_ok = True)
	
	with open (RSA_public_key_path, 'w', encoding='utf-8') as FP:
		json.dump ({
			"RSA_public_key": RSA_public_key
		}, FP, indent = 4)


#
#	https://stuvel.eu/python-rsa-doc/reference.html#rsa.newkeys
#
#
def create_RSA_keys (packet):
	key_size = packet ["key_size"]
	
	write_keys = packet ["write_keys"]
	
	
	RSA_public_key, RSA_private_key = rsa.newkeys (key_size)
	
	RSA_public_key_hexadecimal_strand = rsa.PublicKey.save_pkcs1 (
		RSA_public_key, 
		format = 'DER'
	).hex ().upper ()
	
	RSA_private_key_hexadecimal_strand = rsa.PrivateKey.save_pkcs1 (
		RSA_private_key, 
		format = 'DER'
	).hex ().upper ()
	
	print ("RSA_public_key_hexadecimal_strand:", RSA_public_key_hexadecimal_strand)
	
	if (write_keys == "yes"):
		write_keys_to_paths = packet ["write_keys_to_paths"]
	
		write_RSA_public_key (
			write_keys_to_paths ["RSA_public_key"],
			RSA_public_key_hexadecimal_strand
		)
		write_RSA_private_key (
			write_keys_to_paths ["RSA_private_key"],
			RSA_private_key_hexadecimal_strand
		)

	return {
		"RSA_public_key": RSA_public_key_hexadecimal_strand,
		"RSA_private_key": RSA_private_key_hexadecimal_strand
	}
	

