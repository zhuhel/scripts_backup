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


def getNum(tr='', mhist1='', cut='', **kw):

  hist=TH1F("tmp", "tmp", 5000, 0, 5000)
  tr.Draw("%s>>tmp" %(mhist1), "weight*(%s)" %(cut))
  nNum = hist.Integral()

  return nNum

###################
## Main Function ##
###################
if __name__ == "__main__":

  input_gg = "/afs/cern.ch/work/r/rwoelker/public/2019-08-13_prod_v21_dnn/mc16e/mc16_13TeV.345709.Sherpa_222_NNPDF30NNLO_ggllllNoHiggs_130M4l_dnn.root"
  input_qq1 = "/afs/cern.ch/work/r/rwoelker/public/2019-08-13_prod_v21_dnn/mc16e/mc16_13TeV.364250.Sherpa_222_NNPDF30NNLO_llll_dnn.root"
  input_qq2 = "/afs/cern.ch/work/r/rwoelker/public/2019-08-13_prod_v21_dnn/mc16e/mc16_13TeV.364251.Sherpa_222_NNPDF30NNLO_llll_m4l100_300_filt100_150_dnn.root"
  input_qq3 = "/afs/cern.ch/work/r/rwoelker/public/2019-08-13_prod_v21_dnn/mc16e/mc16_13TeV.364252.Sherpa_222_NNPDF30NNLO_llll_m4l300_dnn.root"
  input_ew = "/afs/cern.ch/work/r/rwoelker/public/2019-08-13_prod_v21_dnn/mc16e/mc16_13TeV.364283.Sherpa_222_NNPDF30NNLO_lllljj_EW6_dnn.root"

  input_s1 = "/afs/cern.ch/work/r/rwoelker/public/2019-08-13_prod_v21_dnn//mc16e/mc16_13TeV.341294.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_VBFH300NW_ZZ4lep_dnn.root"
  input_s2 = "/afs/cern.ch/work/r/rwoelker/public/2019-08-13_prod_v21_dnn//mc16e/mc16_13TeV.341296.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_VBFH500NW_ZZ4lep_dnn.root"
  input_s3=  "/afs/cern.ch/work/r/rwoelker/public/2019-08-13_prod_v21_dnn//mc16e/mc16_13TeV.341298.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_VBFH700NW_ZZ4lep_dnn.root"
  input_s4 = "/afs/cern.ch/work/r/rwoelker/public/2019-08-13_prod_v21_dnn//mc16e/mc16_13TeV.341300.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_VBFH900NW_ZZ4lep_dnn.root"
  input_s5 = "/afs/cern.ch/work/r/rwoelker/public/2019-08-13_prod_v21_dnn//mc16e/mc16_13TeV.341303.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_VBFH1400NW_ZZ4lep_dnn.root"
  input_s6 = "/afs/cern.ch/work/r/rwoelker/public/2019-08-13_prod_v21_dnn//mc16e/mc16_13TeV.341305.PowhegPythia8EvtGen_CT10_AZNLOCTEQ6L1_VBFH1800NW_ZZ4lep_dnn.root"

  bkgs=[input_gg, input_qq1, input_qq2, input_qq3, input_ew]
  sigs=[input_s1, input_s2, input_s3, input_s4, input_s5, input_s6]
  #DNNs=['DNN', 'DNN_no_mjj', 'DNN_no_detajj', 'DNN_no_ptjj', 'DNN_no_eta_zepp', 'DNN_no_min_dr_jz', 'DNN_no_m4l', 'DNN_no_lep1', 'DNN_no_lep2', 'DNN_no_lep3', 'DNN_no_lep4', 'DNN_no_j1', 'DNN_no_j2', 'DNN_no_j3']
  DNNs=['DNN_nominal', 'DNN_no_detajj_j3']
  trname='tree_incl_all'
  mhist1='m4l_constrained_HM'
  mass = 1400
  nbins=50

  outfile="hist_significance_%s.root" %(str(mass))
  resultRoot=TFile(outfile, 'recreate')

  hist_dict={}
  for dnn in DNNs:
    print "Looking at => ", dnn
    hist = TH1F(dnn, dnn, nbins, 0, 1)
    hist.SetDirectory(resultRoot)
    hist_dict[dnn] = hist
    for i in range(nbins):
      dcut = i*(1./nbins)
      cut='%s>%s && %s>%f && %s<%f && n_jets>=2' %(dnn, dcut, mhist1, (mass-0.02*mass), mhist1, (mass+0.02*mass) )
      #print "Apply cut: ", cut
      nbkg = 0.
      for bkg in bkgs:
        tfin = TFile.Open(bkg)
        tr = tfin.Get(trname)
        nbkg = nbkg + getNum(tr, mhist1, cut)
        #print "Reading bkg.   => ", bkg, "Total yield: ", nbkg
        tfin.Close()

      nsig = 0.
      for sig in sigs:
        tfin = TFile.Open(sig)
        tr = tfin.Get(trname)
        nsig = nsig + getNum(tr, mhist1, cut)
        #print "Reading signal => ", sig, "Total yield: ", nsig
        tfin.Close()

      if nbkg > 0.:  m_sign = sqrt( 2*((nsig+nbkg)*log(1+nsig/nbkg)-nsig) )
      else: m_sign = 0.
      print "Cut at %f, Nsig = %f, Nbkg = %f, significance = %f" %(dcut, nsig, nbkg, m_sign)

      hist_dict[dnn].SetBinContent(i+1, m_sign)
    #hist_dict[dnn].Write()

  resultRoot.Write()
