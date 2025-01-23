#from popmap import Popmap

from itertools import takewhile

import pandas

class Genepop():
	'Class for parsing and writing Genepop format files'

	def __init__(self, f, log):
		self.file = f # input genepop file
		self.log = log # logfile

	def parse(self):
		# write to log file
		lfh = open(self.log, 'a')
		lfh.write("Begin reading input genepop file " + str(self.file) + ".\n")

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
		lfh.write("End reading input genepop file " + str(self.file) + ".\n")
		lfh.close()

		return df

	def write(self, df, f):
		# df = dataframe to write to file
		# f = output file
		f = f + ".genepop.txt"
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

