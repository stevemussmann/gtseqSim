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
		optional.add_argument("-f", "--generations",
							dest='gens',
							type=int,
							default=2,
							help="Specify the number of generations to simulate"
		)
		optional.add_argument("-G", "--genepop2",
							dest='genepop2',
							help="Specify a second genepop file containing allele frequencies for a second population [optional]."
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
		optional.add_argument("-p", "--progeny",
							dest='progeny',
							type=int,
							default=50,
							help="Specify the number of progeny per parental pair"
		)
		optional.add_argument("-t", "--prefix1",
							dest='prefix1',
							default="taxon1",
							help="Specify the prefix to be used for naming individuals simulated from the data in your first genepop file (default = taxon1)."
		)
		optional.add_argument("-T", "--prefix2",
							dest='prefix2',
							default="taxon2",
							help="Specify the prefix to be used for naming individuals simulated from the data in your second genepop file (default = taxon2)."
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
		if self.args.genepop2:
			self.exists( self.args.genepop2 )

		# check if integers are positive numbers
		if self.args.inds < 1:
			print("ERROR: the number of individuals to simulate (-n / --inds) must be > 0.")
			print("Exiting Program...")
			print("")
			raise SystemExit
		if self.args.progeny < 1:
			print("ERROR: the number of progeny to simulate (-p / --progeny) must be > 0.")
			print("Exiting Program...")
			print("")
			raise SystemExit
		if self.args.gens < 0:
			print("ERROR: the number of generations to simulate (-f / --generations) cannot be negative.")
			print("Exiting Program...")
			print("")
			raise SystemExit

		# check if genepop and genepop2 are same file and print warning
		if self.args.genepop2:
			if self.args.genepop == self.args.genepop2:
				print("****************************************************************************************************")
				print("WARNING: both genepop files have the same name. If this was not intentional please check your input.")
				print("****************************************************************************************************")
				print("")

	def exists(self, filename):
		if( os.path.isfile(filename) != True ):
			print("")
			print(filename, "does not exist")
			print("Exiting program...")
			print("")
			raise SystemExit
