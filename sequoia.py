import collections
import os
import pandas
import re

from majmin import MajMin

class Sequoia():
	'Class for converting pandas dataframe to sequoia format'

	def __init__(self, df, mval):
		self.pdf = df
		self.mval = mval + mval # missing data value for locus
		mm = MajMin(self.pdf, 0, 1, 2)
		self.recode12 = mm.getMajorMinor(self.mval) #stores major/minor allele for converting to binary format. 2 = missing, 0 = major, 1 = minor
		#print(self.recode12)
		self.genotypes = {'00': '0', '11': '2', '10': '1', '01': '1', '22': '-9'} # map for converting binary format to sequoia format

	def convert(self):
		output = list()

		output = self.makeSequoia(output)
		
		return output

	def makeSequoia(self, output):
		# open sequoia life history file for writing
		fh=open("sequoia.LH.txt", 'w')

		for sampleName, row in self.pdf.iterrows():
			lineList = list()

			# write relevant data to life history file
			fh.write(sampleName)
			fh.write("\t")

			# get sex data for individual
			tempSex = self.checkMF(sampleName)
			if tempSex.casefold() == "m" or tempSex.casefold() == "male":
				fh.write("2") # need to convert sex data to sequoia format (1 = female, 2 = male, 3 = unknown)
			elif tempSex.casefold() == "f" or tempSex.casefold() == "female":
				fh.write("1") # need to convert sex data to sequoia format (1 = female, 2 = male, 3 = unknown)
			else:
				fh.write("3") # need to convert sex data to sequoia format (1 = female, 2 = male, 3 = unknown)
			fh.write("\t")

			# get year individual was born
			bornYear = self.checkYear(sampleName)
			fh.write(bornYear)
			fh.write("\n")

			lineList.append(sampleName)
			
			for (locus, genotype) in row.items():
				quotient, remainder = divmod(len(str(genotype)), 2)
				a0 = str(genotype[:quotient + remainder])
				a1 = str(genotype[quotient + remainder:])
				alleles = [a0, a1]
				tempList = list()
				
				# next line is testing for original data missing genotype value (0000) instead of binary recoded missing value (2). 
				if genotype == self.mval:
					tempList.append(self.recode12[locus][genotype])
					tempList.append(self.recode12[locus][genotype])
				else:
					for allele in alleles:
						tempList.append(self.recode12[locus][allele])
				tempString = ''.join(tempList)
				try:
					tempString = self.genotypes[tempString]
				except KeyError as e:
					print("Problem converting locus" + locus + "for individual" + sampleName + "to create Sequoia output.")
					print("Problem key when accessing recoded allele hash:" + e)
					print("Exiting program...")
					print("")
					print("")
					raise SystemExit
				lineList.append(tempString)

			lineString = "\t".join(lineList)

			output.append(lineString)

		# close sequoia life history file
		fh.close()

		return output
	
	def split(self, word):
		return [char for char in word]
	
	def checkMF(self, sampleName):
		regexM = r'_M\d+$'
		regexF = r'_F\d+$'

		if(re.search(regexM, sampleName)):
			return "M"
		elif(re.search(regexF, sampleName)):
			return "F"
		else:
			return "U"
	
	def checkYear(self, sampleName):
		regex = r'^F\d+_[MF]\d+$'

		if(re.search(regex, sampleName)):
			temp = sampleName.split("_")
			genName = temp[0]
			year = genName[1:]
			return year
		else:
			return "0"
