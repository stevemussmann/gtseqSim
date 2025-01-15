from collections import defaultdict

import numpy
import pandas
import random
import re
#import time

class Reproduce():
	'Class for simulating reproduction within or among 1-2 sample groups'

	def __init__(self, simPdf, simPdf2=None):
		self.geno1 = simPdf
		self.geno2 = simPdf2

	def repro(self, nOff, prefix):
		#print(self.geno1)
		if self.geno2 is not None:
			print("geno2 found")
			#print(self.geno2)
		else:
			print("Conducting within-population crosses...\n")
			gen = int(prefix[1:])
			if gen > 1:
				prevgen = "F" + str(gen-1)
				parentage = prevgen + ".parentage.txt"
				# after F1, downsample to retain 1 male and 1 female per family group
				genoMatrix, sibDict = self.subsample(self.geno1, parentage)
			else:
				# if F1, send full simulated genotype matrix
				genoMatrix = self.geno1

			if gen > 1:	
				spawnPairs = self.getSpawnPairs(genoMatrix, sibDict)
			else:
				spawnPairs = self.getSpawnPairs(genoMatrix)
				
			df = self.spawn(spawnPairs, nOff, prefix, genoMatrix)
			return df
			#print(df)

	def subsample(self, genoMatrix, parentage):
		with open(parentage, 'r') as f:
			lines = f.readlines()

		# get dict of families
		famDict = defaultdict(list)
		lines = lines[1:] # remove header line from lines
		for line in lines:
			temp = line.split()
			key = ",".join([temp[0], temp[1]])
			famDict[key].append(temp[2])

		#print(famDict)

		# pick one male and one female from each family
		keepList = list()
		sibDict = dict()
		for fam, sibs in famDict.items():
			mList, fList = self.checkMF(sibs) # get lists of male and female individuals

			mRand = random.sample(mList, 1)
			fRand = random.sample(fList, 1)
			
			keepList.append(mRand[0])
			keepList.append(fRand[0])

			sibDict[mRand[0]] = fRand[0]

		genoMatrix = genoMatrix.loc[keepList]

		return genoMatrix, sibDict

	def spawn(self, dPairs, nOff, prefix, genoMatrix):
		parentageFile = prefix + ".parentage.txt"
		fh = open(parentageFile, 'w')
		fh.write("male_parent\tfemale_parent\toffspring\n")

		dictlist = list()
		female=0
		male=0

		#for each spawning pair
		for key, pair in dPairs.items():
			#for each offspring per pair
			print("Simulating", str(nOff), "progeny for sample pair", str(pair))
			for n in range(nOff):
				mHap = self.getHaplotype(pair[0], genoMatrix) # sample male parent haplotype
				fHap = self.getHaplotype(pair[1], genoMatrix) # sample female parent haplotype
			
				offspring = self.combDict(mHap, fHap) # combine haplotypes
				b = numpy.random.binomial(1, 0.5) # binomial to decide sex. 0 = f; 1 = m
				if b == 0:
					name = prefix + "_F" + str(female)
					female = female+1
				elif b == 1:
					name = prefix + "_M" + str(male)
					male = male+1
				
				# write parentage information to file
				parentLine = pair[0] + "\t" + pair[1] + "\t" + name + "\n"
				fh.write(parentLine)

				offspring["index"]=name
				dictlist.append(offspring)
			
		df = pandas.DataFrame(dictlist) #single conversion to pandas dataframe
		df.set_index('index', inplace=True) #set index of pandas dataframe

		fh.close()

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

	def getSpawnPairs(self, genoMatrix, sibDict=None):
		index_list = genoMatrix.index.to_list()

		mList, fList = self.checkMF(index_list) # get lists of male and female individuals
		
		nPairs = min(len(mList), len(fList)) # get length of shorter list of individuals

		# randomly sample lists to get equal length lists for pairing
		mRand = random.sample(mList, nPairs)
		fRand = random.sample(fList, nPairs)

		dPairs = defaultdict(list)
			
		## check for full-sibling spawn pairs and correct to prevent inbreeding
		# Only one male and female is sampled per family, so can swap with neighboring pair
		# in list to prevent inbreeding
		for i in range(nPairs):
			if sibDict:
				if sibDict[mRand[i]] == fRand[i]:
					#print("Full Sib Pair")
					#print(mRand[i], fRand[i])
					# if first pair are siblings, swap female with 2nd pair in list
					if i == 0:
						#print("first pair")
						temp = fRand[i+1]
						fRand[i+1] = fRand[i]
						fRand[i] = temp
					# if second pair or later are siblings, swap with i-1 pair in list.
					else:
						#print("after first pair")
						temp = fRand[i-1]
						fRand[i-1] = fRand[i]
						fRand[i] = temp

		# append spawing pairs to default dict once checks for siblings completed.
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
