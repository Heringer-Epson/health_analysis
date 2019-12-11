import os
import numpy as np
import pandas as pd
import src.utils as utils
from src.proc_time import Process_Time

exertype_num2str = {1001:'Walking', 0:'Custom', 14001:'Swimming',
                    1002:'Running', 9002:'Yoga', 11007:'Cycling', 
                    13001:'Hiking', 15006:'Elliptical'}

def data_collector(dataset):

    try:
        fpath = os.path.join('./data/', utils.dataset2fname[dataset])
        df_raw = pd.read_csv(fpath, header=0, index_col=0, low_memory=False)
    except:
        fpath = os.path.join('../data/', utils.dataset2fname[dataset])
        df_raw = pd.read_csv(fpath, header=0, index_col=0, low_memory=False)

    if dataset == 'Sleep':
        #Rename columns for simplicity.
        newcols = {col : col.replace('com.samsung.health.sleep.', '')
                   for col in df_raw.columns}
        df_raw.rename(columns=newcols, inplace=True) 
        df = Process_Time(df_raw, 'start_time', 'end_time', 'time_offset',
                          True, 'milisec').run()
        
        df['Sleep Duration [hr]'] = np.array([
          t.days*24. + t.seconds/3600. for t in df['duration']])
        
    elif dataset == 'Exercise':
        df = Process_Time(df_raw, 'start_time', 'end_time', 'time_offset',
                          False, '%Y-%m-%d %H:%M:%S.%f').run()

        df['Exercise Duration [min]'] = np.array([
          t.days*24.*60 + t.seconds/60. for t in df['duration']]) #In minutes
        df['exercise'] = df['exercise_type'].map(exertype_num2str)

    elif dataset == 'Stress':
        df_raw.dropna(subset=['start_time', 'end_time'], inplace=True)
        df = Process_Time(df_raw, 'start_time', 'end_time', 'time_offset',
                          False, '%Y-%m-%d %H:%M:%S.%f').run()

    elif dataset == 'Step':
        df = Process_Time(df_raw, 'day_time', None, None, False, 'milisec').run()

    elif dataset == 'Heart':
        df = Process_Time(df_raw, 'start_time', 'end_time', 'time_offset',
                          False, '%Y-%m-%d %H:%M:%S.%f').run()          
        df = df.iloc[2:,:] #Do not include first two rows. They date back to 1970.

    elif dataset == 'Floors':
        df = Process_Time(df_raw, 'start_time', 'end_time', 'time_offset',
                          False, '%Y-%m-%d %H:%M:%S.%f').run() 

    elif dataset == 'Calories':
        df = Process_Time(df_raw, 'day_time', None, None, False, 'milisec').run()
        df['Active Time [hr]'] = np.array([t/3600000. for t in df['active_time']])

    elif dataset == 'Summary':
        df = Process_Time(df_raw, 'day_time', None, None, False, 'milisec').run()     
        df['Longest Idle Time [hr]'] = np.array([t/3600000. for t in df['longest_idle_time']])
        df['Longest Active Time [hr]'] = np.array([t/3600000. for t in df['longest_active_time']])

    return df
