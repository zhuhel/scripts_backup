#!/usr/bin/python
#####
# Heling Zhu, Mar. 2020
#####

import sys,os
import glob
from math import sqrt
from itertools import izip

def make_comb(masses=[]):
  infile = "combination_LWA.xml"
  for m in masses:
     print "Looking at => %s" %(m)
     try:f=open(infile, "r")
     except IOError:
         print "Error:input file could not be opened! "
         sys.exit(1)

     logout=open("combination_mH%s.xml"%m, 'w+')
     for line in f:
         line = line.strip()
         if 'mass' in line: 
	    oline = line.replace('mass', m)
         else: oline = line
         logout.write("%s\n" %oline)
     f.close()
     logout.close()

if __name__ == '__main__':

  masses = ["400", "420", "440", "460", "480", "500", "520", "540", "560", "580", "600", "620", "640", "660", "680", "700", "720", "740", "760", "780", "800",  "820", "840", "860", "880", "900", "920", "940", "960", "980", "1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700", "1800", "1900", "2000"]
  make_comb(masses)

