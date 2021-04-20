#!/usr/bin/env python

import os
import sys
import numpy as np

#os.system("rm test.bin")


def link_map_gen():
    ##The real ADC number defined by G#L#A#'s position in new mapping
    maparray=np.zeros(40)
    maparray[0:10]=[36,37,16,17,35,39,38,19,14,13]
    maparray[10:20]=[18,30,12,15,10,31,9,32,33,34]
    maparray[20:30]=[23,11,24,25,5,7,28,26,6,8]
    maparray[30:40]=[27,0,29,22,2,1,20,21,4,3]
    #print(maparray)
    return maparray

def adc_swap_gen():
    swaparray=np.zeros(40)
    swaparray[0:10] =[0,0,0,0,1,0,0,0,0,0]
    swaparray[10:20]=[0,1,0,0,0,0,1,1,1,1]
    swaparray[20:30]=[1,0,0,0,1,0,0,1,0,1]
    swaparray[30:40]=[1,1,1,1,0,0,0,0,0,0]
    return swaparray

def adc_map_switch(phase):

    maparray=link_map_gen()
    swaparray=adc_swap_gen()
    for i in range(40):
        if swaparray[i]==0:
            for j in range(8):
                cmd="mv ADC_CH"+ str(int(8*maparray[int(i)]+j+1))+".bin ./Phase"+str(phase)+"/ADC_CH"+str(int(i*8+j+1))+".bin"
                os.system(cmd)
        else:
            cmd="mv ADC_CH"+ str(int(8*maparray[int(i)]+1))+".bin ./Phase"+str(phase)+"/ADC_CH"+str(int(i*8+4+1))+".bin"
            os.system(cmd)
            cmd="mv ADC_CH"+ str(int(8*maparray[int(i)]+2))+".bin ./Phase"+str(phase)+"/ADC_CH"+str(int(i*8+5+1))+".bin"
            os.system(cmd)
            cmd="mv ADC_CH"+ str(int(8*maparray[int(i)]+3))+".bin ./Phase"+str(phase)+"/ADC_CH"+str(int(i*8+6+1))+".bin"
            os.system(cmd)
            cmd="mv ADC_CH"+ str(int(8*maparray[int(i)]+4))+".bin ./Phase"+str(phase)+"/ADC_CH"+str(int(i*8+7+1))+".bin"
            os.system(cmd)
            cmd="mv ADC_CH"+ str(int(8*maparray[int(i)]+5))+".bin ./Phase"+str(phase)+"/ADC_CH"+str(int(i*8+0+1))+".bin"
            os.system(cmd)
            cmd="mv ADC_CH"+ str(int(8*maparray[int(i)]+6))+".bin ./Phase"+str(phase)+"/ADC_CH"+str(int(i*8+1+1))+".bin"
            os.system(cmd)
            cmd="mv ADC_CH"+ str(int(8*maparray[int(i)]+7))+".bin ./Phase"+str(phase)+"/ADC_CH"+str(int(i*8+2+1))+".bin"
            os.system(cmd)
            cmd="mv ADC_CH"+ str(int(8*maparray[int(i)]+8))+".bin ./Phase"+str(phase)+"/ADC_CH"+str(int(i*8+3+1))+".bin"
            os.system(cmd)
    #os.system("mv ADC_CH"+str ./data/")


def data_extract_amp():
    for phase in range(15):
        print("!!!Extracting Phase:", phase)
        os.system("mkdir Phase" + str(phase))
        filename = '/data/usr/kai/LTDB_PreProduction/LTDB_GUI_DEC2017/data/tmpdata_320ch_ph' + str(phase) + '.dat'
        # merge the 320 ADC channels
        cmd = "merge_calib -m 3" + " -f " + filename
        os.system(cmd)
        adc_map_switch(phase)
        # os.system("mv ADC_CH* Phase"+str(phase))
    print("======== Move extracted file to the target: file/ ========")
    os.system("rm -r file/*")
    os.system("mv Phase* file")


if __name__ == '__main__':

    for phase in range(15):
        print ("!!!Extracting Phase:", phase)
        os.system("mkdir Phase"+str(phase))
        filename='/data/usr/kai/LTDB_PreProduction/LTDB_GUI_DEC2017/data/tmpdata_320ch_ph'+str(phase)+'.dat'
        # merge the 320 ADC channels
        cmd="merge_calib -m 3"+" -f "+ filename
        os.system(cmd)
        adc_map_switch(phase)
        #os.system("mv ADC_CH* Phase"+str(phase))
    
    print ("======== Move extracted file to the target: file/ ========")
    os.system("rm -r file/*")
    os.system("mv Phase* file")
