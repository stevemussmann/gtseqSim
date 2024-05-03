#from popmap import Popmap

from itertools import takewhile

import pandas

class Genepop():
	'Class for parsing and writing Genepop format files'

	def __init__(self, f):
		self.file = f # input genepop file

	def parse(self):
		# read file
		with open(self.file) as fh:
			contents = fh.readlines()
			# strip newline characters
			contents = [line.strip() for line in contents]
		
		# remove header and get locus names
		contents.pop(0) # remove header line
		loci = list(self.retrieve_ele(contents, "Pop")) #retrieve list of loci
		llen = len(loci) #get number of loci
		del contents[:llen] # strip locus names from contents

		# make empty dataframe
		df = pandas.DataFrame(columns=loci)
		#print(df)

		# read into pandas dataframe
		for line in contents:
			if line.lower() != "Pop".lower():
				x = line.split(",")
				name = x[0].strip()
				data = x[1].strip().split()
				df.loc[len(df)] = data
				#print(data)

		#print(df)
		#print(loci)
		#print(contents)
		return df

	def write(self, df, f):
		# df = dataframe to write to file
		# f = output file
		towrite = list()
		towrite.append("Title line:\"\"")
		for col in df.columns:
			towrite.append(col)
		towrite.append("Pop")
		for (index, row) in df.iterrows():
			templist = list()
			tempname = list()
			tempname.append("simgeno")
			tempname.append(str(index))
			templist.append("".join(tempname))
			string = " ".join(row.values.flatten().tolist())
			templist.append(string)
			finalstring = " ,  ".join(templist)
			towrite.append(finalstring)

		with open(f, 'w') as fh:
			for line in towrite:
				fh.write(line)
				fh.write("\n")
		#print(towrite)

	def retrieve_ele(self, l, val):
		for ele in l:
			if ele.lower() == val.lower():
				return
			yield ele

'''
	def convert(self):
		pm = Popmap(self.pops)
		mapDict = pm.parseMap()

		# open file for writing population map.
		fh=open("genepop.popmap.txt", 'w')

		lineList = list()

		lineList.append('Title line:""')

		for (columnName, columnData) in self.pdf.items():
			lineList.append(columnName)

		for (pop, num) in mapDict.items():
			lineList.append("Pop")
			for sampleName, row in self.pdf.iterrows():
				sampleList = list()
				if self.pops[sampleName] == pop:
					# write to popmap
					fh.write(sampleName)
					fh.write("\t")
					fh.write(pop)
					fh.write("\n")

					# append data to sampleList
					sampleList.append(sampleName)
					sampleList.append(",")
					sampleList.append("")
					for (locus, genotype) in row.items():
						alleles = self.split(str(genotype))
						locusList = list()

						if len(alleles) == 1 and alleles[0] == '0':
							locusList.append(self.nucleotides[alleles[0]])
							locusList.append(self.nucleotides[alleles[0]])
						else:
							for allele in alleles:
								locusList.append(self.nucleotides[allele])
						locusStr = ''.join(locusList)
						sampleList.append(locusStr)
					sampleStr = ' '.join(sampleList)
					lineList.append(sampleStr)

		# close genepop popmap file
		fh.close()

		return lineList

	def split(self, word):
		return [char for char in word]
'''
