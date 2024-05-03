import collections
import numpy
import pandas

class SimGenos():
	'Class for simulating individual genotypes from allele frequency data'

	def __init__(self, d):
		self.d = d

	def simInds(self, inds):
		indlist = list(range(inds))
		#print(indlist)
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
			df_dict = pandas.DataFrame([d]) # convert individual's genotype from dict to pandas dataframe
			df = pandas.concat([df, df_dict], ignore_index=True) # add to growing dataframe
		#print(df)

		return df

	'''
		n=1 #number of trials
		p=0.05 #probability of each trial
		s = numpy.random.binomial(n, p)

		#print(str(s))

		# multinomial with multiple alleles
		#m = numpy.random.multinomial(2, [46.0/100, 44.0/100, 10.0/100]) # 3 alleles
		m = numpy.random.multinomial(2, numpy.divide([34, 41, 10, 13, 2], float(100))) # 5 alleles
		#m = numpy.random.multinomial(2, numpy.divide([50, 50], float(100))) # 2 alleles
		print(m)
		# ex. output = [ 0 2 0 ]
		# this means it landed 0 times on 1, 2 times on 2, and 0 times on 3. 
	'''
