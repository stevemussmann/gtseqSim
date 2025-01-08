from collections import defaultdict
import numpy
import pandas
import random
import re
import time

class Reproduce():
	'Class for simulating reproduction within or among 1-2 sample groups'

	def __init__(self, simPdf, simPdf2=None):
		self.geno1 = simPdf
		self.geno2 = simPdf2

	def repro(self, nOff):
		#print(self.geno1)
		if self.geno2 is not None:
			print("geno2 found")
			#print(self.geno2)
		else:
			print("only geno1 found")
			spawnPairs = self.getSpawnPairs()
			df = self.spawn(spawnPairs, nOff, "F1") # 10 is a placeholder for number offspring per spawn pair
			print(df)

	def spawn(self, dPairs, nOff, prefix):
		#df = pandas.DataFrame() # empty dataframe to hold offspring
		dictlist = list()
		female=0
		male=0
		#for each spawning pair
		for key, pair in dPairs.items():
			#for each offspring per pair
			print("Simulating", str(nOff), "progeny for sample pair", str(pair))
			#start_time = time.time()
			for n in range(nOff):
				mHap = self.getHaplotype(pair[0], self.geno1) # sample male parent haplotype
				fHap = self.getHaplotype(pair[1], self.geno1) # sample female parent haplotype
			
				offspring = self.combDict(mHap, fHap) # combine haplotypes
				b = numpy.random.binomial(1, 0.5) # binomial to decide sex. 0 = f; 1 = m
				if b == 0:
					name = prefix + "_F" + str(female)
					female = female+1
				elif b == 1:
					name = prefix + "_M" + str(male)
					male = male+1
				#print(name)

				##This was really slow
				#df_dict = pandas.DataFrame([offspring], index=[name])
				#df = pandas.concat([df, df_dict])
				
				##Faster method - make list of dicts and do single conversion to pandas dataframe at end
				offspring["index"]=name
				dictlist.append(offspring)
			
			#end_time = time.time()
			#elapsed = end_time - start_time
			#print("Time =", elapsed, "seconds")

		df = pandas.DataFrame(dictlist) #single conversion to pandas dataframe
		df.set_index('index', inplace=True) #set index of pandas dataframe
		return df


	def combDict(self, mHap, fHap):
		d = dict()
		for key in mHap:
			if key in fHap:
				temp = [mHap[key], fHap[key]]
				temp.sort()
				d[key] = ''.join(temp)
		return d
		
	def getHaplotype(self, ind, df):
		row = df.loc[ind] #extract individual
		d = row.to_dict() #covert to dict
		
		# iterate over dict to randomly draw one allele from each locus
		hap = dict() #holds haplotype that will be returned
		for locus, genotype in d.items():
			try:
				if len(str(genotype)) % 2 == 0:
					quotient, remainder = divmod(len(str(genotype)), 2)
					a0 = str(genotype[:quotient + remainder])
					a1 = str(genotype[quotient + remainder:])
					allele = self.alleleSelect(a0, a1)
					hap[locus] = allele
				else:
					raise ValueError("Genepop alleles should be encoded as 2-digit or 3-digit format (i.e., 0202 or 102102). Missing data should be 0000 or 000000.")
			except ValueError as e:
				print("ERROR:")
				print(e)
				print("")
				raise SystemExit
		
		return hap

	def alleleSelect(self, a0, a1):
		b = numpy.random.binomial(1, 0.5) # binomial to decide allele
		if b == 0:
			return a0
		elif b == 1:
			return a1

	def getSpawnPairs(self):
		index_list = self.geno1.index.to_list()

		mList, fList = self.checkMF(index_list) # get lists of male and female individuals
		
		nPairs = min(len(mList), len(fList)) # get length of shorter list of individuals

		# randomly sample lists to get equal length lists for pairing
		mRand = random.sample(mList, nPairs)
		fRand = random.sample(fList, nPairs)

		dPairs = defaultdict(list)
		for i in range(nPairs):
			dPairs[i].append(mRand[i])
			dPairs[i].append(fRand[i])

		return dPairs


	def checkMF(self, idx):
		regexM = r'_M\d+$'
		regexF = r'_F\d+$'

		mList = list()
		fList = list()

		for i in idx:
			if(re.search(regexM, i)):
				mList.append(i)
			elif(re.search(regexF, i)):
				fList.append(i)
			else:
				print("ERROR: this condition should be unreachable.")
				print("Simulated data contains individual not male or female.")
				print("")
				raise SystemExit

		return mList, fList
