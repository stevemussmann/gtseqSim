#!/usr/bin/env python3

from allelefreqs import Allelefreqs
from comline import ComLine
from genepop import Genepop
from reproduce import Reproduce
from sequoia import Sequoia
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

	# get number padding length for assigning sample names
	pad = len(str((input.args.inds/2)*(input.args.progeny/2)))

	## handle first (or only) genepop file
	gp = Genepop(input.args.genepop) # make new Genepop object
	pdf = gp.parse() # parse genepop file and return pandas dataframe

	# calculate allele frequencies for first (or only) genepop file 
	af = Allelefreqs(pdf) # make new allelefreqs object
	freqs = af.calcFreqs() # calculate allele frequencies

	# simulate genotypes for first (or only) genepop file
	sg = SimGenos(freqs) # make new SimGenos object
	simPdf = sg.simInds(input.args.inds, input.args.prefix1, pad) # simulate genotypes for the requested number of individuals


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
		simPdf2 = sg2.simInds(input.args.inds, input.args.prefix2, pad) # simulate requested number of genotypes


	# list of pandas dataframes
	dfList = list() # list of pandas dataframes
	famList = list() # list of dicts of lists
	parList = list() # list of lists

	## simulate reproduction
	# optional cross genotypes within or among populations; simulate defined number of generations
	if input.args.genepop2:
		repro = Reproduce(simPdf, simPdf2)
	else:
		reproDF = simPdf
		for i in range(input.args.gens):
			repro = Reproduce(reproDF)
			prefix = "F" + str(i+1)
			reproDF, famDict, pList = repro.repro(input.args.progeny, prefix, pad)
			dfList.append(reproDF)
			famList.append(famDict)
			parList.append(pList)
	
	# optional missing data simulation
	if input.args.miss == True:
		sg.simMissing(simPdf)
	#print(simPdf)
		
	if input.args.genepop2:
		# optional missing data simulation
		if input.args.miss == True:
			sg2.simMissing(simPdf2)
		#print(simPdf2)

	## organize data for output
	# extract parents from among offspring
	parDFlist = list()

	parDFlist.append(simPdf)
	if input.args.genepop2:
		parDFlist.append(simPdf2)

	if len(parList)>1:
		for i in range(len(parList)):
			# lists with parents and offspring are offset by 1
			if i+1 < len(parList):
				newDF = dfList[i].loc[parList[i+1]] # extract the parents to new df
				dfList[i].drop(parList[i+1], inplace=True) # drop parents from original df
				parDFlist.append(newDF)# add to parental df list

	# do poisson subsampling
	#offDFlist = list()
	#if input.args.lam:
	#	for l in dfList:
	#		print(input.args.lam)

	## combine dataframes
	parDFlist.extend(dfList)
	combo = pandas.concat(parDFlist)

	## write outputs
	# write simulated f0 genotypes
	gp.write(combo, input.args.outfile) # write simulated genotypes to genepop file

	# write genotypes for all successive generations
	#for i in range(input.args.gens):
	#	prefix = "F" + str(i+1)
	#	fn = prefix + ".genepop.txt"
	#	gp.write(dfList[i], fn)
	
	# write sequoia output (only works for datasets with exclusively biallelic loci)
	if input.args.sequoia:
		#frames = list()
		#frames.append(simPdf)
		#for frame in dfList:
		#	frames.append(frame)
		#combo = pandas.concat(frames)
		print("Writing sequoia output file...")
		seq = Sequoia(combo, sg.mval) # sg.mval is missing data value returned from SimGenos object
		output = seq.convert()

		seqfh = open("output.sequoia.txt", 'w')
		for line in output:
			seqfh.write(line)
			seqfh.write("\n")


	# close log file for writing
	fh.close()

main()

raise SystemExit
