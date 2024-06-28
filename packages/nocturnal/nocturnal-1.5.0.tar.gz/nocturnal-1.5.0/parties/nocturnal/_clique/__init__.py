




from .group import clique as clique_group

import nocturnal.activities.fernet_1_tar.clique as fernet_1_tar_clique

def clique ():
	import click
	@click.group ()
	def group ():
		pass

	import click
	@click.command ("example")
	def example_command ():	
		print ("example")


	group.add_command (fernet_1_tar_clique.clique ())

	#group.add_command (example_command)
	#group.add_command (clique_group ())


	
	group ()




#
