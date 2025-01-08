from collections import defaultdict
#import numpy
import pandas
import random
import re

class Reproduce():
	'Class for simulating reproduction within or among 1-2 sample groups'

	def __init__(self, simPdf, simPdf2=None):
		self.geno1 = simPdf
		self.geno2 = simPdf2

	def repro(self):
		#print(self.geno1)
		if self.geno2 is not None:
			print("geno2 found")
			#print(self.geno2)
		else:
			print("only geno1 found")
			spawnPairs = self.getSpawnPairs()

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
