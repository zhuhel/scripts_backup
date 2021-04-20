import os,sys
sys.path.append('/data/usr/kai/LTDB_PreProduction/LTDB_GUI_DEC2017/')
from dataproc_tmp import data_proc_tmp
from getSel import getSel
from dataproc import dataproc
from data_extract_amp import data_extract_amp
from ltdb_app_hongbin import daq_all_phase

# cmd1="python ./dataproc_tmp.py"
# cmd2="python ./getSel.py"
# cmd3="python ./dataproc.py"
# os.system(cmd1)
# os.system(cmd2)
# os.system(cmd3)


def main():
    adc_num_s1 = input("Input ADC num under test:")
    adc_num_s2 = input("Input ADC num under test again:")
    if adc_num_s1 == adc_num_s2:
        adc_num = int(adc_num_s1)

        # daq_all_phase()
        data_extract_amp()
        data_proc_tmp(adc_num)
        getSel(adc_num)  # move the data files for ADC channel whose amp > 1000
        dataproc(adc_num)
    else:
        print("error!")


if __name__ == '__main__':
    main()
