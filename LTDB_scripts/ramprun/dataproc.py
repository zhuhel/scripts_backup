
import array, sys
import numpy as np
import datetime, time
from scipy import stats
import seaborn as sns
import pylab as plt

from pylab import matplotlib,figure,xlim,savefig,show,legend,plot,subplots,xlabel,ylabel,grid,text

def dataproc(adc_num):
    data128=np.reshape(np.zeros(16*128),(-1,128))
    #maxpos=[15,15,15,15,15,15,15,15,15,15,15,15]
    amp=np.zeros(16)
    ch=320
    nl1=np.zeros(ch)
    nl1_raw=np.zeros(ch)
    nlall=[[0 for col in range(16)] for row in range(ch)]
    ch_list = list(range((adc_num - 1) * 4, adc_num * 4))
    #for CH in 8,9,10,11,12,13,14,15,108,109,110,111,136,137,138,139,208,209,210,211:
    # for CH in 8,9:
    for CH in ch_list:
       #if CH==166 or CH==176 or CH==177: continue
       print ("Check=>CH", CH)
       for ph in range(16):

           filename="./goodfile/Amp"+str(ph)+"/ADC_CH"+str(CH+1)+".bin"

           data=open(filename,'rb').read(50000)
           data16_orig=array.array('H', data)
           data16_orig.byteswap()
           np.set_printoptions(formatter={'int':lambda x:'0x{0:04x}'.format(x)})

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
           data128[ph]=np.roll(mean_val,shift)

           amp[ph]=data128[ph][15]-data128[ph][0]
       #print amp

       matplotlib.style.use('ggplot')
       figure(CH);
       plot(data128[0],'r')
       plot(data128[1],'g')
       plot(data128[2],'b')
       plot(data128[3],'r')
       plot(data128[4],'g')
       plot(data128[5],'b')
       plot(data128[6],'r')
       plot(data128[7],'g')
       plot(data128[8],'b')
       plot(data128[9],'r')
       plot(data128[10],'g')
       plot(data128[11],'b')
       plot(data128[12],'r')
       plot(data128[13],'g')
       plot(data128[14],'b')
       plot(data128[15],'r')
       xlabel('Samples')
       ylabel('Amplitude / (ADC code)')
       xlim([0,60])
       grid(True);
       savefig("./plots/amp_nl_CH"+str(CH)+".png", format='png')


       len_pt=12
       in_amp=[1*50/50.,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
       P1=np.polyfit(in_amp[0:len_pt], amp[0:len_pt], 1)
       in_amp=np.array(in_amp)
       yfit1=P1[0]*in_amp+P1[1];
       nl1[CH]=max(abs(yfit1[0:len_pt]-amp[0:len_pt]))/max(yfit1[0:len_pt])
       print (yfit1[0:len_pt]-amp[0:len_pt])
       nlall[CH]=(yfit1-amp)/max(yfit1[0:len_pt])


       fig1=figure(CH+100)
       ax1=fig1.add_subplot(2,1,1)
       ax1.plot(in_amp,nlall[CH]*100,'g')
       ax1.grid(True)
       ax1.set_ylabel('Non-linearity / %')
       ax1.set_ylim([-1.,1.])
       ax2=fig1.add_subplot(2,1,2)
       ax2.plot(in_amp,amp,'g*', label="CH"+str(CH))
       ax2.plot(in_amp,yfit1,'g')
       ax2.grid(True)
       ax2.legend(loc=2)
       ax2.set_xlabel('Input Amplitude')
       ax2.set_ylabel('Output Amplitude (ADC code)')

       ax1.set_xlim([0,17])
       text(7,1500,'Non-Linearity='+str(nl1[CH]*100)[0:6]+'%')
       fig1.savefig("./plots/fit_nl_CH"+str(CH)+".png", format='png')

    nl1_raw=nl1
    for i in range(320):
       if nl1[319-i]==0:
          nl1=np.delete(nl1, 319-i)


    print (nl1)
    mean_nl = np.mean(nl1)
    min_nl = np.min(nl1)
    max_nl = np.max(nl1)
    sigma_nl = np.std(nl1)
    print ([min_nl, mean_nl, max_nl])

    matplotlib.style.use('ggplot')
    figure(1000);
    plot(nl1*100,'g')
    xlabel('Channel Number')
    ylabel('Non-linearity (%)')
    xlim([0,20])
    grid(True);
    savefig("./plots/dis_nl.png", format='png')

    figure(1001)
    sns.distplot(nl1, bins=5, kde=False, fit=stats.norm);
    plt.xlabel("non-linearity")
    plt.ylabel("Count")
    #plt.title(r'Histogram of Pedestal: $\mu=%f$, $\sigma=%f$' % (mu, sigma))
    plt.text(max_nl-0.1*(max_nl-min_nl), 1.1/(max_nl-min_nl), '$\mu=$' + str(mean_nl))
    plt.text(max_nl-0.1*(max_nl-min_nl), 0.9/(max_nl-min_nl), '$\sigma=$' + str(sigma_nl))
    plt.savefig("./plots/hist_nl.png", format='png')


    show()

if __name__ == '__main__':
    dataproc(3)
