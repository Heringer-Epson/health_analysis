import calendar
import holidays
import numpy as np
from datetime import datetime
from dateutil import tz

#List of holidays in the relevant time range.
holidays_obj = holidays.CountryHoliday('Canada', state=None, prov='Ontario')
holidays_list = (
  holidays_obj['2016-1-1':'2016-12-31']
  + holidays_obj['2017-1-1':'2017-12-31'] 
  + holidays_obj['2018-1-1':'2018-12-31'] 
  + holidays_obj['2019-1-1':'2019-12-31'])
holidays_list_str = [t.strftime('%Y/%m/%d') for t in holidays_list]

weekday_str2num = {'Sunday':1, 'Monday':2, 'Tuesday':3, 'Wednesday':4,
                   'Thursday':5, 'Friday':6, 'Saturday':7}

class Process_Time(object):
    """
    Description:
    ------------
    Given a list of time strings, convert it to a datetime object which is in the
    local timezone.
    """        
    def __init__(self, df, timestart_key, timeend_key, UTC_key, need_correction,
                 time_format):
        self.df = df
        self.timestart_key = timestart_key
        self.timeend_key = timeend_key
        self.UTC_key = UTC_key
        self.need_correction = need_correction
        self.time_format = time_format
                        
    def create_date_obj(self, key):
        if self.time_format == 'milisec':
            time_obj = np.array(
              [datetime.fromtimestamp(t) for t in self.df[key].values/1000.])            
        else:
            time_obj = np.array(
              [datetime.strptime(t, self.time_format) for t in self.df[key].values])

        #Convert to local time if needed.
        if self.need_correction:
            from_zone = tz.gettz('UTC')
            to_zone = [tz.gettz(t_off) for t_off in self.df[self.UTC_key]]
            time_obj_corr = np.array([_t.replace(tzinfo=from_zone).astimezone(_to_zone).replace(tzinfo=None)
                                      for (_t,_to_zone) in zip(time_obj,to_zone)])            
        else:
            time_obj_corr = time_obj
            
        return time_obj_corr
    
    def run(self):
        #Compute start and end time in standard format.
        if self.timestart_key is not None:
            time_obj = self.create_date_obj(self.timestart_key)
            self.df['Start_time_obj'] = time_obj
            self.df['date'] = np.array([t.strftime('%Y/%m/%d') for t in time_obj]) 
            self.df['start_hour'] = np.array([t.hour + t.minute/60. + t.second/3600. for t in time_obj])  
            self.df['is_holiday'] = [t in holidays_list_str for t in self.df['date'].values]
            self.df['weekday'] = np.array([calendar.day_name[t.weekday()] for t in time_obj])
            self.df['weekday_num'] = self.df['weekday'].map(weekday_str2num)
    
        if self.timeend_key is not None:
            time_obj = self.create_date_obj(self.timeend_key)
            self.df['End_time_obj'] = time_obj        
            self.df['end_hour'] = np.array([t.hour + t.minute/60. + t.second/3600. for t in time_obj])
            
        if ((self.timestart_key is not None) and (self.timeend_key is not None)):
            self.df['duration'] = self.df['End_time_obj'] - self.df['Start_time_obj']

        #Sort df after all quantities have been computed.
        self.df.sort_values(by ='Start_time_obj', inplace=True)
        return self.df 
