#!/usr/bin/env python

###########################
## Do significance scan ###
## Heling, 2018 ###########
###########################

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

def get_hist_significance(histsig='', histbkg='', scale=1, uncer=0, **kw):
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
    hname = "significance"
    hist_signf=TH1F(hname, hname, nbins, histo_xmin, histo_xmax)
    hist_signf.Sumw2()
    ## sig efficiency
    hname = "sig_efficiency"
    hist_sigeff=TH1F(hname, hname, nbins, histo_xmin, histo_xmax)
    hist_sigeff.Sumw2()
    ## bkg rejection efficiency
    hname = "bkg_rejection"
    hist_bkgrej=TH1F(hname, hname, nbins, histo_xmin, histo_xmax)
    hist_bkgrej.Sumw2()

    startp=histsig.FindBin(600.)
    endp  =histbkg.FindBin(3000.)

    for i in range(startp,endp):
    #for i in range(1,nbins):
        ## calculate error for each cut
        err=0.
        for j in range(i,nbins):
           b_err=histbkg.GetBinError(j)
           err=err+b_err*b_err
        err=sqrt(err)
        print "Bkg stat. error: ", err

        nsig, nbkg=0, 0
        nsig=histsig.Integral(i, nbins)  # no overflow
        nbkg=histbkg.Integral(i, nbins)  # no overflow
        #nbkg=histbkg.IntegralAndError(i, nbins, Double(err) )  # no overflow

        #print "sig/bkg: ", nsig, nbkg
        signf=get_signf(nsig, nbkg, uncer, err)
        hist_signf.SetBinContent(i, signf)
        ## signal efficiency
        sigeff=nsig/nsig_tot
        hist_sigeff.SetBinContent(i, sigeff)
        ## bkg rejection
        if nbkg_tot!=0:
          bkgrej=1-nbkg/nbkg_tot
          hist_bkgrej.SetBinContent(i, bkgrej)
        elif nbkg_tot==0:
          hist_bkgrej.SetBinContent(i, 1)

    return [hist_signf, hist_sigeff, hist_bkgrej]

def get_signf(nsig=1, nbkg=1, uncer=0, err=0., **kw):
    signf=0
    #err=0.
    delta_bkg=uncer*nbkg+err
    if nbkg!=0:
      if nsig/nbkg <-1:
        print 'Error=> nsig= %g , nbkg= %g ' % (nsig, nbkg) 
        signf=-1
      else:
        signf= nsig/sqrt(nbkg+delta_bkg*delta_bkg)
    else: signf=-1
    return signf

###################
## Main Function ##
###################
if __name__ == "__main__":
    sig1="Up_ewk"
    bkg1="Up_qcd"
    hname="TagJJM_final"
    uncer=0

    if len(sys.argv) == 2:
        inputdir=sys.argv[1]
    elif len(sys.argv) == 3:
        inputdir=sys.argv[1]
        hname=sys.argv[2]
    else:
        raise RuntimeError('One and only one arg needed: root file path')
    
    if uncer==0: outfile = inputdir+hname+'_scanSignf_lumi3000_uncer0.root'
    elif uncer==0.05: outfile = inputdir+hname+'_scanSignf_lumi3000_uncer5.root'
    elif uncer==0.1: outfile = inputdir+hname+'_scanSignf_lumi3000_uncer10.root'
    elif uncer==0.3: outfile = inputdir+hname+'_scanSignf_lumi3000_uncer30.root'
    #outfile = inputdir+'/'+hname+'_scanSignf_lumi3000_noerr.root'
    resultRoot=TFile(outfile, 'RECREATE')

    inputSig1="{0}/{1}/hist-xAOD.root".format(inputdir, sig1)
    inputBkg1="{0}/{1}/hist-xAOD.root".format(inputdir, bkg1)

    f_sig1=TFile(inputSig1);
    histo_Sig1=gDirectory.Get(hname)
    f_bkg1=TFile(inputBkg1);
    histo_Bkg1=gDirectory.Get(hname)

    histo_Sig=histo_Sig1.Clone()
    histo_Sig.Rebin(50)
    histo_Sig.Scale(12.196*3000/166876.75)
    histo_Bkg=histo_Bkg1.Clone()
    histo_Bkg.Rebin(50)
    histo_Bkg.Scale(1363.9*3000/413075.09)
    signf_results=get_hist_significance(histo_Sig, histo_Bkg, 0, uncer)
    histo_signf=signf_results[0]
    histo_sigeff=signf_results[1]
    histo_bkgrej=signf_results[2]

    histo_signf.SetDirectory(resultRoot)
    histo_sigeff.SetDirectory(resultRoot)
    histo_bkgrej.SetDirectory(resultRoot)

    resultRoot.Write() 
    print "Done! Output file: ", outfile 
