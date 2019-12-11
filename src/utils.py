import numpy as np
import pandas as pd
from datetime import datetime as dt

dataset2fname = {
  'Sleep': 'sleep.csv',
  'Exercise': 'Exercise.csv',
  'Stress': 'stress.csv',
  'Step': 'step_daily_trend.csv',
  'Heart': 'heart_rate.csv',
  'Floors': 'floors_climbed.csv',
  'Calories': 'calories_burned.csv',
  'Summary': 'day_summary.csv'
}

dataset2cols = {
  'Sleep': ['start_hour', 'end_hour',  'Sleep Duration [hr]'],
  'Exercise': ['start_hour', 'end_hour', 'distance', 'mean_speed',
               'max_heart_rate', 'Exercise Duration [min]'],
  'Stress': ['score'],
  'Step': ['distance', 'count', 'speed', 'calorie', 'source_type'],
  'Heart': ['heart_rate', 'deviceuuid', 'start_hour', 'end_hour', 'max', 'min'],
  'Floors': ['floor'],
  'Calories': ['rest_calorie', 'active_calorie', 'Active Time [hr]'],
  'Summary': ['longest_idle_time', 'longest_active_time', 'distance',
              'score', 'calorie']
}

dataset2zoptions = {
  'Sleep': ['None', 'weekday', 'is_holiday'],
  'Exercise': ['None', 'exercise', 'weekday', 'is_holiday'],
  'Stress': ['None', 'weekday', 'is_holiday'],
  'Step': ['None', 'weekday', 'is_holiday', 'source_type'],
  'Heart': ['None', 'time_offset', 'deviceuuid', 'weekday', 'is_holiday'],
  'Floors': ['None', 'time_offset', 'deviceuuid', 'weekday', 'is_holiday'],
  'Calories': ['None', 'deviceuuid', 'weekday', 'is_holiday'],
  'Summary': ['None', 'deviceuuid', 'weekday', 'is_holiday', 'goal'],
  
}

def time2yearf(time_obj):
    t_aux = pd.DatetimeIndex(time_obj)
    timef_list = [t.year + (t.month - 1.) / 12. + (t.day - 1.) / 365. for t in t_aux]
    return timef_list

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

def make_tz_changers(df, time_key, tz_key):
    df.sort_values(by=time_key, inplace=True)
    tz_list = df[tz_key].values
    time_obj = df[time_key].values
    cond = tz_list[:-1] != tz_list[1:]
    return time_obj[1:][cond]
