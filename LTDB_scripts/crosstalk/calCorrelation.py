
import array, sys
import numpy as np
import numpy.fft
import datetime, time
import matplotlib.pyplot as plt

from pylab import matplotlib,figure,xlim,savefig,show,legend,plot,subplots,xlabel,ylabel,grid

data128_CH0=np.reshape(np.zeros(15*128),(-1,128))
data128_CH1=np.reshape(np.zeros(15*128),(-1,128))
maxpos=[15,15,15,15,15,15,15,15,15,15,15,15,15,15,14,14,14,14]

CH0 = 2
#CH1 = 3
#for CH1 in range(8):
for CH1 in range(4):
      print ("Check=> CH", CH0, CH1)
      for ph in range(15):
          filename0="./phase"+str(ph)+"/ADC_CH"+str(CH0+1)+".bin"
          filename1="./phase"+str(ph)+"/ADC_CH"+str(CH1+1)+".bin"
      
          data0=open(filename0,'rb').read(50000)
          data1=open(filename1,'rb').read(50000)
          data16_orig0=array.array('H', data0)
          data16_orig0.byteswap()
          data16_orig1=array.array('H', data1)
          data16_orig1.byteswap()
      
          offset=1000
          samples=20480
          data_CH0=data16_orig0[offset:offset+samples]
          data_CH0=np.mod(data_CH0,2**12)
          data_channel0= np.transpose(np.reshape(data_CH0,(-1,128)))
          data_CH1=data16_orig1[offset:offset+samples]
          data_CH1=np.mod(data_CH1,2**12)
          data_channel1= np.transpose(np.reshape(data_CH1,(-1,128)))
      
          mean_val0=np.zeros(128)
          mean_val1=np.zeros(128)
      
          for i in range(128):
              mean_val0[i]=np.mean(data_channel0[i])	
      
          for i in range(128):
              for j in range(int(samples/128)):
                  if abs(data_channel0[i][j]-mean_val0[i])>8:
                      data_channel0[i][j]=mean_val0[i]
      
          for i in range(128):
              mean_val0[i]=np.mean(data_channel0[i]) 
              
          for i in range(128):
              mean_val1[i]=np.mean(data_channel1[i])	
      
          for i in range(128):
              for j in range(int(samples/128)):
                  if abs(data_channel1[i][j]-mean_val1[i])>8:
                      data_channel1[i][j]=mean_val1[i]
      
          for i in range(128):
              mean_val1[i]=np.mean(data_channel1[i]) 
              
          shift=maxpos[ph]-np.argmax(mean_val0)   
         
          data128_CH0[ph]=np.roll(mean_val0,shift)        
          data128_CH1[ph]=np.roll(mean_val1,shift)        
      
      dataall0=np.reshape(np.transpose(data128_CH0),(-1,1))
      dataall1=np.reshape(np.transpose(data128_CH1),(-1,1))
      
      datanew0=[]
      datanew1=[]
      for i in range(1000,1500):
          datanew0.extend(dataall0[i])
          datanew1.extend(dataall1[i])
      
      Cov = np.cov(datanew0,datanew1)
      #std0 = np.std(dataall0[1000:1500])
      #std1 = np.std(dataall1[1000:1500])
      std0 = np.std(datanew0)
      std1 = np.std(datanew1)
      Corr = np.corrcoef(datanew0,datanew1)
      
      print (Cov[0][1])
      print (Corr[0][1])
      print (std0)
      print (std1)
