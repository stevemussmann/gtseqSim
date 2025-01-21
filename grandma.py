import collections
import os
import pandas
import re

from majmin import MajMin

class gRandma():
	'Class for converting pandas dataframe to gRandma format'

	def __init__(self, df, mval):
		self.pdf = df
		self.mval = mval # missing data value for allele
		self.genotypes = {'00': '', '01': 'A', '02': 'C', '03': 'G', '04': 'T', '05': '-'} # map for converting binary format to sequoia format
		
		## tried to see if I could get around single allele in a column error by 
		## sorting according to major/minor alleles. Doesn't seem to work. 
		#mm = MajMin(self.pdf, 0, 1, 2)
		#self.recode12 = mm.getMajorMinor(self.mval) #stores major/minor allele for converting to binary format. 2 = missing, 0 = major, 1 = minor
		#self.transposed12 = self.transpose(self.recode12) # transpose keys and values this around so it's easier to work with
		#print(self.transposed12)

	def transpose(self, dofd):
		transposed = collections.defaultdict(dict)

		for key, val in dofd.items():
			for key2, val2 in val.items():
				transposed[key].update({val2: key2})

		return transposed

	def convert(self):
		output = list()

		## for a biallelic marker, need to have homozygotes of each allele and 
		## heterozygotes (i.e., 3 different genotypes for a biallelic marker)
		blacklist = self.preCheck(self.pdf)
		#print(self.pdf)
		if blacklist:
			self.pdf.drop(blacklist, axis=1, inplace=True)

		#print(self.pdf)
		output = self.makeSequoia(output)
		
		return output
	
	def preCheck(self, df):
		alleleDict = dict()
		blacklist = list()

		for (columnName, columnData) in df.items():
			#print(columnName)
			alleleDict = self.pdf[columnName].value_counts().to_dict()
			#print(alleleDict)

			col0 = list()
			col1 = list()
			for genotype, count in alleleDict.items():
				quotient, remainder = divmod(len(str(genotype)), 2)
				a0 = str(genotype[:quotient + remainder])
				a1 = str(genotype[quotient + remainder:])
				if a0 != self.mval:
					col0.append(a0)
				if a1 != self.mval:
					col1.append(a1)

			set0 = set(col0)
			set1 = set(col1)

			if (len(set0) < 2) or (len(set1) < 2):
				blacklist.append(columnName)
				#print(columnName)
				#print(set0)
				#print(set1)

		#print(str(len(blacklist)))

		return blacklist


	def makeSequoia(self, output):

		## make header line
		headerList = list()
		headerList.append("Pop")
		headerList.append("Ind")
		
		colNames = list(self.pdf.columns) # get list of column names

		for colName in colNames:
			headerList.append(colName)
			colA2 = colName + ".A2"
			headerList.append(colA2)

		headerString = "\t".join(headerList)

		output.append(headerString)

		for sampleName, row in self.pdf.iterrows():
			lineList = list() # temporary list used to hold contents of line as it is built

			splitName = sampleName.split('_')
			lineList.append(splitName[0]) # add pop name
			lineList.append(sampleName) # add sample name
			
			# deal with alleles in concatenated format of pandas dataframe
			for (locus, genotype) in row.items():
				quotient, remainder = divmod(len(str(genotype)), 2)
				a0 = str(genotype[:quotient + remainder])
				a1 = str(genotype[quotient + remainder:])
				alleles = [a0, a1]

				## tried to see if I could get around single allele in a column error by 
				## sorting according to major/minor alleles. Doesn't seem to work. 
				#alleles = [str(self.recode12[locus][a0]), str(self.recode12[locus][a1])]
				#alleles.sort() # sort minor (col1), major (col2)
				#alleles[0] = self.transposed12[locus][alleles[0]]
				#alleles[1] = self.transposed12[locus][alleles[1]]

				tempList = list()
				
				# add alleles to string
				for allele in alleles:
					try:
						lineList.append(self.genotypes[allele])
					except KeyError as e:
						print("ERROR in gRandma conversion:")
						print(e)
						print("")
						raise SystemExit


			lineString = "\t".join(lineList)

			output.append(lineString)

		return output
