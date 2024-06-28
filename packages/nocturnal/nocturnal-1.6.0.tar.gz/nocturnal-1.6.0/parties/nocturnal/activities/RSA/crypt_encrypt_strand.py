
''''
	from nocturnal.activities.RSA.crypt_decrypt_strand import decrypt_RSA_strand
	encrypt_RSA_strand ({
		"RSA_public_key_hexadecimal_strand": "",
		"strand_bytes": b""
	});
"'''

#/
#
import rsa
#
#\

def encrypt_RSA_strand (packet):
	strand_bytes = packet ["strand_bytes"]
	
	RSA_public_key_hexadecimal_strand = packet ["RSA_public_key_hexadecimal_strand"]
	RSA_public_key = rsa.PublicKey.load_pkcs1 (
		bytes.fromhex (RSA_public_key_hexadecimal_strand.lower ()), 
		format = 'DER'
	)
	
	encrypted_strand_bytes = rsa.encrypt (
		strand_bytes, 
		RSA_public_key
	)
	
	return encrypted_strand_bytes