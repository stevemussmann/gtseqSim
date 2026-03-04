#!/usr/bin/env python3

from comline import ComLine
from genepop import Genepop

import argparse
#import os
import sys

def main():
	input = ComLine(sys.argv[1:])

	gpop = Genepop(input.args.genepop, input.args.json)
	gpop.parseGenepop() # parse data from genepop file
	gpop.convertGenepop() # convert genepop file to microhaplotype format

main()

raise SystemExit
