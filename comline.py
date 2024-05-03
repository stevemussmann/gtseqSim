import argparse
import os.path

class ComLine():
	'Class for implementing command line options'

	def __init__(self, args):
		parser = argparse.ArgumentParser()
		parser._action_groups.pop()
		required = parser.add_argument_group('Required arguments')
		optional = parser.add_argument_group('Optional arguments')
		required.add_argument("-g", "--genepop",
							dest='genepop',
							required=True,
							help="Specify a file in genepop format for input."
		)
		optional.add_argument("-m", "--miss",
							dest='miss',
							action='store_true',
							help="Turn on missing data simulation."
		)
		optional.add_argument("-n", "--inds",
							dest='inds',
							type=int,
							default=50,
							help="Specify the number of individual genotypes to simulate"
		)
		optional.add_argument("-o", "--outfile",
							dest='outfile',
							default="output.genepop.txt",
							help="Specify an output file name (default = output.genepop.txt)."
		)
		self.args = parser.parse_args()

		'''
		#check if input file ends with .xlsx
		if not self.args.infile.endswith(".xlsx"):
			print("ERROR: Input file " + self.args.infile + " does not end with .xlsx file extension.")
			print("Is this a valid excel file?")
			print("Exiting Program...")
			print("")
			raise SystemExit
		'''

		#check if files exist
		self.exists( self.args.genepop )

	def exists(self, filename):
		if( os.path.isfile(filename) != True ):
			print("")
			print(filename, "does not exist")
			print("Exiting program...")
			print("")
			raise SystemExit
