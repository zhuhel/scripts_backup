#!/usr/bin/env python

import os, sys
import operator

from ROOT import TFile,TTree,TChain, Double, TBranch, TH1F, TH2F
import ROOT as r
from array import array
import math

class DileptonType:
  NA = 0 
  _ee = 1
  _mm = 2 
  _em = 3


def stdCal(hist, mean=-1):
    sq_sum = 0
    nWts = hist.GetNbinsX()
    for iwt in range(nWts):
      sq_sum = sq_sum + math.pow( (hist.GetBinContent(iwt+1)-mean), 2)
    std = math.sqrt( sq_sum/nWts )
    return std


def fillHist(input="", output="", outdir=""):
  trname="truth"

  tfin=TFile.Open(input)
  tr=tfin.Get(trname)

  logout=open("%s/eventInfo_%s.txt" % (outdir, output), 'a+')

  tfout=TFile.Open("%s/hist_%s.root" % (outdir, output), 'RECREATE')

  #chs=["4mu", "4e", "2e2mu", "incl"]
  cuts=["All", "VBS"]

  ## event loop
  nEntries=tr.GetEntries()
  print 'Info=> Total number of events: ', nEntries
  nPassed=0

  pass_cuts={}
  dict_cut_count={}

  ##----------------- Define histograms -------------------
  nWts=101
  hist_dict_pdf_weights={}
  hist_dict_extpdf_weights={}
  hist_dict_scale_weights={}
  for ic, cut in enumerate(cuts):
      hname="pdf_weights_%s" % (cut)
      hist=TH1F(hname, hname, nWts, 0, nWts)
      hist.SetDirectory(tfout)
      hist.Sumw2()

      hist_dict_pdf_weights[cut]=hist

      hname="extpdf_weights_%s" % (cut)
      hist=TH1F(hname, hname, 3, 0, 3)
      hist.SetDirectory(tfout)
      hist.Sumw2()

      hist_dict_extpdf_weights[cut]=hist

      hname="scale_weights_%s" % (cut)
      hist=TH1F(hname, hname, 13, 0, 13)
      hist.SetDirectory(tfout)
      hist.Sumw2()

      hist_dict_scale_weights[cut]=hist

  tr.SetBranchStatus("*",0)
  tr.SetBranchStatus("mc_weight",1)
  tr.SetBranchStatus("pass_VBS",1)
  tr.SetBranchStatus("pdf_weights",1)

  for i in range(nEntries):
  #for tr in Tree:
    #if i>1000: break
    tr.GetEntry(i)
    if i%10000==0: print 'Info=> Processed events: ', i

    nLep=4

    nPassed+=1

    wt=tr.mc_weight
    
    ## apply some cuts
    for ic, cut in enumerate(cuts):
      if cut not in dict_cut_count: dict_cut_count[cut]=0
      pass_cuts[cut]=0 ## reset
    pass_cuts["All"]=1
    if tr.pass_VBS==1: pass_cuts["VBS"]=1

    for ic, cut in enumerate(cuts):
      if pass_cuts[cut]==0: continue
      dict_cut_count[cut] += 1.

      for iwt in range(nWts):
         #hist_dict_pdf_weights[cut].Fill(iwt, wt*tr.pdf_weights.at(iwt)*12.196/151597.89)
         hist_dict_pdf_weights[cut].Fill(iwt, wt*tr.pdf_weights.at(iwt)*1363.9/411962.56)
      for j in range(101,103):
         #hist_dict_extpdf_weights[cut].Fill(j-100, wt*tr.pdf_weights.at(j)*12.196/151597.89)
         hist_dict_extpdf_weights[cut].Fill(j-100, wt*tr.pdf_weights.at(j)*1363.9/411962.56)

      #hist_dict_scale_weights[cut].SetBinContent(1, wt*tr.pdf_weights.at(1)*12.196/151597.89 )
      #hist_dict_extpdf_weights[cut].Fill(0, wt*tr.pdf_weights.at(0)*12.196/151597.89 )
      hist_dict_extpdf_weights[cut].Fill(0, wt*tr.pdf_weights.at(0)*1363.9/411962.56 )

  ## calculate the std of each histograms
  
  for ic, cut in enumerate(cuts):
    mean = hist_dict_pdf_weights[cut].GetBinContent(1)
    if mean==0:
      print "WARNNING: no events left in cut %s" %(cut)
      continue
    std = stdCal(hist_dict_pdf_weights[cut], mean) 
    std_ext = stdCal(hist_dict_extpdf_weights[cut], mean)
    #std_scale = stdCal(hist_dict_scale_weights[cut], mean)
    
    oline="==================== cut\tInternal pdf weights\tExternal pdf weights =============="
    logout.write("%s\n" % oline)
    print oline
    oline="Standrad derivation of %s:\t%2.4f\t%2.4f" %(cut, std, std_ext)
    logout.write("%s\n" % oline)
    print oline
    oline="Nominal             of %s:\t%2.4f\t%2.4f" %(cut, mean, mean)
    logout.write("%s\n" % oline)
    print oline
    oline="Relative error      of %s:\t%2.4f\t%2.4f" %(cut, std/mean, std_ext/mean)
    logout.write("%s\n" % oline)
    print oline
  
  #print "nominal xsec: ", hist_dict_pdf_weights['All'].GetBinContent(1), hist_dict_pdf_weights['2lep'].GetBinContent(1)
      
  ## fill hist
  tfout.cd()
  for ic, cut in enumerate(cuts):
      hist_dict_pdf_weights[cut].Write()
      hist_dict_extpdf_weights[cut].Write()
      hist_dict_scale_weights[cut].Write()

  tfout.Close()
  tfin.Close()

  logout.write("%s\n" % input)
  oline="\n ===== info ===== "
  logout.write("%s\n" % oline)
  print oline
  oline=" nTotoal = %d "  % (nEntries)
  logout.write("%s\n" % oline)
  print oline
  for ic, cut in enumerate(cuts):
    oline="   %10s : %-10d" % (cut, dict_cut_count[cut])
    print oline
    logout.write("%s\n" % oline)

  logout.write("=============\n")
  logout.close()

