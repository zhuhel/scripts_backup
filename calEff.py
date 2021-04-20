#!/usr/bin/env python

import array
import sys,os
import glob
from math import sqrt,fabs,sin,log
from ROOT import TFile,TTree,TChain,TBranch,TH1,TH1F,TList
from ROOT import TLorentzVector,TGraphAsymmErrors,TMath
from ROOT import THStack,TCanvas,TLegend,TColor,TPaveText,TPad
from ROOT import gStyle,gDirectory
from ROOT import Double
from array import array


###################
## Main Function ##
###################
if __name__ == "__main__":

   #cuts=["cut", "bdt", "bdtg", "dnn"]
   cuts=["DNN2020", "DNN2019"]
   channels=["ggF_em", "ggF_4e", "ggF_4m", "ggF_bk", "VBF"]
   hist_signif_ggH={} 
   hist_signif_VBFH={}
   hist_eff_ggH={}
   hist_eff_VBFH={}
   hist_eff_bkg={}
   tfout=TFile.Open("significance.root", 'RECREATE')
   #tfout=TFile.Open("eff_signif_dnn.root", 'RECREATE')

   for ic,cut in enumerate(cuts):
     hist_signif_ggH[cut]={}
     hist_signif_VBFH[cut]={}
     hist_eff_ggH[cut]={}
     hist_eff_VBFH[cut]={}
     hist_eff_bkg[cut]={}
     for j,ch in enumerate(channels):
       hname = "Significance_ggH_%s_%s" %(cut, ch)
       hist=TH1F(hname, hname, 6, 0, 6)
       hist.SetDirectory(tfout)
       hist.Sumw2()
       hist_signif_ggH[cut][ch]=hist

       hname = "Significance_VBFH_%s_%s" %(cut, ch)
       hist=TH1F(hname, hname, 6, 0, 6)
       hist.SetDirectory(tfout)
       hist.Sumw2()
       hist_signif_VBFH[cut][ch]=hist

       hname = "Eff_ggH_%s_%s" %(cut, ch)
       hist=TH1F(hname, hname, 6, 0, 6)
       hist.SetDirectory(tfout)
       hist.Sumw2()
       hist_eff_ggH[cut][ch]=hist

       hname = "Eff_VBFH_%s_%s" %(cut, ch)
       hist=TH1F(hname, hname, 6, 0, 6)
       hist.SetDirectory(tfout)
       hist.Sumw2()
       hist_eff_VBFH[cut][ch]=hist

       hname = "Eff_bkg_%s_%s" %(cut, ch)
       hist=TH1F(hname, hname, 6, 0, 6)
       hist.SetDirectory(tfout)
       hist.Sumw2()
       hist_eff_bkg[cut][ch]=hist

   for ic,cut in enumerate(cuts):
     ## read the histograms
     path=cut+"_200/Sum"
     f_qqZZ=TFile.Open(path+"/nominal_qqZZ.root")
     f_qqZZEW=TFile.Open(path+"/nominal_qqZZEW.root")
     f_ggZZ=TFile.Open(path+"/nominal_ggZZ.root")

     f_ggH=TFile.Open(path+"/nominal_ggF.root")
     f_VBFH=TFile.Open(path+"/nominal_VBF.root")

     h_qqZZ_all = f_qqZZ.Get("yield_all")
     h_qqZZEW_all = f_qqZZEW.Get("yield_all")
     h_ggZZ_all = f_ggZZ.Get("yield_all")
     h_ggH_all = f_ggH.Get("yield_all")
     h_VBFH_all = f_VBFH.Get("yield_all")
     h_bkg_all = h_qqZZ_all.Clone()
     h_bkg_all.Add(h_ggZZ_all)
     h_bkg_all.Add(h_qqZZEW_all)

     for j,ch in enumerate(channels):
       hname = "yield_"+ch
       h_qqZZ = f_qqZZ.Get(hname)
       h_qqZZEW = f_qqZZEW.Get(hname)
       h_ggZZ = f_ggZZ.Get(hname)
       h_ggH  = f_ggH.Get(hname)
       h_VBFH  = f_VBFH.Get(hname)
       h_bkg = h_qqZZ.Clone()
       h_bkg.Add(h_ggZZ)
       h_bkg.Add(h_qqZZEW)
       nbins = h_qqZZ.GetNbinsX()

       for i in range(nbins):
          nsig1 = h_ggH.GetBinContent(i+1)
          nsig2 = h_VBFH.GetBinContent(i+1)
          nbkg = h_bkg.GetBinContent(i+1)
          print i, nbkg
          eff_bkg = nbkg/h_bkg_all.GetBinContent(i+1)
          eff1 = nsig1/h_ggH_all.GetBinContent(i+1)
          eff2 = nsig2/h_VBFH_all.GetBinContent(i+1)
          if nbkg > 0: 
             #signif1 = nsig1/sqrt(nbkg)
             #signif2 = nsig2/sqrt(nbkg)
             signif3 = sqrt( 2*((nsig1+nbkg)*log(1+nsig1/nbkg)-nsig1) )
             signif4 = sqrt( 2*((nsig2+nbkg)*log(1+nsig2/nbkg)-nsig2) )
          else: 
             signif3 = 0
             signif4 = 0
          hist_signif_ggH[cut][ch].SetBinContent(i+1, signif3)
          hist_signif_VBFH[cut][ch].SetBinContent(i+1, signif4)
          hist_eff_ggH[cut][ch].SetBinContent(i+1, eff1)
          hist_eff_VBFH[cut][ch].SetBinContent(i+1, eff2)
          hist_eff_bkg[cut][ch].SetBinContent(i+1, eff_bkg)
          

   tfout.Write()
