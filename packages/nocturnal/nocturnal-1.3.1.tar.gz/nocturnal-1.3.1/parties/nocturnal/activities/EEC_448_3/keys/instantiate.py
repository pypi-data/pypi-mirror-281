


'''
	from nocturnal.activities.EEC_448_3.keys.instantiate import instantiate_EEC_448_3_private_key
	from nocturnal.activities.EEC_448_3.keys.instantiate import instantiate_EEC_448_3_public_key
	
	public_key = instantiate_EEC_448_3_public_key ({
		"public_key_path": 
	})
	private_key = instantiate_EEC_448_3_private_key ({
		"private_key_path": 
	})
'''

from nocturnal.activities.FS.file.scan import scan_file

import nocturnal.activities.EEC_448_3.private_key.instance as instantiate_private_key
import nocturnal.activities.EEC_448_3.public_key.instance as instantiate_public_key
	
import json

def instantiate_EEC_448_3_public_key (packet):
	public_key_path = packet ["public_key_path"]
	public_key_content = scan_file ({
		"path": public_key_path
	})
	public_key = json.loads (public_key_content) ["nocturnal_EEC_448_3_public_key"]
	public_key_instance = instantiate_public_key.from_DER_hexadecimal_string (public_key)
	
	return public_key_instance
	
	
	
	
	
def instantiate_EEC_448_3_private_key (packet):
	private_key_path = packet ["private_key_path"]
	private_key_content = scan_file ({
		"path": private_key_path
	})
	private_key = json.loads (private_key_content) ["nocturnal_EEC_448_3_private_key"]
	
	private_key_instance = instantiate_private_key.from_DER_hexadecimal_string (private_key)
	
	return private_key_instance
	
#\