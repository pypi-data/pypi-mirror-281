

'''
	unicode_string = json.dumps ({
		"move": "send",
		"fields": {
			"to": {
				"format": "EEC_448_1",
				"address": "3043300506032b6571033a00e26960a83c45c0bb86e356cd727473e96682e76c6dd01c991a6ea0a394ecca27b467554d73e2a22b05425c1926a7a92befda5c1937d6876f00"
			},
			"amount": "40324789324873"
		}
	}, indent = 4)		
	unsigned_bytes = unicode_string.encode ("utf-8")

	from nocturnal.activities.EEC_448_3.sign import EEC_448_3_sign
	signed_bytes = EEC_448_3_sign (
		private_key_instance,
		unsigned_bytes = unsigned_bytes,
		format = "bytes"
	)
	
	signed_bytes_hexadecimal = signed ["signed bytes hexadecimal"]
'''

from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa

import nocturnal.activities.EEC_448_3.modulators.hexadecimal.from_byte_string as byte_string_to_hex

def EEC_448_3_sign (
	private_key_instance = None,
	unsigned_bytes = None,
	format = "bytes"
):
	signer = eddsa.new (private_key_instance, 'rfc8032')
	signed_bytes = signer.sign (unsigned_bytes)
	
	if (format == "bytes"):
		return signed_bytes
	
	if (format == "hexadecimal string"):
		return byte_string_to_hex.modulate (signed_bytes)
		
	raise Exception (f'The format "{ format }" was unaccounted for.')
