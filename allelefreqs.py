import collections
import pandas
import sys

from contextlib import redirect_stdout

class Allelefreqs():
	'Class for calculating allele frequencies'

	def __init__(self, df, log):
		self.pdf = df
		self.log = log

	def calcFreqs(self):
		# open log file
		lfh = open(self.log, 'a')

		dofd=collections.defaultdict(dict) # dict of dicts; key1 = locus name, key2 = allele, val = allele count

		for (columnName, columnData) in self.pdf.items():
			#print(columnName)
			alleleDict = self.pdf[columnName].value_counts().to_dict()
			for( key, val ) in alleleDict.items():
				try:
					int(key)
				except ValueError as e:
					print("Unexpected error in parsing allele frequencies:")
					print(e)
					print("Check if genotypes are encoded in 2-digit or 3-digit format.")
					print("")
					with redirect_stdout(lfh):
						print("Unexpected error in parsing allele frequencies:")
						print(e)
						print("Check if genotypes are encoded in 2-digit or 3-digit format.")
						print("")
					raise SystemExit

				try:
					if (len(str(key)) % 2) == 0:
						quotient, remainder = divmod(len(str(key)), 2) # accounts for any length of allele encoding (e.g., 2-digit or 3-digit alleles) 
						res_first = str(key[:quotient + remainder])
						res_second = str(key[quotient + remainder:])

						# add first allele
						if( res_first not in dofd[columnName] ):
							dofd[columnName][res_first] = val
						else:
							dofd[columnName][res_first] = dofd[columnName][res_first] + val

						# add second allele
						if( res_second not in dofd[columnName] ):
							dofd[columnName][res_second] = val
						else:
							dofd[columnName][res_second] = dofd[columnName][res_second] + val
					else:
						raise ValueError("Genepop alleles should be encoded as 2-digit or 3-digit format (i.e., 0202 or 102102). Missing data should be 0000 or 000000.")
				except ValueError as e:
					print("Unexpected error:")
					print(e)
					print("")
					with redirect_stdout(lfh):
						print("Unexpected error:")
						print(e)
						print("")
					raise SystemExit

		lfh.close()

		return dofd
