
import array, sys
import numpy as np
import numpy.fft
import datetime, time
import matplotlib.pyplot as plt

from pylab import matplotlib,figure,xlim,savefig,show,legend,plot,subplots,xlabel,ylabel,grid

data128=np.reshape(np.zeros(15*128),(-1,128))
maxpos=[16,16,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15]
peaktime0=np.zeros(320)
amp0=np.zeros(320)
crosstalk=np.zeros(320)
shift=np.zeros(15)
#if sys.argv[1]=="-ch":  CH=sys.argv[2]

group=4
ADC=54 # For crosstalk test, define the channel with input first.
aCH=4
testdir="./Group"+str(group)+"_ADC"+str(ADC)+"_Ch"+str(aCH)
inCH=int((ADC-1)*4+aCH-1)
print ("================ Input channel: ", inCH)
if ADC>=1 and ADC<17: startCH=0
elif ADC>=17 and ADC<33: startCH=64
elif ADC>=33 and ADC<49: startCH=128
elif ADC>=49 and ADC<65: startCH=192
elif ADC>=65 and ADC<81: startCH=256
endCH=startCH+64


### To get the phase shift of input channel
for ph in range(15):
    filename=testdir+"/Phase"+str(ph)+"/ADC_CH"+str(inCH+1)+".bin"

    f=open(filename,'rb')
    data=f.read()
    f.close()
    data16_orig=array.array('H', data)
    data16_orig.byteswap()

    offset=1000

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
### End of the phase shift extract
print (shift)

for CH in range(startCH,endCH):
#for CH in range(152,160):
   print ("Check=> CH", CH)
   for ph in range(15):
       filename=testdir+"/Phase"+str(ph)+"/ADC_CH"+str(CH+1)+".bin"
   
       f=open(filename,'rb')
       data=f.read()
       f.close()
       data16_orig=array.array('H', data)
       data16_orig.byteswap()
   
       offset=1000
   
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
           
       data128[ph]=np.roll(mean_val, int(shift[ph]))
       #data128[ph]=np.roll(mean_val,(maxpos[ph]-np.argmax(mean_val)))
   
   dataall=np.reshape(np.transpose(data128),(-1,1))
   
   ### calculation of peaking time and amplitude for CH0
   baseline0=np.mean(dataall[0:100])
   maxvalue0=np.max(dataall)
   endpoint0=np.argmax(dataall)
   for i in range(1920):
      if dataall[i] >= baseline0+0.05*(maxvalue0-baseline0):
         startpoint0=i
         break
   peaktime0[CH] = (endpoint0-startpoint0)*24.95/15
   amp0[CH] = (maxvalue0-baseline0)

   matplotlib.style.use('ggplot')
   
   if CH<-1:
      f=figure(CH)
      ax = f.add_subplot(111)
      #if CH%16>=0 and CH%16<4:   ax.plot(dataall, 'b')
      #if CH%16>=4 and CH%16<8:   ax.plot(dataall, 'g')
      #if CH%16>=8 and CH%16<12:  ax.plot(dataall, 'r')
      #if CH%16>=12 and CH%16<16: ax.plot(dataall, 'y')
      ax.plot(dataall, 'b')
      ax.set_ylabel('ADC data')
      ax.set_xlabel('Samples/600MHz')
      #if CH!= 20: ax.set_ylim([530,550])
      ax.set_xlim([0,128*15])
      #f.savefig("crosstalk_"+str(CH)+".png", format='png')
  

for CH in range(startCH,endCH):
#for CH in range(152,160):
   crosstalk[CH] = amp0[CH]/amp0[inCH]*100

   '''
   ## plot fft 
   figure(100+CH)
   data3=[]
   for i in range(1000,1500):
       data3.extend(dataall[i])
   
   data3_fft = np.fft.fft(data3)
   data3_fft = data3_fft[range(250)]
   freq=np.fft.fftfreq(500,1.667e-3)
   freq=freq[range(250)]
   if CH%16>=0 and CH%16<4:   plt.plot(freq[2:250],abs(data3_fft[2:250]),'b')
   if CH%16>=4 and CH%16<8:   plt.plot(freq[2:250],abs(data3_fft[2:250]),'g')
   if CH%16>=8 and CH%16<12:  plt.plot(freq[2:250],abs(data3_fft[2:250]),'r')
   if CH%16>=12 and CH%16<16: plt.plot(freq[2:250],abs(data3_fft[2:250]),'y')
   xlabel('f (MHz)')
   ylabel('ADC data')
   xlim([0,300])
   #plt.savefig("fft_"+str(CH)+".png", format='png')
   
   matplotlib.style.use('ggplot')
   f=figure(1000+int(CH))
   ax = f.add_subplot(111)
   if CH%16>=0 and CH%16<4:   ax.plot( dataall[1400:1500],'b')
   if CH%16>=4 and CH%16<8:   ax.plot( dataall[1400:1500],'g')
   if CH%16>=8 and CH%16<12:  ax.plot( dataall[1400:1500],'r')
   if CH%16>=12 and CH%16<16: ax.plot( dataall[1400:1500],'y')
   #ax.legend(loc=0,fontsize=12)
   ax.set_ylabel('ADC data')
   ax.set_xlabel('Samples/720MHz')
   ax.set_xlim([0,100])
   f.savefig("baseline_"+str(CH)+".png", format='png')
   #ax[2].set_ylim([-50,3000])
   '''
   ## for crosstalk of 320 channels
   matplotlib.style.use('ggplot')
   f=figure(100)
   ax = f.add_subplot(211)
   if CH!=inCH: ax.plot(CH, crosstalk[CH], '.g')
   #else: ax.semilogy(CH, crosstalk[CH], '.g')
   ax.set_ylabel('Percentage of crosstalk (%)')
   ax.set_xlabel('Channel Number / 600MHz')
   ax.set_xlim([startCH,endCH])
   #ax.set_ylim([10e-4,10e3])
   
for i in range(320):
   if crosstalk[319-i]==0:
      crosstalk=np.delete(crosstalk, 319-i)

print (crosstalk)
min_ct = np.min(crosstalk)
max_ct = np.max(crosstalk)
mean_ct = np.mean(crosstalk)
allCH=endCH-startCH
print ([min_ct, max_ct, (mean_ct*allCH-100.)/(allCH-1.)])

show()
