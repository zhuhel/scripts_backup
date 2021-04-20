#!/usr/bin/env python

###############################
# Heling Zhu, Aug. 2019 @CERN
##############################

import sys
import math
import array
import os
import glob
from math import sqrt,fabs,sin,log
from ROOT import TFile,TTree,TChain,TBranch,TH1,TH1F,TList
from ROOT import TLorentzVector,TGraphAsymmErrors,TMath
from ROOT import THStack,TCanvas,TLegend,TColor,TPaveText,TPad
from ROOT import gStyle,gDirectory,gPad
from ROOT import Double

bkgs = ['qqZZ', 'qqZZEW', 'ggZZ']
Chs  = ['ggF_2mu2e', 'ggF_4e', 'ggF_4mu', 'ggF_bkg', 'VBF_incl']
lumi = 138.965
y = [-99., -99., -99., -99., -99.]
err = [-99., -99., -99., -99., -99.]

for bkg in bkgs:
    tfin = TFile.Open('nominal_'+bkg+'.root')
    for ic,ch in enumerate(Chs):
       hname = 'm4l_'+ch+'_13TeV'
       hist = tfin.Get(hname)

       y[ic] = hist.IntegralAndError(1, hist.GetNbinsX(), Double(err[ic]))

       
    tfin.Close()

    #print ("n_%s\t& %.4f & %.4f & %.4f & %.4f \\" %(bkg, y[0], y[1], y[2], y[3]))
    print ("n_%s\t& %.4f & %.4f & %.4f & %.4f & %.4f \\" %(bkg, y[0], y[1], y[2], y[3], y[4]))
