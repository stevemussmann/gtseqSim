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

		required.add_argument("-g", "--genepop",
							dest='genepop',
							required=True,
							help="Specify input genepop file."
		)
		required.add_argument("-j", "--json",
							dest='json',
							required=True,
							help="Specify json dictionary of genepop allele encodings."
		)
		optional.add_argument("-o", "--outfile",
							dest='outfile',
							default="convertedData.csv",
							help="Specify output file name (default=convertedData.csv)"
		)
		self.args = parser.parse_args()

		# check if files exist
		self.exists( self.args.genepop )
		self.exists( self.args.json )

	def exists(self, filename):
		if( os.path.isfile(filename) != True ):
			print("")
			print(filename, "does not exist")
			print("Exiting program...")
			print("")
			raise SystemExit