def read_cutflow(tfile='', output='', outdir=''):
    """Read VBS cutflow histogram and print"""
    f_in = TFile(tfile)
    logout=open("%s/eventInfo_%s.txt" % (outdir, output), 'a+')

    oline = "cut              \t\t cross section \t\t ratio"
    logout.write("%s" % oline)
    print oline


    h_cutflow_pre = f_in.Get('Cutflow_incl_Incl')
    Ntotal = h_cutflow_pre.GetBinContent(1)
    print "Number of total raw events = ", Ntotal
    print_histo(h_cutflow_pre, Ntotal, logout)

    h_cutflow_2e2mu = f_in.Get('Cutflow_incl_2e2mu')
    h_cutflow_4mu = f_in.Get('Cutflow_incl_4mu')
    h_cutflow_4e = f_in.Get('Cutflow_incl_4e')
    print_histo(h_cutflow_2e2mu, Ntotal, logout)
    print_histo(h_cutflow_4mu, Ntotal, logout)
    print_histo(h_cutflow_4e, Ntotal, logout)

    logout.write("=============\n")
    logout.close()

def print_histo(histo, Ntotal, logout):
    h_name = histo.GetName()
    oline='\n{0:=^50}'.format(h_name)
    logout.write("%s\n" % oline)
    print oline

    
    cutsName=["Total           ", "4leptons        ", "lepton pT       ", "60GeV<MZs<120GeV", "Mll>10GeV       ", "2jets           ", "TagJets         ", "VBFsel          "]
    #for i in range(histo.GetNbinsX()+1):
    for i, cut in enumerate(cutsName):
        number = histo.GetBinContent(i+1)*12.196/Ntotal*3000
        error  = histo.GetBinError(i+1)*12.196/Ntotal*3000
        fraction = number/12.196
        #number = histo.GetBinContent(i+1)*1363.9/Ntotal*3000
        #error  = histo.GetBinError(i+1)*1363.9/Ntotal*3000
        #fraction = number/1363.9
        oline="%s\t\t%f +/- %f" %(cut, number, error)
        logout.write("%s\n" % oline)
        print oline

    

if __name__ == "__main__":

  input="hist-xAOD.root"
  argvv=sys.argv
  if len(argvv)>=2:
    input=argvv[1]

  print input
  output=input.split('/')[-2]
  outdir="Output_hist"
  if not os.path.isdir(outdir): os.makedirs(outdir) 
  read_cutflow(input, output, outdir)
  #fillHist(input, output, outdir)
