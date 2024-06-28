

'''
	import nocturnal.activities.EEC_448_3.modulators.byte_string.from_UTF8 as UTF8_to_byte_string
	byte_string = UTF8_to_byte_string.modulate ("Hi there!")
'''


def modulate (UTF8_string):
	byte_string = UTF8_string.encode ("utf-8")

	assert (
		byte_string.decode ("utf-8") ==
		UTF8_string
	)

	return byte_string