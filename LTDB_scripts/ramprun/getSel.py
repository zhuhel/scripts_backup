#!/usr/bin/env python

import array, sys, os
import numpy as np
import datetime, time

from pylab import matplotlib,figure,xlim,savefig,show,legend,plot,subplots,xlabel,ylabel,grid,text

def fileSel(filename):

   data=open(filename,'rb').read(50000)
   data16_orig=array.array('H', data)
   data16_orig.byteswap()

   offset=0
   filesize=np.size(data16_orig)
   #samples=int(filesize)-offset
   samples=20480
   data16=data16_orig[offset:offset+samples]

   data16=np.mod(data16,2**12)
   data_channel= np.transpose(np.reshape(data16,(-1,128)))
   mean_val=np.zeros(128)

   for i in range(128):
       mean_val[i]=np.mean(data_channel[i])
   for i in range(128):
       for j in range(int(samples/128)):
           if abs(data_channel[i][j]-mean_val[i])>8:
               data_channel[i][j]=mean_val[i]
   for i in range(128):
       mean_val[i]=np.mean(data_channel[i])

   shift=15-np.argmax(mean_val)
   data128=np.roll(mean_val,shift)

   amp=data128[15]-data128[0]

   return amp


def getSel(adc_num):
    # for i in range(80):

    ch_list = list(range((adc_num - 1) * 4, adc_num * 4))
    for ap in range(16):
        # for CH in range(320):
        for CH in ch_list:
            # if CH==166: continue
            filename = "./file/Amp" + str(ap) + "/ADC_CH" + str(CH + 1) + ".bin"
            amp = fileSel(filename)
            print("Check=> Amp:", amp, "  CH:", CH + 1, "  ####amp:", ap)

            targetf = "./goodfile/Amp" + str(ap)
            if not os.path.exists(targetf): os.system("mkdir " + targetf)

            cmd = 'cp ' + filename + ' ' + targetf
            if (amp > 100):
                os.system(cmd)
                print("!!! Move ", filename)


def main():
    adc_num_s = input("enter ADC number:")
    adc_num = int(adc_num_s)
    getSel(adc_num)


if __name__ == '__main__':
    main()


