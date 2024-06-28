
''''
	from nocturnal.activities.RSA.crypt_decrypt_strand import decrypt_RSA_strand
	decrypt_RSA_strand ({
		"RSA_private_key hex string": "",
		"encrypted_strand_bytes": b""
	});
"'''

#/
#
import rsa
#
#\

def decrypt_RSA_strand (packet):
	encrypted_strand_bytes = packet ["encrypted_strand_bytes"]

	RSA_private_key_hexadecimal_strand = packet ["RSA_private_key_hexadecimal_strand"]
	RSA_private_key = rsa.PrivateKey.load_pkcs1 (
		bytes.fromhex (RSA_private_key_hexadecimal_strand), 
		format = 'DER'
	)

	decrypted_strand_bytes = rsa.decrypt (
		encrypted_strand_bytes, 
		RSA_private_key
	)
	
	return decrypted_strand_bytes