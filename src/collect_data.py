import os
import pandas as pd
import src.utils as utils
from src.proc_time import Process_Time

exertype_num2str = {1001:'Walking', 0:'Custom', 14001:'Swimming',
                    1002:'Running', 9002:'Yoga', 11007:'Cycling', 
                    13001:'Hiking', 15006:'Elliptical'}

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
        df.rename(columns={'duration':'Sleep_duration'}, inplace=True)

    elif dataset == 'Exercise':
        fpath = os.path.join('./data/', utils.dataset2fname[dataset])
        df_raw = pd.read_csv(fpath, header=0, index_col=0, low_memory=False)

        df = Process_Time(df_raw, 'start_time', 'end_time', 'time_offset',
                          False, '%Y-%m-%d %H:%M:%S.%f').run()

        #Additional column. Type of exercise.
        df['exercise'] = df['exercise_type'].map(exertype_num2str)

    return df
