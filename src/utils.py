import numpy as np
from datetime import datetime as dt


dataset2fname = {
  'Sleep': 'sleep.csv',
  'Exercise': 'Exercise.csv',
  'Stress': 'stress.csv',
  'Step': 'step_daily_trend.csv',
  'Heart': 'heart_rate.csv',
}

dataset2cols = {
  'Sleep': ['start_hour', 'end_hour',  'Sleep Duration [hr]'],
  'Exercise': ['start_hour', 'end_hour', 'distance', 'mean_speed',
               'max_heart_rate', 'Exercise Duration [min]'],
  'Stress': ['score'],
  'Step': ['distance', 'count', 'speed', 'calorie', 'source_type'],
  'Heart': ['heart_rate', 'deviceuuid', 'start_hour', 'end_hour', 'max', 'min']
}

dataset2zoptions = {
  'Sleep': ['None', 'weekday', 'is_holiday'],
  'Exercise': ['None', 'exercise', 'weekday', 'is_holiday'],
  'Stress': ['None', 'weekday', 'is_holiday'],
  'Step': ['None', 'weekday', 'is_holiday', 'source_type'],
  'Heart': ['None', 'time_offset', 'deviceuuid', 'weekday', 'is_holiday', 'source_type'],
  
}


def trim_time(df1, df2):
    t_min = max((min(df1.Start_time_obj), min(df2.Start_time_obj)))
    t_max = min((max(df1.Start_time_obj), max(df2.Start_time_obj)))
    t_min = t_min.year + (t_min.month - 1.) / 12.
    t_max = t_max.year + (t_max.month - 1.) / 12.

    #Correct way.
    t_list = [int(t) for t in np.arange(np.ceil(t_min),np.floor(t_max) + 0.1,1)]
    return t_min, t_max, t_list

def format_date(time_range):
    t_min = '{:04d}-{:02d}-01'.format(int(time_range[0] // 1),
                                      int(12.*(time_range[0] % 1)) + 1)
    t_max = '{:04d}-{:02d}-01'.format(int(time_range[1] // 1),
                                      int(12.*(time_range[1] % 1)) + 1)
    return t_min, t_max
