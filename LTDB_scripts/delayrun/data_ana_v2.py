import array
import numpy as np
import sys
import datetime, time
from scipy import stats
import seaborn as sns
from pylab import matplotlib,figure,xlim,savefig,show,legend,plot,subplots,xlabel,ylabel,grid
import pylab as plt

filename=sys.argv[1]

#CHA=1



### Set file name
print filename

data=open(filename,'rb').read()

### change the start sample position and how many samples to analyze

data16_orig=array.array('H', data)
data16_orig.byteswap()
#data16_orig=data16_orig1.byteswap()

np.set_printoptions(formatter={'int':lambda x:'0x{0:04x}'.format(x)})

print "Exact the channel data"

offset=1000


filesize=np.size(data16_orig)
samples=int(filesize)-offset
#samples=20000

start_pt= offset
stop_pt= start_pt+samples

data16_ch=data16_orig[offset:offset+samples]

## process 1 channels

data_ch = np.mod(data16_ch,2**12)

print "Calculate the diff values"
delta_ch=np.diff(data_ch)

## Analyze 
print "start to find spikes..."

mean_vec=np.mean(data_ch)
spike_number=0
for i in range(samples):
   if abs(data_ch[samples-1-i]- mean_vec) > 8:
      #data_ch_A=np.delete(data_ch_A,samples-1-i)
      spike_number=spike_number+1

'''
##============== for ef0 only ===============
spike_time=np.zeros(550)
spike_point=np.zeros(550)
spike_number_A=0
nlarge=0
for i in range(samples):
    if abs(data_ch_A[i]-3824)>15:
       spike_point[spike_number_A]=i
       if spike_number_A==0:
          spike_time[spike_number_A]=i
       if spike_number_A!=0:
          spike_time[spike_number_A]=i-spike_point[spike_number_A-1]       
  #     if spike_time[spike_number_A]<2:
  #        spike_time[spike_number_A]=-1
       spike_number_A=spike_number_A+1
'''
print "done"
print "------------------------"
print ("Number of spikes: %d" %(spike_number))
print "------------------------"
print ("Total number of samples: %d" %(samples))
print "------------------------"

print "begin plotting..."

f=figure(0)
ax = f.add_subplot(111)
ax.plot(data_ch[0:10000], 'r')
ax.set_ylabel('ADC data')
ax.set_xlabel('Samples')

### TODO: plot fft

'''
figure(1)
n=10000
data_fft = np.fft.fft(data_ch_A)
data_fft = data_fft[range(n/2)]
freq=np.fft.fftfreq(n,0.025)
freq=freq[range(n/2)]
#print(freq)
plt.plot(freq[1:n/2],abs(data_fft[1:n/2]))
xlabel('f (MHz)')
ylabel('ADC data')



matplotlib.style.use('ggplot')
f, ax = subplots(2,1,sharex=True)
ax[0].plot(data_ch_A[0:1000000],'.r',label='Data_CH1')
ax[1].plot(delta_ch_A[0:1000000],'.g',label='Delta_CH1')
ax[0].legend(loc=0,fontsize=12)
ax[1].legend(loc=0,fontsize=12)

ax[0].set_ylabel('ADC data')
ax[1].set_ylabel('Delta data')

ax[1].set_xlabel('Samples')
#ax.savefig("histo_points.pdf", format='pdf')

## ================== for efo partern calculate the interval of spikes ============
figure(1)
#sns.distplot(spike_time, bins=20, kde=False);
plt.hist(spike_time, bins=20, log=True);

plt.xlabel("Time of interval between two spikes [sample]")
plt.ylabel("Number of spikes")
#plt.semilogy()

#plt.title(r'Histogram of Pedestal: $\mu=%f$, $\sigma=%f$' % (mu, sigma))
#plt.text(max_mean-0.1*(max_mean-min_mean), 1.1/(max_mean-min_mean), '$\mu=$' + str(mu))
plt.text(2500000, 100, 'Total number of spikes: 545')
plt.savefig("spike_time.png", format='pdf')
'''
show()

