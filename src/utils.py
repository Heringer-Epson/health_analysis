import numpy as np
from datetime import datetime as dt


dataset2fname = {
  'Sleep-1': 'sleep.csv',
  'Exercise': 'Exercise.csv'
}

dataset2cols = {
  'Sleep-1': ['start_hour', 'end_hour',  'Sleep_duration'],
  'Exercise': ['start_hour', 'end_hour', 'distance', 'mean_speed', 'max_heart_rate']
}

dataset2zoptions = {
  'Sleep-1': ['None', 'weekday', 'is_holiday'],
  'Exercise': ['None', 'exercise', 'weekday', 'is_holiday']
}


def trim_time(df1, df2):
    t_min = max((min(df1.Start_time_obj), min(df2.Start_time_obj)))
    t_max = min((max(df1.Start_time_obj), max(df2.Start_time_obj)))
    
    t_min = t_min.year + (t_min.month - 1.) / 12.
    t_max = t_max.year + (t_max.month - 1.) / 12.

    t_list = [int(t) for t in np.arange(t_min,t_max + 0.0001,1)]
    return t_min, t_max, t_list
    
    #df1_out = df1[((df1['Start_time_obj'] > t_min) & (df1['Start_time_obj'] < t_max))]
    #df2_out = df2[((df2['Start_time_obj'] > t_min) & (df2['Start_time_obj'] < t_max))]
    #return t_min, t_max
    #return df1_out, df2_out

def format_date(time_range):
    t_min = '{:04d}-{:02d}-01'.format(int(time_range[0] // 1),
                                      int(12.*(time_range[0] % 1)) + 1)
    t_max = '{:04d}-{:02d}-01'.format(int(time_range[1] // 1),
                                      int(12.*(time_range[1] % 1)) + 1)
    return t_min, t_max
