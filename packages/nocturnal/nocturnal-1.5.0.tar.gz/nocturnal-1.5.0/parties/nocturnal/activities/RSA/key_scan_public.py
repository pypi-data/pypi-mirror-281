

'''
	from nocturnal.activities.RSA.key_scan_public import scan_RSA_public_key
	RSA_public_key = scan_RSA_public_key ("");
'''

import json
import rsa

def scan_RSA_public_key (key_path):
	with open (key_path, mode = 'r') as FP:
		RSA_public_key_hexadecimal_strand = json.load (FP) ["RSA_public_key"]
		
		RSA_public_key = rsa.PublicKey.load_pkcs1 (
			bytes.fromhex (RSA_public_key_hexadecimal_strand), 
			format = 'DER'
		)
		
		return RSA_public_key
		
	raise Exception (f"Could not read fernet key at { key_path }")
	
	
	