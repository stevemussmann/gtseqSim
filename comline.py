import argparse
import os.path
import sys

from contextlib import redirect_stdout

class ComLine():
	'Class for implementing command line options'

	def __init__(self, args, logfile):
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
		optional.add_argument("-l", "--lambda",
							dest='lam',
							type=float,
							default=None,
							help="Specify lambda value for poisson sampling"
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
							default="output",
							help="Specify an output file name prefix (default = output)."
		)
		optional.add_argument("-p", "--progeny",
							dest='progeny',
							type=int,
							default=50,
							help="Specify the number of progeny per parental pair"
		)
		optional.add_argument("-r", "--grandma",
							dest='grandma',
							action='store_true',
							help="Write gRandma output (works for biallelic loci only)."
		)
		optional.add_argument("-s", "--sequoia",
							dest='sequoia',
							action='store_true',
							help="Write sequoia output (works for biallelic loci only)."
		)
		optional.add_argument("-S", "--secondary",
							dest='secondary',
							type=int,
							default=None,
							help="Specify the number of individual genotypes to simulate as part of a secondary population (based on allele frequencies from genepop file input in -g / --genepop option)."
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

		lfh = open(logfile, 'a')

		## DISABLE ALL FUNCTIONS RELATED TO GENEPOP2 FILE UNTIL THEY ARE IMPLEMENTED
		if self.args.genepop2:
			print("")
			print("ERROR:")
			print("All functions related to the second genepop file option (-G / --genepop2) are currently disabled.")
			print("These will eventually be implemented to help facilitate simulations related to hybridization.")
			print("Please rerun the program without the -G / --genepop2 option to continue.")
			print("Exiting program...")
			print("")
			with redirect_stdout(lfh):
				print("")
				print("ERROR:")
				print("All functions related to the second genepop file option (-G / --genepop2) are currently disabled.")
				print("These will eventually be implemented to help facilitate simulations related to hybridization.")
				print("Please rerun the program without the -G / --genepop2 option to continue.")
				print("Exiting program...")
				print("")
			raise SystemExit

		lfh.close()

		#check if files exist
		self.exists( self.args.genepop, logfile )
		if self.args.genepop2:
			self.exists( self.args.genepop2 )

		lfh = open(logfile, 'a')

		# check if integers are positive numbers
		if self.args.inds < 1:
			print("ERROR: the number of individuals to simulate (-n / --inds) must be > 0.")
			print("Exiting Program...")
			print("")
			with redirect_stdout(lfh):
				print("ERROR: the number of individuals to simulate (-n / --inds) must be > 0.")
				print("Exiting Program...")
				print("")
			raise SystemExit
		if self.args.progeny < 1:
			print("ERROR: the number of progeny to simulate (-p / --progeny) must be > 0.")
			print("Exiting Program...")
			print("")
			with redirect_stdout(lfh):
				print("ERROR: the number of progeny to simulate (-p / --progeny) must be > 0.")
				print("Exiting Program...")
				print("")
			raise SystemExit
		if self.args.gens < 0:
			print("ERROR: the number of generations to simulate (-f / --generations) cannot be negative.")
			print("Exiting Program...")
			print("")
			with redirect_stdout(lfh):
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
				with redirect_stdout(lfh):
					print("****************************************************************************************************")
					print("WARNING: both genepop files have the same name. If this was not intentional please check your input.")
					print("****************************************************************************************************")
					print("")
		lfh.close()

	def exists(self, filename, logfile):
		lfh = open(logfile, 'a')
		if( os.path.isfile(filename) != True ):
			print("")
			print(filename, "does not exist")
			print("Exiting program...")
			print("")
			with redirect_stdout(lfh):
				print("")
				print(filename, "does not exist")
				print("Exiting program...")
				print("")
			raise SystemExit
		lfh.close()
