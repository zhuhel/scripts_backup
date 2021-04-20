#!/usr/bin/env python

###############################
# Heling Zhu, Apr. 2018 @BNL
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


def getHist(tr='', cate='', mhist1="", **kw):
  cut = "&& ((n_jets >= 2 && DNN_VBF < 0.8 && DNN_ggF_no_KD > 0.5) || (n_jets < 2 && DNN_ggF_no_KD > 0.5))"
  if cate=="ggF_2e2mu": cut += "&& (event_type==3||event_type==2)" 
  elif cate=="ggF_4e":  cut += "&& event_type==1"
  elif cate=="ggF_4mu": cut += "&& event_type==0"

  hname = "%s_%s" % (mhist1, cate)
  #hist=TH1F(hname, hname, 1000, 0, 1000)
  #hist=TH1F(hname, hname, 600, -3, 3)
  hist=TH1F(hname, hname, 1000, 50, 150)
  hist.Sumw2()
  tr.Draw("%s>>%s" %(mhist1, hname), "weight*(weight!=0. %s)" %(cut))
  return hist

###################
## Main Function ##
###################
if __name__ == "__main__":

  inputh ="/afs/cern.ch/work/r/rwoelker/public/2019-11-08_prod_v21_ggF_DNN/mc16a/mc16_13TeV.303327.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_ZZ_llll_c10_m0600_dnn.root"
  #inputh ="/afs/cern.ch/work/r/rwoelker/public/2019-11-08_prod_v21_ggF_DNN/mc16a/mc16_13TeV.341278.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_ggH600NW_ZZ4lep_dnn.root"
  trname='tree_incl_all'
  #mhist1='m4l_constrained_HM'
  mhist1='mZ1_constrained'

  outfile="hist_RS_G_m0600.root"
  #outfile="hist_ggH600NW.root"
  resultRoot=TFile(outfile, 'UPDATE')

  tfin=TFile.Open(inputh)
  tr=tfin.Get(trname)
  h1=getHist(tr, "ggF_2e2mu", mhist1)
  h2=getHist(tr, "ggF_4e", mhist1)
  h3=getHist(tr, "ggF_4mu", mhist1)

  h1.SetDirectory(resultRoot)
  h2.SetDirectory(resultRoot)
  h3.SetDirectory(resultRoot)
  resultRoot.Write()

