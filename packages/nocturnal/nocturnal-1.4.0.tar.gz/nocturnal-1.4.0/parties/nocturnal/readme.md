




******

Bravo!  You have received a Medical Diploma from   
the Orbital Convergence University International Air and Water Embassy of the Tangerine Planet.  

You are now officially certified to include this module in your practice.

******

![nocturnal](https://gitlab.com/status600/treasures/nocturnal.1/-/raw/business/Placidplace--club-7708117_1280.jpg)

# nocturnal

---

## description   
Make sure you use this inside a Docker container.    
It runs deletions.

---		
		
## obtain & build
```
pip install nocturnal
```


## fernet tar
Given a directory (in the CWD) named: "constant"   

This produces a key: fernet.key.JSON   
Then produces encrypt: constant.tar.fernet   
Then produces decrypt: constant.decrypted   

These procedures search for: fernet.key.JSON
```
nocturnal fernet_1_tar produce_key
nocturnal fernet_1_tar encrypt --dir "constant"
nocturnal fernet_1_tar decrypt --file "constant.tar.fernet"
```


## EEC_448_3 Keys (Edward's Elliptic Curve 448, variant 3)    
This produces a public and private key.   
Then the keys are read from files.   
Then a byte string is signed.   
Then the signed byte string is verified.  

```
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


seed = "5986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8"

private_key_path = str (normpath (join (variance_path, "EEC_448_3_private_key"))) + ".JSON"
public_key_path = str (normpath (join (variance_path, "EEC_448_3_public_key"))) + ".JSON"

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
	

signed_bytes = EEC_448_3_sign (
	private_key_instance,
	unsigned_bytes = json.dumps ({
		"move": "send",
		"fields": {
			"to": {
				"format": "EEC_448_1",
				"address": "3043300506032b6571033a00e26960a83c45c0bb86e356cd727473e96682e76c6dd01c991a6ea0a394ecca27b467554d73e2a22b05425c1926a7a92befda5c1937d6876f00"
			},
			"amount": "40324789324873"
		}
	}, indent = 4).encode ("utf-8"),
	format = "bytes"
)
verified = EEC_448_3_verify (
	public_key_instance,
	
	signed_bytes = signed_bytes,
	unsigned_bytes = unsigned_bytes
)

assert (verified == "yes"), verified

			
```

   