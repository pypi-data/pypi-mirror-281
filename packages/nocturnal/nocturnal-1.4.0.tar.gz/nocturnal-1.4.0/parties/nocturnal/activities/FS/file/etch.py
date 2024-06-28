

'''
	from nocturnal.activities.FS.file.etch import etch_file
	etch_file ({
		"path": "",
		"strand": "",
		"mode": "w"
	})
'''

import os

def etch_file (packet):
	path = packet ["path"]
	strand = packet ["strand"]
	
	if ("mode" in packet):
		mode = packet ["mode"]
	else:
		mode = "wb"

	#print ('etching', type (strand), strand)

	with open (path, mode) as FP:
		os.chmod (path, 0o777)
		FP.write (strand)
		return;
		
	raise Exception (f"File was not etched at path: '{ path }'.")