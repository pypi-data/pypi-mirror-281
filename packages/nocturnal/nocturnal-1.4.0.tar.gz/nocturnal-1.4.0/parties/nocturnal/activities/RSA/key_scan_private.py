

'''
	from nocturnal.activities.RSA.key_scan_private import scan_RSA_private_key
	RSA_private_key = scan_RSA_private_key ("");
'''

import json
import rsa

def scan_RSA_private_key (key_path):
	with open (key_path, mode = 'r') as FP:
		RSA_private_key_hexadecimal_strand = json.load (FP) ["RSA_private_key"]
		
		RSA_private_key = rsa.PrivateKey.load_pkcs1 (
			bytes.fromhex (RSA_private_key_hexadecimal_strand), 
			format = 'DER'
		)
		
		return RSA_private_key
		
	raise Exception (f"Could not read fernet key at { key_path }")
	
	
	

