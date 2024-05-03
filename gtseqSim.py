#!/usr/bin/env python3

from allelefreqs import Allelefreqs
from comline import ComLine
from genepop import Genepop
from simgenos import SimGenos

import numpy
import pandas
import sys

def main():
	input = ComLine(sys.argv[1:])

	gp = Genepop(input.args.genepop) # make new Genepop object
	pdf = gp.parse() # parse genepop file and return pandas dataframe

	af = Allelefreqs(pdf) # make new allelefreqs object
	freqs = af.calcFreqs() # calculate allele frequencies

	sg = SimGenos(freqs) # make new SimGenos object
	simPdf = sg.simInds(input.args.inds) # simulate genotypes for the requested number of individuals

	#print(simPdf)

	gp.write(simPdf, input.args.outfile) # write simulated genotypes to genepop file

main()

raise SystemExit
