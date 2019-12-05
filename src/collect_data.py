import os
import pandas as pd
import src.utils as utils
from src.proc_time import Process_Time

def data_collector(dataset):
    if dataset == 'Sleep-1':

        fpath = os.path.join('./data/', utils.dataset2fname[dataset])
        df_raw = pd.read_csv(fpath, header=0, index_col=0, low_memory=False)

        #Rename columns for simplicity.
        newcols = {col : col.replace('com.samsung.health.sleep.', '')
                   for col in df_raw.columns}
        df_raw.rename(columns=newcols, inplace=True) 
        df = Process_Time(df_raw, 'start_time', 'end_time', 'time_offset',
                          True, 'milisec').run()
        
    return df
