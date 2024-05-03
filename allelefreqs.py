import collections
import pandas

class Allelefreqs():
	'Class for calculating allele frequencies'

	def __init__(self, df):
		self.pdf = df

	def calcFreqs(self):
		dofd=collections.defaultdict(dict) # dict of dicts; key1 = locus name, key2 = allele, val = allele count

		for (columnName, columnData) in self.pdf.items():
			#print(columnName)
			alleleDict = self.pdf[columnName].value_counts().to_dict()
			for( key, val ) in alleleDict.items():
				quotient, remainder = divmod(len(str(key)), 2)
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

			#print(dofd)
			#print("")

		return dofd
