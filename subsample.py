import collections
import numpy
import pandas
import random

class Subsample():
	'Class to subsample offspring'

	def __init__(self, lam):
		self.lam = lam

	def poisson(self, d):
		nFam = len(d) # number of families
		#print(nFam)
		s = numpy.random.poisson(self.lam, nFam)

		return s

	def subsample(self, d, s, l=None):
		i = 0 # initialize counter
		keeplist = list() # will hold list of individuals to be retained
		for parents, offspring in d.items():
			if l:
				offspring = list(set(offspring) - set(l)) # remove offspring from the list that were later used as parents
			random.shuffle(offspring)
			if s[i] > len(offspring):
				print("WARNING: number of offspring to be sampled from family group was larger than family group itself. All offspring kept from family group", parents)
				kept = offspring[:len(offspring)]
			else:
				kept = offspring[:s[i]]
	
			keeplist.extend(kept)
			#print(offspring)
			i+=1 # increment counter
		
		# get inverse of keeplist. The inverse list will be dropped from pandas dataframe
		keepInds = set(keeplist)
		allInds = set().union(*d.values())
		if l:
			discard = list(allInds - keepInds - set(l)) # need to prevent parents from being dropped.
		else:
			discard = list(allInds - keepInds)
		#print(keeplist)
		#print(discard)

		return discard
