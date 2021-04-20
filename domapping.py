#!/usr/bin/env python

import sqlite3
import sys,os

sqlite_file = 'LArId.db'
inputlist = 'list.txt'

if len(sys.argv)>=2:
   sqlite_file = sys.argv[1]
if len(sys.argv)>=3:
   inputlist = sys.argv[2]

print "Looking at => Database: %s, inputlist: %s" %(sqlite_file, inputlist)

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute("SELECT distinct DET,AC,QUADRANT,SCNAME,SC_ONL_ID FROM LARID")

## 1. Make dictionary from database
dic = dict()
for row in c:
  #print row
  key = (row[0],row[1],row[2],row[3])
  if key in dic:
    dic[key].add(abs(int(row[4])))
  else:
    dic[key] = abs(int(row[4]))

## 2. get all 4 keys from files
try: mlist=open(inputlist, 'r')
except IOError:
  print "Cannot open %s, exit!" %(inputlist)
  sys.exit()

for fname in mlist:
  fname = fname.strip()
  if fname.startswith('#'): continue
  print " - Looking at => ", fname
  ### 2.1 QUADRANT and Detector side, 1 for A and -1 for C
  #fname = 'Commissioning_SIMPLEEMB_A_1.txt'
  basename = fname.split('/')[-1].replace('.txt', '')
  dirf = fname.split('/')[0]
  print "basename, dirf:", basename, dirf
  logout = open('Mapping/Mapping_'+basename+'.txt', 'w')
  try: mfile=open(fname, 'r')
  except IOError:
    print "Cannot open %s, exit!" %(fname)
    sys.exit()
  
  for line in mfile:
    line = line.strip()
    if 'QuadrantID:' not in line and 'Side:' not in line: continue
    elif 'Side:' in line:
      if 'A' in line.split(':')[-1]: ac = 1
      else: ac = -1
    else:
      quad = int(line.split(':')[-1])
      #print quad
      break
  if quad==99: quad=3 ## for data in EMF, 99 means 3
  mfile.close()
  ### 2.2 DET now is always 0 for EMB, 1 for EME, 2 for EMH
  if 'EMB' in basename: det = 0
  elif 'EME' in basename: det = 1
  elif 'EMH' in basename: det = 2
  omap = dirf+'/data/'+basename+'/mon_mapping.txt'
  print "det, ac, quad:", det, ac, quad
  ### 2.4 from file name, get mapping line by line
  try: fmap=open(omap, 'r')
  except IOError:
    print "Cannot open %s, exit!" %(omap)
    sys.exit()
  for line in fmap:
    line = line.strip()
    ch = line.split(':')[0]
    name = line.split(':')[1]
  
    ### 2.5 build the key
    if 'GND' in name:
      scid = -999
    else:
      scname = name.split('_')[1]+'_'+name.split('_')[2]
      key = (det,ac,quad,scname)
      scid = dic[key]
    ch = int(ch)
    #print key, scid, ch
    oline = '%s %s' %(scid, ch)
    logout.write("%s\n" %oline)
  logout.close()

