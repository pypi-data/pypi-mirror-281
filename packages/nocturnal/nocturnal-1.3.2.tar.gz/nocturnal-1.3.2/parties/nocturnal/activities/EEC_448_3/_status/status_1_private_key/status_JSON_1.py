
'''
	python3 status.proc.py "activities/EEC_448_3/_status/status_1_private_key/status_JSON_1.py"
'''

from nocturnal.activities.EEC_448_3.sign import EEC_448_3_sign
from nocturnal.activities.EEC_448_3.verify import EEC_448_3_verify

from nocturnal.activities.EEC_448_3.keys.generate import generate_EEC_448_3_keys
from nocturnal.activities.EEC_448_3.keys.instantiate import instantiate_EEC_448_3_private_key
from nocturnal.activities.EEC_448_3.keys.instantiate import instantiate_EEC_448_3_public_key
	
	

import pathlib
from os.path import dirname, join, normpath
import os
import json

variance_path = str (normpath (
	join (pathlib.Path (__file__).parent.resolve (), "variance")
))

def erase (path):
	try:
		os.remove (path)
	except Exception as E:
		pass;

def check_1 ():
	seeds = [ 
		"4986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8",
		"5986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8",
		"000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",		
		"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
		"123412341234123412341234123412341234123412341234123412341234123412341234123412341234123412341234123412341234123412",
		"0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f",	
		"135791357913579135791357913579135791357913579135791357913579135791357913579135791357913579135791357913579135791357",	
		"2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef"	
	]
	
	private_key_path = str (normpath (join (variance_path, "EEC_448_3_private_key"))) + ".JSON"
	public_key_path = str (normpath (join (variance_path, "EEC_448_3_public_key"))) + ".JSON"
	
	for seed in seeds:	
		erase (private_key_path)
		erase (public_key_path)
		
		generate_EEC_448_3_keys ({
			"seed": seed,
			"paths": {
				"private_key": private_key_path,
				"public_key": public_key_path
			}
		})
		
		public_key_instance = instantiate_EEC_448_3_public_key ({
			"public_key_path": public_key_path
		})
		private_key_instance = instantiate_EEC_448_3_private_key ({
			"private_key_path": private_key_path
		})
		
		unsigned_bytes = json.dumps ({
			"move": "send",
			"fields": {
				"to": {
					"format": "EEC_448_1",
					"address": "3043300506032b6571033a00e26960a83c45c0bb86e356cd727473e96682e76c6dd01c991a6ea0a394ecca27b467554d73e2a22b05425c1926a7a92befda5c1937d6876f00"
				},
				"amount": "40324789324873"
			}
		}, indent = 4).encode ("utf-8")		
		
		signed_bytes = EEC_448_3_sign (
			private_key_instance,
			unsigned_bytes = unsigned_bytes,
			format = "bytes"
		)
		verified = EEC_448_3_verify (
			public_key_instance,
			
			signed_bytes = signed_bytes,
			unsigned_bytes = unsigned_bytes
		)
		
		assert (verified == "yes"), verified
		
		return;
	
		
		
			
		

		
checks = {
	"elliptic private key generation": check_1
}






#