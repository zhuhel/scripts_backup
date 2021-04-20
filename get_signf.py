#!/usr/bin/env python

######################
## rebin histogram ###
## Lailin, 2012 ######
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

def get_hist_significance(histsig='', histbkg='', profile=1, scale=1, **kw):
    nsig_tot=histsig.Integral()
    nbkg_tot=histbkg.Integral()
    ## scale sig and bkg histo to 1
    if scale==1:
      if nsig_tot!=0:
        histsig.Scale(1.0/nsig_tot)
        nsig_tot=1.0
      if nbkg_tot!=0:
        histbkg.Scale(1.0/nbkg_tot)
        nbkg_tot=1.0
    ## book histogram
    nbins=histsig.GetNbinsX()
    histo_xmin=histsig.GetXaxis().GetXmin()
    histo_xmax=histsig.GetXaxis().GetXmax()
    ## significance
    hist_signf=TH1F('significance', 'significance', nbins, histo_xmin, histo_xmax)
    hist_signf.Sumw2()

    for i in range(1,nbins):
        nsig, nbkg=0, 0
        nsig=histsig.GetBinContent(i)  # no overflow
        nbkg=histbkg.GetBinContent(i)  # no overflow

        print "sig/bkg: ", nsig, nbkg
        signf=get_signf(nsig, nbkg, profile)
        hist_signf.SetBinContent(i, signf)

    return [hist_signf]

def get_signf(nsig=1, nbkg=1, profile=1, uncer=0,**kw):
    signf=0
    if profile==0:
        if nbkg+nsig>0: signf=nsig/sqrt(nbkg+nsig) 
        else: signf=-1
    if profile==1:
        if nbkg!=0:
          if nsig/nbkg <-1:
            print 'Error=> nsig= %g , nbkg= %g ' % (nsig, nbkg) 
            signf=-1
          else:
            if uncer==0: signf2=(2*((nsig+nbkg)*log(1+nsig/nbkg) - nsig))
            else: signf2=2.*( (nsig+nbkg)*log((nsig+nbkg)*(nbkg+(nbkg*uncer)*(nbkg*uncer))/(nbkg*nbkg+(nsig+nbkg)*(nbkg*uncer)*(nbkg*uncer))) - nbkg*nbkg/(nbkg*uncer)/(nbkg*uncer)*log(1+(nbkg*uncer)*(nbkg*uncer)*nsig/(nbkg*(nbkg+(nbkg*uncer)*(nbkg*uncer)))))
            if signf2 >=0 : signf=sqrt(signf2)
            else:
              print 'Error=> nsig= %g , nbkg= %g signf2= %g ' % (nsig, nbkg, signf2) 
              signf=-1
        else: signf=-1
    return signf

###################
## Main Function ##
###################
if __name__ == "__main__":
    sig1="Up_ewk"
    bkg1="Up_qcd"
    cut="TagJJM"
    uncer=2

    if len(sys.argv) == 2:
        inputdir=sys.argv[1]
    elif len(sys.argv) == 3:
        inputdir=sys.argv[1]
        cut=sys.argv[2]
    else:
        raise RuntimeError('One and only one arg needed: root file path')
    
    outfile=inputdir+'significance_uncer0.root'
    resultRoot=TFile(outfile, 'RECREATE')

    inputSig1="{0}/{1}/hist-xAOD.root".format(inputdir, sig1)
    inputBkg1="{0}/{1}/hist-xAOD.root".format(inputdir, bkg1)

    f_sig1=TFile(inputSig1);
    histo_Sig1=gDirectory.Get(hname)
    f_bkg1=TFile(inputBkg1);
    histo_Bkg1=gDirectory.Get(hname)

    histo_Sig=histo_Sig1.Clone()
    histo_Sig.Rebin(50)
    histo_Bkg=histo_Bkg1.Clone()
    histo_Bkg.Rebin(50)

    nsig = histo_Sig.Integral()
    nbkg = histo_Bkg.Integral()
    m_signif = get_signf(nsig, nbkg, 1, uncer)
    print m_signif

    signf_results=get_hist_significance(histo_Sig, histo_Bkg, 1, 0)
    histo_signf=signf_results[0]
    histo_signf.SetDirectory(resultRoot)

    resultRoot.Write() 
    print "Done! Output file: ", outfile 
