
import array, sys
import numpy as np
import numpy.fft
import datetime, time
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from pylab import matplotlib,figure,xlim,savefig,show,legend,plot,subplots,xlabel,ylabel,grid


def data_proc_tmp(adc_num):
    data128=np.reshape(np.zeros(16*128),(-1,128))
    maxpos=[15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15]
    shift=np.zeros(16)
    #old_peaktime0=np.zeros(64)
    #old_amp0=np.zeros(64)
    peaktime0=np.zeros(64)
    amp0=np.zeros(64)
    #if sys.argv[1]=="-l":  L=sys.argv[2]
    ch_list = list(range((adc_num - 1) * 4, adc_num * 4))
    for CH in ch_list:
    #for CH in 217,240:
          print ("Check=> CH", CH)
       #if CH==16:
          #for ph in 0,1,2,3,5,6,7,8,10,11,12,13,14:
          for ph in range(16):

              filename="./file/Amp"+str(ph)+"/ADC_CH"+str(CH)+".bin"
              #filename="./goodfile/Amp"+str(ph)+"/ADC_CH"+str(CH)+".bin"

              data=open(filename,'rb').read()
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

              shift[ph]=maxpos[ph]-np.argmax(mean_val)

              data128[ph]=np.roll(mean_val,int(shift[ph]))

              '''
              print(data128[ph])
    
              matplotlib.style.use('ggplot')
              f, ax = subplots(2,1,sharex=True)
              ax[0].plot(mean_val[0:128],'r',label='CH1 raw')
              ax[1].plot(data128[ph][0:128],'g',label='CH1 after moving')
              ax[0].legend(loc=0,fontsize=12)
              ax[1].legend(loc=0,fontsize=12)
              
              ax[0].set_ylabel('ADC data')
              ax[1].set_ylabel('ADC data')
              
              ax[1].set_xlabel('Samples')
              #ax.savefig("histo_points.pdf", format='pdf')
              show()
              '''
          dataall=np.reshape(np.transpose(data128),(-1,1))

          matplotlib.style.use('ggplot')

          '''
          # plot the waveform of each channel
          if CH>47:
             f=figure(int(CH))
             ax = f.add_subplot(111)
             ax.plot(dataall, 'b')
             ax.set_ylabel('ADC data')
             ax.set_xlabel('Samples/600MHz')
             ax.set_xlim([0,128*15])
          '''
          # test for each phase
          for i in range(16):
             f=figure(int(i))
             ax = f.add_subplot(111)
             ax.plot(data128[i], 'b')
             ax.set_ylabel('ADC data')
             ax.set_xlabel('Samples/600MHz')
             ax.set_xlim([0,128*1])
    show()
