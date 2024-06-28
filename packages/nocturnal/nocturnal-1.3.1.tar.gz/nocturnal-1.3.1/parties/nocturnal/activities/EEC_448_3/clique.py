





import nocturnal.gadget.flask.start_dev as flask_start_dev

def clique ():
	import click
	@click.group ("EEC_448_3")
	def group ():
		pass


	import click
	@group.command ("generate")
	#@click.option ('--gadget-port', '-np', default = '43123')
	def generate ():		

		return;

	import click
	@group.command ("sign")
	#@click.option ('--gadget-port', '-np', default = '43123')
	def sign ():		

		return;
		
	import click
	@group.command ("verify")
	#@click.option ('--gadget-port', '-np', default = '43123')
	def verify ():		

		return;
		
	

	return group




#



