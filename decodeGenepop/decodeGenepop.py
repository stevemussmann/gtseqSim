#!/usr/bin/env python3

from comline import ComLine

import argparse
#import os
import sys

def main():
	input = ComLine(sys.argv[1:])
	print(input.args.infile)

main()

raise SystemExit
