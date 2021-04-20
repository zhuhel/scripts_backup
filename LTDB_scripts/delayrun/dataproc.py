
import array, sys
import numpy as np
import numpy.fft
import datetime, time
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from pylab import matplotlib,figure,xlim,savefig,show,legend,plot,subplots,xlabel,ylabel,grid


def dataproc(adc_num):
    data128=np.reshape(np.zeros(15*128),(-1,128))
    shift=np.zeros(15)
    #old_peaktime0=np.zeros(320)
    #old_amp0=np.zeros(320)
    peaktime0=np.zeros(320)
    amp0=np.zeros(320)
    baseline=np.zeros(320)

    ch_list = list(range((adc_num - 1) * 4, adc_num * 4))
    for CH in ch_list:
       pos_shift=50
       pos_shift_final=0
       mean_val=[[0 for col in range(128)] for row in range(15)]
       std_val=[[0 for col in range(128)] for row in range(15)]
       mean_val_shift=[[0 for col in range(128)] for row in range(15)]
       std_val_shift=[[0 for col in range(128)] for row in range(15)]
       if CH!=-1:
          print("Check=> CH", CH)
          for ph in range(15):
              filename="./goodfile/Phase"+str(14-ph)+"/ADC_CH"+str(CH+1)+".bin"

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


              for i in range(128):
                  mean_val[ph][i]=np.mean(data_channel[i])

              for i in range(128):
                  for j in range(int(samples/128)):
                      if abs(data_channel[i][j]-mean_val[ph][i])>8:
                          data_channel[i][j]=mean_val[ph][i]

              for i in range(128):
                  mean_val[ph][i]=np.mean(data_channel[i])
                  std_val[ph][i]=np.std(data_channel[i])

          ##================= self combination ===========================
          a_max_position=np.argmax(mean_val)
          a_delay_max=int(a_max_position/128)  #this delay should be consider as delay 0
          a_max=[0 for col in range(15)]
          a_small=[0 for col in range(15)]

          for m in range(0, 15):
            a_max[m]=np.argmax(mean_val[m])
            if a_max[m]!=0 and a_max[m]!=127:
              a_small[m]=min(abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]+1]),abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]-1]))
            elif a_max[m]==0:
              a_small[m]=min(abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]+1]),abs(mean_val[m][a_max[m]]-mean_val[m][127]))
            elif a_max[m]==127:
              a_small[m]=min(abs(mean_val[m][a_max[m]]-mean_val[m][0]),abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]-1]))


          a_delay_min=np.argmin(a_small)


          for m in range(0, 15):

            biggest=a_max[m]

            if a_delay_max>a_delay_min:
              if m<=a_delay_max:
                if m>a_delay_min:
                  pos_shift_final=pos_shift
                elif m==a_delay_min:
                  if a_max[m]!=0 and a_max[m]!=127:
                     isPass=abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]+1]) < abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]-1])
                  elif a_max[m]==0:
                     isPass=abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]+1]) < abs(mean_val[m][a_max[m]]-mean_val[m][127])
                  elif a_max[m]==127:
                     isPass=abs(mean_val[m][a_max[m]]-mean_val[m][0]) < abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]-1])
                  #if abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]+1]) < abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]-1]):
                  if isPass:
                    pos_shift_final=pos_shift-1
                  else:
                    pos_shift_final=pos_shift
                else:
                  pos_shift_final=pos_shift-1
              else:
                pos_shift_final=pos_shift-1
            else:
              if m>a_delay_max:
                if m<a_delay_min:
                  test=1
                  pos_shift_final=pos_shift-1
                elif m==a_delay_min:
                  #if abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]+1]) < abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]-1]):
                  if a_max[m]!=0 and a_max[m]!=127:
                     isPass=abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]+1]) < abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]-1])
                  elif a_max[m]==0:
                     isPass=abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]+1]) < abs(mean_val[m][a_max[m]]-mean_val[m][127])
                  elif a_max[m]==127:
                     isPass=abs(mean_val[m][a_max[m]]-mean_val[m][0]) < abs(mean_val[m][a_max[m]]-mean_val[m][a_max[m]-1])
                  if isPass:
                    pos_shift_final=pos_shift-1
                  else:
                    pos_shift_final=pos_shift
                else:
                  pos_shift_final=pos_shift
              else:
                pos_shift_final=pos_shift

            #print(pos_shift_final)
            #print(a_delay_max, a_delay_min, m)

            if biggest>pos_shift_final:
              mean_val_shift[m][0:pos_shift_final+1]=mean_val[m][biggest-pos_shift_final:biggest+1]
              mean_val_shift[m][pos_shift_final+1:128+pos_shift_final-biggest]=mean_val[m][biggest+1:128]
              mean_val_shift[m][128+pos_shift_final-biggest:128]=mean_val[m][0:biggest-pos_shift_final]

              std_val_shift[m][0:pos_shift_final+1]=std_val[m][biggest-pos_shift_final:biggest+1]
              std_val_shift[m][pos_shift_final+1:128+pos_shift_final-biggest]=std_val[m][biggest+1:128]
              std_val_shift[m][128+pos_shift_final-biggest:128]=std_val[m][0:biggest-pos_shift_final]
            elif biggest<pos_shift_final:
              mean_val_shift[m][pos_shift_final:128]=mean_val[m][biggest:biggest+128-pos_shift_final]
              mean_val_shift[m][0:pos_shift_final-biggest]=mean_val[m][biggest+128-pos_shift_final:128]
              mean_val_shift[m][pos_shift_final-biggest:pos_shift_final]=mean_val[m][0:biggest]
              std_val_shift[m][pos_shift_final:128]=std_val[m][biggest:biggest+128-pos_shift_final]
              std_val_shift[m][0:pos_shift_final-biggest]=std_val[m][biggest+128-pos_shift_final:128]
              std_val_shift[m][pos_shift_final-biggest:pos_shift_final]=std_val[m][0:biggest]
            else:
              mean_val_shift[m]=mean_val[m]


          data_shift=np.reshape(np.transpose(np.array([mean_val_shift[a_delay_max],mean_val_shift[np.mod(a_delay_max-1,15)],\
            mean_val_shift[np.mod(a_delay_max-2,15)],mean_val_shift[np.mod(a_delay_max-3,15)],\
            mean_val_shift[np.mod(a_delay_max-4,15)],mean_val_shift[np.mod(a_delay_max-5,15)],\
            mean_val_shift[np.mod(a_delay_max-6,15)],mean_val_shift[np.mod(a_delay_max-7,15)],\
            mean_val_shift[np.mod(a_delay_max-8,15)],mean_val_shift[np.mod(a_delay_max-9,15)],\
            mean_val_shift[np.mod(a_delay_max-10,15)],mean_val_shift[np.mod(a_delay_max-11,15)],\
            mean_val_shift[np.mod(a_delay_max-12,15)],mean_val_shift[np.mod(a_delay_max-13,15)],\
            mean_val_shift[np.mod(a_delay_max-14,15)]])),128*15)

          std_shift=np.reshape(np.transpose(np.array([std_val_shift[a_delay_max],std_val_shift[np.mod(a_delay_max-1,15)],\
            std_val_shift[np.mod(a_delay_max-2,15)],std_val_shift[np.mod(a_delay_max-3,15)],\
            std_val_shift[np.mod(a_delay_max-4,15)],std_val_shift[np.mod(a_delay_max-5,15)],\
            std_val_shift[np.mod(a_delay_max-6,15)],std_val_shift[np.mod(a_delay_max-7,15)],\
            std_val_shift[np.mod(a_delay_max-8,15)],std_val_shift[np.mod(a_delay_max-9,15)],\
            std_val_shift[np.mod(a_delay_max-10,15)],std_val_shift[np.mod(a_delay_max-11,15)],\
            std_val_shift[np.mod(a_delay_max-12,15)],std_val_shift[np.mod(a_delay_max-13,15)],\
            std_val_shift[np.mod(a_delay_max-14,15)]])),128*15)

          ## ===================================== end of combination =============================


          ### calculation of peaking time and amplitude for CH0
          baseline[CH]=np.mean(data_shift[0:500])
          baseline0=np.mean(data_shift[0:500])
          #maxvalue0=np.max(data_shift)
          maxpoint0=np.argmax(data_shift)
          xmax=[maxpoint0-1, maxpoint0, maxpoint0+1]
          P1=np.polyfit(xmax, data_shift[maxpoint0-1:maxpoint0+2],2)
          #print P1
          maxvalue0=float((4*P1[0]*P1[2]-P1[1]*P1[1])/(4*P1[0]))
          endpoint0=float(-1*P1[1]/(2*P1[0]))
          value0p5=float(baseline0+0.05*(maxvalue0-baseline0))
          for i in range(1920):
             if data_shift[i] >= value0p5:
                minpoint0=i
                break
          xmin=[minpoint0-1,minpoint0]
          P2=np.polyfit(xmin, data_shift[minpoint0-1:minpoint0+1],1)
          #print P2
          startpoint0=float((value0p5-P2[1])/P2[0])
          peaktime0[CH] = (endpoint0-startpoint0)*24.95/15
          amp0[CH] = (maxvalue0-baseline0)
          #print("Peaking time of CH%s: %f" %(CH, peaktime0))
          #print("Amplitude of CH%s: %f" %(CH, amp0))
          #print("Crosstalk of CH%s: %f" %(CH, amp0/1314.3085))

          matplotlib.style.use('ggplot')

          '''
          # plot fft 
          data3=[]
          for i in range(1000,1500):
              data3.extend(data_shift[i])
          
          data3_fft = np.fft.fft(data3)
          data3_fft = data3_fft[range(250)]
          freq=np.fft.fftfreq(500,1.667e-3)
          freq=freq[range(250)]
          plt.plot(freq[2:250],abs(data3_fft[2:250]))
          xlabel('f (MHz)')
          ylabel('ADC data')
          xlim([0,250])
          '''

          matplotlib.style.use('ggplot')
          f=figure(1000+int(CH))
          ax = f.add_subplot(111)
          ax.plot( data_shift[0:1920],'y',label='CH%i'%(int(CH%4)+1))
          ax.legend(loc=0,fontsize=12)
          ax.set_ylabel('ADC data')
          ax.set_xlabel('Samples/720MHz')
          ax.set_xlim([500,1500])
          #ax[2].set_ylim([-50,3000])
          f.savefig("./plots/wave_CH"+str(CH)+".pdf", format='pdf')

    old_peaktime0 = peaktime0
    old_amp0 = amp0
    for m in range(320):
       if peaktime0[319-m]==0:
          peaktime0=np.delete(peaktime0, 319-m)
          amp0=np.delete(amp0, 319-m)

    ave_baseline=np.mean(baseline)
    print ("The average of 320-ch baseline: ", ave_baseline)
    print (amp0)
    print (peaktime0)
    mu_pkt = np.mean(peaktime0)
    std_pkt = np.std(peaktime0)
    mu_amp = np.mean(amp0)
    std_amp = np.std(amp0)

    # ### plot amplitude
    # f=figure(3001)
    # ax = f.add_subplot(211)
    # ax.plot(amp0, 'b')
    # ax.set_ylabel('Amplitude / (ADC code)')
    # ax.set_xlabel('Channel Number')
    # ax.set_xlim([0,320])
    # f.savefig("dis_amp.pdf", format='pdf')
    #
    # ### plot peaking time
    # f=figure(3002)
    # ax = f.add_subplot(211)
    # ax.plot(peaktime0, 'b')
    # ax.set_ylabel('Peaking time (ns)')
    # ax.set_xlabel('Channel Number')
    # ax.set_xlim([0,320])
    # f.savefig("dis_peakingtime.pdf", format='pdf')
    #
    # ### calculation of std
    # figure(2001)
    # sns.distplot(peaktime0, bins=10, kde=False, fit=stats.norm);
    # plt.xlabel("Peaking time / (ns)")
    # plt.ylabel("Count")
    # plt.text(53, 0.8, '$\mu=$' + str(mu_pkt))
    # plt.text(53, 0.75, '$\sigma=$' + str(std_pkt))
    # plt.savefig("histo_peakingtime.pdf", format='pdf')
    #
    # figure(2002)
    # sns.distplot(amp0, bins=10, kde=False, fit=stats.norm);
    # plt.xlabel("Amplitude / (ADC code)")
    # plt.ylabel("Count")
    # #plt.title(r'Histogram of Pedestal: $\mu=%f$, $\sigma=%f$' % (mu, sigma))
    # plt.text(2250, 0.0055, '$\mu=$' + str(mu_amp))
    # plt.text(2250, 0.0052, '$\sigma=$' + str(std_amp))
    # plt.savefig("histo_amp.pdf", format='pdf')

    show()


def main():
    adc_num_s = input("enter ADC number:")
    adc_num = int(adc_num_s)
    dataproc(adc_num)


if __name__ == '__main__':
    main()
