

'''
	from nocturnal.activities.RSA_fernet_1.key_scan import scan_keys
	keys = scan_keys ("");
'''

from cryptography.fernet import Fernet

import json

def scan_keys (key_path):
	with open (key_path, mode = 'rb') as FP:
		return json.loads (FP.read ())
		
		#fernet_key = bytes.fromhex (fernet_key_dict ["fernet_key"])
		#return Fernet (fernet_key)
		
	raise Exception (f"Could not read keys at { key_path }")