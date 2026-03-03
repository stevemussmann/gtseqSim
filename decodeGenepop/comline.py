import argparse
import os.path
#import distutils.util

class ComLine():
	'Class for implementing command line options'

	def __init__(self, args):
		parser = argparse.ArgumentParser()
		parser._action_groups.pop()
		required = parser.add_argument_group('required arguments')
		optional = parser.add_argument_group('optional arguments')

		required.add_argument("-f", "--infile",
							dest='infile',
							required=True,
							help="Specify input file"
		)
		optional.add_argument("-o", "--outfile",
							dest='outfile',
							default="default.txt",
							help="Specify output file name (default=default.txt)"
		)
		self.args = parser.parse_args()

		# check if files exist
		self.exists( self.args.infile )

	def exists(self, filename):
		if( os.path.isfile(filename) != True ):
			print("")
			print(filename, "does not exist")
			print("Exiting program...")
			print("")
			raise SystemExit
