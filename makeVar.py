#!/usr/bin/env python

######################
## HL-LHC projection###
## Heling Zhu, 2018 ###
######################

import sys
#ROOTSYS = '/afs/atlas.umich.edu/opt/root/lib'
#sys.path.append(ROOTSYS)

#####################
## Import Module  ###
#####################
import array
import os
import glob
from math import sqrt,fabs,sin,log
from ROOT import TFile,TTree,TChain,TBranch,TH1,TH1F,TList
from ROOT import TLorentzVector,TGraphAsymmErrors,TMath
from ROOT import THStack,TCanvas,TLegend,TColor,TPaveText,TPad
from ROOT import gStyle,gDirectory
from ROOT import Double

def setVarHist(histo='', var='', **kw):
    ## book histogram
    nbins=histo.GetNbinsX()
    histo_xmin=histo.GetXaxis().GetXmin()
    histo_xmax=histo.GetXaxis().GetXmax()
    hist_up=TH1F(var+'_up', var+'_up', nbins, histo_xmin, histo_xmax)
    hist_down=TH1F(var+'_down', var+'_down', nbins, histo_xmin, histo_xmax)

    print nbins

    for i in range(1,nbins):
        ndata=0
        ndata=histo.GetBinContent(i)  # no overflow
        nerror=histo.GetBinError(i)
        nup = ndata+nerror
        ndown = ndata-nerror
        print "nup = ", nup, "   ndown = ", ndown

        hist_up.SetBinContent(i, nup)
        hist_up.SetBinError(i, 0)
        hist_down.SetBinContent(i, ndown)
        hist_down.SetBinError(i, 0)

    return [hist_up, hist_down]



###################
## Main Function ##
###################
if __name__ == "__main__":

    if len(sys.argv) == 2:
        inputdir=sys.argv[1]
    else:
        raise RuntimeError('One and only one arg needed: root file path')

    #hname = 'MVV'
    hname = 'TagJJM_final'

    uncers=['dataonly', 'uncer0', 'uncer5', 'uncer10', 'uncer30']

    outfile=inputdir+"/var_"+hname+".root"
    resultRoot=TFile(outfile, 'RECREATE')

    #print "Make => dataonly"
    #in1=inputdir+"/dataonly_bins_differential_uncer0_"+hname+".root"
    #fin1=TFile(in1)
    #hist1=gDirectory.Get("final")
    #outh1 = setVarHist(hist1, 'dataonly')
    #outh1_up = outh1[0]
    #outh1_up.SetDirectory(resultRoot)
    #outh1_down = outh1[1]
    #outh1_down.SetDirectory(resultRoot)
    #resultRoot.Write()
    for uncer in uncers:
       print "Make => ", uncer
       in2="test.root"
       if uncer=='dataonly': in2=inputdir+"/dataonly_bins_differential_uncer0_"+hname+".root"
       else: in2=inputdir+"/bins_differential_"+uncer+"_"+hname+".root"
       fin2=TFile(in2)
       hist2=gDirectory.Get("final")
       outh2 = setVarHist(hist2, uncer)
       outh2_up = outh2[0]
       outh2_up.SetDirectory(resultRoot)
       outh2_down = outh2[1]
       outh2_down.SetDirectory(resultRoot)
       resultRoot.Write()

    print "Done! Output file: ", outfile
