#import collections
#import numpy
import pandas

class Reproduce():
	'Class for simulating reproduction within or among 1-2 sample groups'

	def __init__(self, simPdf, simPdf2=None):
		self.geno1 = simPdf
		self.geno2 = simPdf2

		#print(self.geno1)
		if self.geno2 is not None:
			print("geno2 found")
			#print(self.geno2)

