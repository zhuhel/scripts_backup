#!/usr/bin/env python

#########################################
# Heling Zhu, Apr. 9, 2019 @ Hefei
# Version 0
#########################################
# Used to make the judgement from 
# RTOG 0813 table with a provided
# PTV Volume and [R100% R50% D2cm V20] set.
############################################

import math
import os
from array import array

def linear(PTV, ptv1, ptv2, a1, a2):

    ## For values of PTV not specified, linear interpolation between table entries is required.
    return (a2-a1)/(ptv2-ptv1)*(PTV-ptv1)+a1
	

def judgement(PTV=0., R100=9999., R50=9999., D2cm=9999., V20=9999.):

    ## read the table: RTOG 0813
    _None={
	1.8:   [1.2, 5.9, 50.0, 10],
	3.8:   [1.2, 5.5, 50.0, 10],
	7.4:   [1.2, 5.1, 50.0, 10],
	13.2:  [1.2, 4.7, 50.0, 10],
	22.0:  [1.2, 4.5, 54.0, 10], 
	34.0:  [1.2, 4.3, 58.0, 10], 
	50.0:  [1.2, 4.0, 62.0, 10],
	70.0:  [1.2, 3.5, 66.0, 10],
	95.0:  [1.2, 3.3, 70.0, 10],
	126.0: [1.2, 3.1, 73.0, 10],
	163.0: [1.2, 2.9, 77.0, 10]
    }
    _Minor={
	1.8:   [1.5, 7.5, 57.0, 15],
	3.8:   [1.5, 6.5, 57.0, 15],
	7.4:   [1.5, 6.0, 58.0, 15],
	13.2:  [1.5, 5.8, 58.0, 15],
	22.0:  [1.5, 5.5, 63.0, 15], 
	34.0:  [1.5, 5.3, 68.0, 15], 
	50.0:  [1.5, 5.0, 77.0, 15],
	70.0:  [1.5, 4.8, 86.0, 15],
	95.0:  [1.5, 4.4, 89.0, 15],
	126.0: [1.5, 4.0, 91.0, 15],
	163.0: [1.5, 3.7, 94.0, 15]
    }


    if PTV in _None:
	my_None = _None[PTV]
	my_Minor = _Minor[PTV]
    else:
	a1_None = a2_None = []
	a1_Minor= a2_Minor= []
	# do linear interpolation
	for ptvscan in sorted(_None):
	    if ptvscan<PTV:
		ptv1 =  ptvscan
		a1_None = _None[ptv1]
		a1_Minor = _Minor[ptv1]
	    else:
		ptv2 = ptvscan
		a2_None = _None[ptv2]
		a2_Minor = _Minor[ptv2]
		break
        my_None = [linear(PTV,ptv1,ptv2,a1,a2) for a1,a2 in zip(a1_None,a2_None)]
        my_Minor = [linear(PTV,ptv1,ptv2,a1,a2) for a1,a2 in zip(a1_Minor,a2_Minor)]

    ## 1. R100
    if my_None[0]<=R100:
	if my_Minor[0]<=R100:
	    print "Major: R100=%.1f!" %(R100)
	else:
	    print "Minor: R100=%.1f!" %(R100)
    else:
	print "None: R100=%.1f!" %(R100)
    
    ## 2. R50
    if my_None[1]<=R50:
	if my_Minor[1]<=R50:
	    print "Major: R50=%.1f!" %(R50)
	else:
	    print "Minor: R50=%.1f!" %(R50)
    else:
	print "None: R50=%.1f!" %(R50)
    
    ## 3. D2cm
    if my_None[2]<=D2cm:
	if my_Minor[2]<=D2cm:
	    print "Major: D2cm=%.1f!" %(D2cm)
	else:
	    print "Minor: D2cm=%.1f!" %(D2cm)
    else:
	print "None: D2cm=%.1f!" %(D2cm)
    
    ## 4. V20
    if my_None[3]<=V20:
	if my_Minor[3]<=V20:
	    print "Major: V20=%.1f!" %(V20)
	else:
	    print "Minor: V20=%.1f!" %(V20)
    else:
	print "None: V20=%.1f!" %(V20)
    

if __name__ == '__main__':

    PTV = float(input("Enter your PTV Volume:"))
    R100 = float(input("Enter the value of R100% for judgement:"))
    R50 = float(input("Enter the value of R50% for judgement:"))
    D2cm = float(input("Enter the value of D2cm for judgement:"))
    V20 = float(input("Enter the value of V20 for judgement:"))

    judgement(PTV, R100, R50, D2cm, V20)
