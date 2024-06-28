

'''
	{ verify, approve, validate, certify, vouch }
'''

'''
	from nocturnal.activities.EEC_448_3.verify import EEC_448_3_verify
	verified = EEC_448_3_verify (
		public_key_instance,
		
		signed_bytes = signed_bytes,
		unsigned_bytes = unsigned_bytes
	)
	assert (verified == "yes")
'''

from Crypto.Signature import eddsa
from Crypto.PublicKey import ECC

def EEC_448_3_verify (
	public_key_instance = None,
	
	unsigned_bytes = None,
	signed_bytes = None
):
	verifier = eddsa.new (public_key_instance, 'rfc8032')
	
	try:
		verifier.verify (unsigned_bytes, signed_bytes)		
		return "yes";
		
	except Exception as E:
		print ("exception:", E)
		
		#
		#	for example, "The signature is not authentic"
		#
	
		pass;
				
	return "no";