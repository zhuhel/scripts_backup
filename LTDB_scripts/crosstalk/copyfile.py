import os

dest_dir =
os.mkdir('./')
os.system("mkdir " + targetf)
path = '/data/usr/kai/LTDB_PreProduction/LTDB_GUI_DEC2017/data/'
for ph in range(15):
    filename = path + 'tmpdata_320ch_ph%i.dat'%
    cmd = 'cp ' + filename + ' ' + targetf
    print("copy file %s to %s..."%(filename, targetf))
    os.system(cmd)