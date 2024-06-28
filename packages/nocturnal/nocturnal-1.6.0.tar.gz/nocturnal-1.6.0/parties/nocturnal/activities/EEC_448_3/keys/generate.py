

'''
	from nocturnal.activities.EEC_448_3.keys import generate_EEC_448_3_keys
	keys = generate_EEC_448_3_keys ({
		"seed": "",
		"paths": {
			"public": "",
			"private": "" 
		}
	})
'''

'''
	{
		"public": {
			"hexadecimal string": public_key_DER_hexadecimal_string,
		},
		"private": {
			"hexadecimal string": private_key_DER_hexadecimal_string
		}
	}
'''

import nocturnal.activities.EEC_448_3.private_key.creator as EEC_448_3_private_key_creator
import nocturnal.activities.EEC_448_3.public_key.creator as EEC_448_3_public_key_creator

from nocturnal.activities.FS.file.etch import etch_file

import json


def generate_EEC_448_3_keys (packet):
	seed = packet ["seed"]
	public_key_path = packet ["paths"] ["public_key"]
	private_key_path = packet ["paths"] ["private_key"]
	
	#/
	#
	#	create private key
	#
	private_key = EEC_448_3_private_key_creator.create (seed)
	private_key_instance = private_key ["instance"]
	private_key_DER_hexadecimal_string = private_key ["DER hexadecimal string"]
	#\
	
	#/
	#
	#	create public key
	#
	public_key = EEC_448_3_public_key_creator.create (
		private_key_instance
	)
	public_key_instance = public_key ["instance"]
	public_key_DER_hexadecimal_string = public_key ["DER hexadecimal string"]
	#\
	
	etch_file ({
		"path": public_key_path,
		"strand": json.dumps ({
			"nocturnal_EEC_448_3_public_key": public_key_DER_hexadecimal_string
		}, indent = 4),
		"mode": "w"
	})
	
	etch_file ({
		"path": private_key_path,
		"strand": json.dumps ({
			"nocturnal_EEC_448_3_private_key": private_key_DER_hexadecimal_string
		}, indent = 4),
		"mode": "w"
	})
	
	return {
		"public": {
			"hexadecimal string": public_key_DER_hexadecimal_string,
		},
		"private": {
			"hexadecimal string": private_key_DER_hexadecimal_string
		}
	}