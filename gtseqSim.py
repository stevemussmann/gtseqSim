#!/usr/bin/env python3

from allelefreqs import Allelefreqs
from comline import ComLine
from colony import Colony
from genepop import Genepop
from grandma import gRandma
from reproduce import Reproduce
from sequoia import Sequoia
from simgenos import SimGenos
from subsample import Subsample

from contextlib import redirect_stdout

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
	fh.close()

	# get input command line options
	input = ComLine(sys.argv[1:], logfile)

	# get number padding length for assigning sample names
	maxInds = 0
	if input.args.inds2:
		maxInds = input.args.inds1 + input.args.inds2
	else:
		maxInds = input.args.inds1
	pad = len(str((maxInds/2)*(input.args.meanProgeny/2)))

	## handle first (or only) genepop file
	gp = Genepop(input.args.genepop, logfile) # make new Genepop object
	pdf = gp.parse() # parse genepop file and return pandas dataframe

	# calculate allele frequencies for first (or only) genepop file 
	af = Allelefreqs(pdf, logfile) # make new allelefreqs object
	freqs = af.calcFreqs() # calculate allele frequencies

	# simulate genotypes for first (or only) genepop file
	sg = SimGenos(freqs, logfile) # make new SimGenos object
	## NEED TO MODIFY SimGenos.simInds() FUNCTION TO CAPTURE AVERAGE MISSING DATA WHEN SECOND GENEPOP FILE IS INPUT
	simPdf = sg.simInds(input.args.inds1, input.args.prefix1, pad, input.args.sex1) # simulate genotypes for the requested number of individuals

	# simulate genotypes for secondary population
	if input.args.secondary:
		sgA = SimGenos(freqs, logfile)
		simPdfA = sgA.simInds(input.args.secondary, "secondary", pad, 0.5) # simulate genotypes for requested number of individuals in input.args.alt

	## handle second (optional) genepop file
	if input.args.genepop2:
		# parse second (optional) genepop file
		gp2 = Genepop(input.args.genepop2, logfile) # make new Genepop object
		pdf2 = gp2.parse() # parse genepop file and return pandas dataframe

		# check if pdf2 contains same loci as pdf
		if not pdf.columns.equals(pdf2.columns):
			print("ERROR:", str(input.args.genepop2), "contains at least one locus not found in", str(input.args.genepop))
			print("Check your inputs to ensure both files contain the same set of loci.")
			print("")
			raise SystemExit
	
		# calculate allele frequencies
		af2 = Allelefreqs(pdf2, logfile) # make new allelefreqs object
		freqs2 = af2.calcFreqs() # calculate allele frequencies

		# simulate genotypes 
		sg2 = SimGenos(freqs2, logfile) # make new SimGenos object
		simPdf2 = sg2.simInds(input.args.inds2, input.args.prefix2, pad, input.args.sex2) # simulate requested number of genotypes


	# list of pandas dataframes
	dfList = list() # list of pandas dataframes
	famList = list() # list of dicts of lists
	parList = list() # list of lists

	## simulate reproduction
	# optional cross genotypes within or among populations; simulate defined number of generations
	if input.args.genepop2:
		# if you only want to simulate hybrid crosses - option not implemented yet
		if input.args.hybrid == True:
			print("Hybrid option not fully implemented.")
			print("Only a genepop file of simulated parental genotypes will be printed.\n\n")
			repro = Reproduce(simPdf, logfile, simPdf2)
		# if you want to merge the two genepop files and do random mating - fixed at one generation currently
		else:
			reproDF = pandas.concat([simPdf, simPdf2], ignore_index=False) # combine genotypes simulated from two genepop files for random mating
			repro = Reproduce(reproDF, logfile)
			prefix = "F1"
			reproDF, famDict, pList = repro.repro(input.args.meanProgeny, input.args.sdProgeny, prefix, pad, input.args.polyandry, input.args.polygyny)
			dfList.append(reproDF)
			famList.append(famDict)
			parList.append(pList)
	else:
		reproDF = simPdf
		for i in range(input.args.gens):
			repro = Reproduce(reproDF, logfile)
			prefix = "F" + str(i+1)
			reproDF, famDict, pList = repro.repro(input.args.meanProgeny, input.args.sdProgeny, prefix, pad, input.args.polyandry, input.args.polygyny)
			dfList.append(reproDF)
			famList.append(famDict)
			parList.append(pList)
	
	## organize data for output
	# extract parents from among offspring
	parDFlist = list()

	parDFlist.append(simPdf)
	if input.args.secondary:
		parDFlist.append(simPdfA)
	if input.args.genepop2:
		parDFlist.append(simPdf2)

	if len(parList)>1:
		for i in range(len(parList)):
			# lists with parents and offspring are offset by 1
			if i+1 < len(parList):
				newDF = dfList[i].loc[parList[i+1]] # extract the parents to new df
				dfList[i].drop(parList[i+1], inplace=True) # drop parents from original df
				parDFlist.append(newDF)# add to parental df list

	# do offspring subsampling (if invoked) to prepare list of individuals for removal
	offDFlist = list()
	if input.args.lam:
		discardList = list() # list of offspring that were not retained by subsample function
		i = 1 # parent list is offset by +1 from the offspring lists
		for d in famList:
			sub = Subsample(input.args.lam)
			s = sub.poisson(d)
			if i < len(parList):
				l = parList[i]
				discard = sub.subsample(d, s, l)
			else:
				discard = sub.subsample(d, s)
			discardList.extend(discard)
			i+=1

	## combine dataframes
	parDFlist.extend(dfList)
	combo = pandas.concat(parDFlist)

	## remove individuals from combined dataframe (if offspring subsampling is invoked)
	if input.args.lam:
		combo.drop(discardList, inplace=True) 

	# optional missing data simulation
	if input.args.miss == True:
		combo = sg.simMissing(combo)
		
	## THE FOLLOWING BLOCK WILL PROBABLY BE DELETED IN FUTURE REVISION
	#if input.args.genepop2:
		# optional missing data simulation
		#if input.args.miss == True:
			#simPdf2 = sg2.simMissing(simPdf2)
		#print(simPdf2)

	## write outputs
	# write genotypes to genepop file
	print("Writing genepop output file...")
	gp.write(combo, input.args.outfile)

	# write genotypes for all successive generations
	#for i in range(input.args.gens):
	#	prefix = "F" + str(i+1)
	#	fn = prefix + ".genepop.txt"
	#	gp.write(dfList[i], fn)
	
	# write sequoia output (only works for datasets with exclusively biallelic loci)
	if input.args.sequoia:
		print("Writing sequoia output file...")
		seq = Sequoia(combo, sg.mval) # sg.mval is missing data value returned from SimGenos object
		output = seq.convert()

		seqF = input.args.outfile + ".sequoia.txt"
		seqfh = open(seqF, 'w')
		for line in output:
			seqfh.write(line)
			seqfh.write("\n")

	# write gRandma output
	if input.args.grandma:
		print("Writing gRandma output files...")
		gma = gRandma(combo, sg.mval)
		gmaOut = gma.convert()

		gmaF = input.args.outfile + ".grandma.txt"
		gmafh = open(gmaF, 'w')
		for line in gmaOut:
			gmafh.write(line)
			gmafh.write("\n")
	
	# write COLONY output
	if input.args.colony:
		print("Writing COLONY output file...")
		colony = Colony(combo, input.args.prefix1, input.args.prefix2)
		colOut = colony.convert()

		colF = "Colony2.Dat"
		colfh = open(colF, 'w')
		for line in colOut:
			colfh.write(line)
			colfh.write("\n")


main()

raise SystemExit
