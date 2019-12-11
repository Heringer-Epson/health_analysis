import sys
import json
import calendar
import holidays
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil import tz

sys.path.insert(0, './../')
from src import utils
from src.collect_data import data_collector
from src.proc_time import Process_Time, holidays_list_str

def create_time_collection():
    M ={}
    complete_tz, complete_t = [], []
    df_names = ['Sleep', 'Exercise', 'Stress', 'Step', 'Heart', 'Floors',
                'Calories', 'Summary']
    complete_tz, complete_t = [], []
    for i, name in enumerate(df_names):
        df = data_collector(name)
        time_obj = df['date'].values
        timef = utils.time2yearf(time_obj)        
        M[name] = timef

        #Create  list with the dates when the time offset changed.
        if 'time_offset' in df.columns:
            complete_t += list(timef)
            complete_tz += list(df['time_offset'].values)
    aux_df = pd.DataFrame({'date':complete_t, 'time_offset':complete_tz})
    tz_change_dates = utils.make_tz_changers(aux_df, 'date', 'time_offset')
    M['tz_change_dates'] = list(tz_change_dates)

    #Create list with holidays in the relevant time period.
    M['date_holidays'] = utils.time2yearf(holidays_list_str)
        
    with open('../outputs/time_collection.json', 'w') as json_file:
      json.dump(M, json_file)

create_time_collection()


