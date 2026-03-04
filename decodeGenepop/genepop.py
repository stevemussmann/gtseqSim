#import os
#import pandas
import json

class Genepop():
	'Class for operating on Genepop format files'

	def __init__(self, file, ldict):
		self.file = file
		self.loci = list()
		self.genos = list()

		# read json
		with open(ldict, 'r') as fh:
			self.ldict = json.load(fh)
		
		# reverse keys and vals in ldict
		for locus, d in self.ldict.items():
			#print(locus)
			revDict = {val: key for key, val in d.items()}
			self.ldict[locus] = revDict

	def parseGenepop(self):
		# read genepop file
		with open(self.file, 'r') as fh:
			lines = [line.strip() for line in fh]

		header = lines.pop(0) # remove header from parsed file

		try:
			firstPop = lines.index("Pop")
			self.loci = lines[:firstPop] # pull locus names from header of file
			genos = lines[firstPop:] # pull genotypes from end of file
			self.genos = [geno for geno in genos if geno != "Pop"] # strip 'Pop' occurrences from genos
			#print(genos)
		except ValueError:
			print("\nNo 'Pop' lines were found in genepop file.")
			print("Is your genepop file formatted correctly?\n\n")
			raise SystemExit(1)

	def convertGenepop(self):
		print("Converting Genepop file...")
		lineList = list() # holds lines that will be written to csv file
	
		# make header line
		headerList = list()
		headerList.append("indiv")
		headerList.append("Population ID")
		headerList.append("colony2")
		headerList.append("POPCOLUMN_SEX")

		for locus in self.loci:
			a1 = locus + "_1"
			a2 = locus + "_2"
			headerList.append(a1)
			headerList.append(a2)

		header = ','.join(headerList) # construct header line
		lineList.append(header) # push to lineList

		# convert data back to microhap format
		for item in self.genos:
			genoList = list()
			itemList = item.split()
			itemList = [thing for thing in itemList if thing != ',']
			name = itemList.pop(0)
			genoList.append(name)
			genoList.append(name)
			genoList.append(name)
			genoList.append(name)
			for locus in itemList:
				try:
					if (len(str(locus)) % 2) == 0:
						quotient, remainder = divmod(len(str(locus)), 2) # accounts for any length of allele encoding (e.g., 2-digit or 3-digit alleles)
						gpAllele1 = str(locus[:quotient + remainder])
						gpAllele2 = str(locus[quotient + remainder:])

						genoList.append(gpAllele1)
						genoList.append(gpAllele2)

					else:
						raise ValueError("Genepop alleles should be encoded as 2-digit or 3-digit format (i.e., 0202 or 102102). Missing data should be 0000 or 000000.")
				except ValueError as e:
					print("Unexpected error:")
					print(e)
					print("")
					raise SystemExit(1)

			genoLine = ','.join(genoList)
			lineList.append(genoLine)

		outName = "convertedData.csv"
		fh = open(outName, 'w')
		for line in lineList:
			fh.write(line)
			fh.write("\n")
		fh.close()
