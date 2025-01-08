#!/usr/bin/env python3

from allelefreqs import Allelefreqs
from comline import ComLine
from genepop import Genepop
from reproduce import Reproduce
from simgenos import SimGenos

import datetime
import numpy
import pandas
import sys

def main():
	# get date time
	now = datetime.datetime.now()
	formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
	
	# open log file for writing
	logfile = "gtseqSim.log"
	fh = open(logfile, 'w')

	# print execution command to log
	fh.write("## Log file for run beginning at " + formatted_datetime + "\n\n")
	fh.write("## gtseqSim.py was executed with the following command:\n" + str(" ".join(sys.argv)) + "\n\n")
	input = ComLine(sys.argv[1:])

	## handle first (or only) genepop file
	gp = Genepop(input.args.genepop) # make new Genepop object
	pdf = gp.parse() # parse genepop file and return pandas dataframe

	# calculate allele frequencies for first (or only) genepop file 
	af = Allelefreqs(pdf) # make new allelefreqs object
	freqs = af.calcFreqs() # calculate allele frequencies

	# simulate genotypes for first (or only) genepop file
	sg = SimGenos(freqs) # make new SimGenos object
	simPdf = sg.simInds(input.args.inds) # simulate genotypes for the requested number of individuals


	## handle second (optional) genepop file
	if input.args.genepop2:
		# parse second (optional) genepop file
		gp2 = Genepop(input.args.genepop2) # make new Genepop object
		pdf2 = gp2.parse() # parse genepop file and return pandas dataframe

		# check if pdf2 contains same loci as pdf
		if not pdf.columns.equals(pdf2.columns):
			print("ERROR:", str(input.args.genepop2), "contains at least one locus not found in", str(input.args.genepop))
			print("Check your inputs to ensure both files contain the same set of loci.")
			print("")
			raise SystemExit
	
		# calculate allele frequencies
		af2 = Allelefreqs(pdf2) # make new allelefreqs object
		freqs2 = af2.calcFreqs() # calculate allele frequencies

		# simulate genotypes 
		sg2 = SimGenos(freqs2) # make new SimGenos object
		simPdf2 = sg2.simInds(input.args.inds) # simulate requested number of genotypes


	## simulate reproduction
	# optional cross genotypes within or among populations; simulate defined number of generations
	if input.args.genepop2:
		repro = Reproduce(simPdf, simPdf2)
	else:
		repro = Reproduce(simPdf)
		repro.repro(input.args.progeny)

	# optional missing data simulation
	if input.args.miss == True:
		sg.simMissing(simPdf)
	#print(simPdf)
		
	if input.args.genepop2:
		# optional missing data simulation
		if input.args.miss == True:
			sg2.simMissing(simPdf2)
		#print(simPdf2)

	# write outputs
	gp.write(simPdf, input.args.outfile) # write simulated genotypes to genepop file


	# close log file for writing
	fh.close()

main()

raise SystemExit
