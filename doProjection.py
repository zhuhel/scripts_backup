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

def ResetError(histo='', **kw):
    ## book histogram
    nbins=histo.GetNbinsX()
    histo_xmin=histo.GetXaxis().GetXmin()
    histo_xmax=histo.GetXaxis().GetXmax()
    hist_out=TH1F('psudoData', 'psudoData', nbins, histo_xmin, histo_xmax)

    for i in range(1,nbins):
        ndata=0
        ndata=histo.GetBinContent(i)  # no overflow
        nerror=sqrt(ndata)

        hist_out.SetBinContent(i, ndata)
        hist_out.SetBinError(i, nerror)
        #hist_out.SetBinError(i, 0)

    return hist_out

def setBkgUncer(histo='', uncer=0, **kw):
    ## book histogram
    nbins=histo.GetNbinsX()
    histo_xmin=histo.GetXaxis().GetXmin()
    histo_xmax=histo.GetXaxis().GetXmax()
    hist_out=TH1F('bkg', 'bkg', nbins, histo_xmin, histo_xmax)

    for i in range(1,nbins+1):
        ndata=0
        ndata=histo.GetBinContent(i)  # no overflow
        #nstat=histo.GetBinError(i)
        nstat=0.05*ndata
        nerror=sqrt(nstat*nstat+uncer*ndata*uncer*ndata)

        hist_out.SetBinContent(i, ndata)
        hist_out.SetBinError(i, nerror)
        #hist_out.SetBinError(i, 0)

    return hist_out


###################
## Main Function ##
###################
if __name__ == "__main__":
    if len(sys.argv) == 2:
        inputdir=sys.argv[1]
    else:
        raise RuntimeError('One and only one arg needed: root file path')

    hname = 'MVV'
    #hname = 'TagJJM_final'
    uncer=0
    if uncer==0:      outfile=inputdir+'all_bins_differential_uncer0_'+hname+'.root'
    elif uncer==0.05: outfile=inputdir+'all_bins_differential_uncer5_'+hname+'.root'
    elif uncer==0.1:  outfile=inputdir+'all_bins_differential_uncer10_'+hname+'.root'
    elif uncer==0.3:  outfile=inputdir+'all_bins_differential_uncer30_'+hname+'.root'
    resultRoot=TFile(outfile, 'RECREATE')

    smearSig="{0}/Up_ewk/hist-xAOD.root".format(inputdir)
    smearBkg="{0}/Up_qcd/hist-xAOD.root".format(inputdir)
    truthSig="{0}/truth_ewk/hist-xAOD.root".format(inputdir)

    f_smearSig=TFile(smearSig);
    histo_smearSig=gDirectory.Get(hname)
    f_smearBkg=TFile(smearBkg);
    histo_smearBkg=gDirectory.Get(hname)
    f_truthSig=TFile(truthSig);
    histo_truthSig=gDirectory.Get(hname)

    histo_smearSig.Rebin(100)
    histo_smearSig.Scale(12.196*3000/166876.75)
    histo_smearBkg.Rebin(100)
    histo_smearBkg.Scale(1363.9*3000./411962.56)
    histo_truthSig.Rebin(100)
    histo_truthSig.Scale(12.196*3000/166876.75)
    histo_data = histo_smearSig.Clone()
    histo_data.Add(histo_smearBkg)

    psudoData = ResetError(histo_data)
    histo_bkg = setBkgUncer(histo_smearBkg, uncer)
    psudoData.Sumw2()
    histo_bkg.Sumw2()
    testhist = psudoData.Clone()

    testhist.SetDirectory(resultRoot)
    histo_bkg.SetDirectory(resultRoot)

    psudoData.Add(histo_bkg, -1)
    histo_cF = histo_smearSig.Clone()
    histo_cF.Divide(histo_truthSig)
    histo_cF.SetDirectory(resultRoot)
    psudoData.Divide(histo_cF)
    psudoData.Scale(1./3000.)
    psudoData.SetName("final")

    psudoData.SetDirectory(resultRoot)
    resultRoot.Write()
    print "Done! Output file: ", outfile

