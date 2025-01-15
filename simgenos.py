import collections
import numpy
import pandas

class SimGenos():
	'Class for simulating individual genotypes from allele frequency data'

	def __init__(self, d):
		self.d = d
		self.miss = self.determineMissing()

	def determineMissing(self):
		missDict = dict() # dictionary to hold missing data proportions
		for (locus, key2) in self.d.items():
			remove = list() # list of dictionary keys to remove
			total = 0 # keep track of total allele count for calculating missing data proportion
			missing = 0 # keep track of number of missing alleles
			for (key, val) in key2.items():
				total = int(val) + total
				length = len(str(key)) # get length to construct missing data value
				miss = "0" * length # construct missing data value
				if str(key) == miss:
					remove.append(key) # add missing data value to list of secondary keys to be deleted from self.d
					missing = missing + int(val) # add to running total of missing alleles
			missDict[locus] = (missing/float(total)) # calculate missing data proportion for locus
			for item in remove:
				del self.d[locus][item] # remove missing data keys from self.d
		return missDict

	def makeSampleNames(self, inds, prefix, pad):
		#pad = len(str(inds)) # get number padding length
		female=0
		male=0
		indList = list()
		for i in range(inds):
			b = numpy.random.binomial(1, 0.5) # binomial to assign sex. 0 = f; 1 = m
			if b == 0:
				name = prefix + "_F" + str(female).zfill(pad)
				female = female+1
				indList.append(name)
			elif b == 1:
				name = prefix + "_M" + str(male).zfill(pad)
				male = male+1
				indList.append(name)

		return indList

	def simInds(self, inds, prefix, pad):
		indlist = self.makeSampleNames(inds, prefix, pad)
		data = collections.defaultdict(dict) # key1 = individual; key2 = locus, val = alleles

		# locus = locus name
		# key2 = dict; key=allele, val=count
		for (locus, key2) in self.d.items():
			keys = key2.keys() #get list of allele names
			vals = key2.values() #get list of allele counts
			vals = [int(i) for i in vals] # convert values to integers so that division happens properly in numpy.random.multinomial function

			for ind in indlist:
				m = numpy.random.multinomial(2, numpy.divide(vals, float(sum(vals)))) #draw two alleles from multinomial distribution for locus

				comb = dict(map(lambda i,j : (i,j), keys, m)) # combine the allele names with multinomial output

				# create list to hold alleles for this locus
				templist = list()
				for (key, val) in comb.items():
					if val > 0:
						for i in range(val):
							templist.append(key)
				templist.sort() # sort alleles in-place so they are in numerical order
				alleles = "".join(templist) # join into string
				data[ind][locus] = alleles #add to data dict of dicts

		df = pandas.DataFrame() # make empty dataframe
		for (ind, d ) in data.items(): # for each individual
			df_dict = pandas.DataFrame([d], index=[ind]) # convert individual's genotype from dict to pandas dataframe
			df = pandas.concat([df, df_dict]) # add to growing dataframe

		return df

	def simMissing(self, df):
		# determine which loci need to have missing data simulated
		simList = list() # list of loci needing missing data simulation
		for (key, val) in self.miss.items():
			if val > 0.0:
				simList.append(key) # add to list of missing data proportion > 0.0

		for locus in simList:
			for index, row in df.loc[:, [locus]].iterrows():
				s = numpy.random.binomial(1, self.miss[locus])
				if(s == 1):
					genoLen = len(str(row[locus])) # get length of encoded genotype
					newgeno = "0" * genoLen # make missing data genotype
					df.loc[index,locus] = newgeno # insert missing data genotype

