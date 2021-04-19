import os
import json

import pandas as pd

user_input = 'STEPS_KCAL'
directory = os.listdir(user_input)

searchstring = 'UDSFile'
data_s = []
for fname in directory:
    if os.path.isfile(user_input + os.sep + fname):
        # Full path
        if 'UDS' in fname:
            with open(user_input + os.sep + fname) as f:
                data_s.append(json.load(f))

big = [ pd.DataFrame.from_records(j) for j in data_s]

bigdf = pd.concat(big)
bigdf['date'] = pd.to_datetime([i.get('date') for i in bigdf.calendarDate])

bigf = bigdf[['date','activeSeconds','highlyActiveSeconds','totalSteps','allDayStress','activeKilocalories']].sort_values('date')
jk = bigf.allDayStress.apply(pd.Series).aggregatorList.apply(pd.Series)
total = jk.iloc[:,0].apply(pd.Series)

Active_Data = pd.concat([bigf,total],axis=1)[['date','activeSeconds','highlyActiveSeconds','totalSteps','allDayStress','activeKilocalories','averageStressLevel','stressDuration']].dropna()


user_input = 'SLEEP_DATA'
directory = os.listdir(user_input)

data_s = []
for fname in directory:
            with open(user_input + os.sep + fname) as f:
                data_s.append(json.load(f))

big = [ pd.DataFrame.from_records(j) for j in data_s]

bigdf = pd.concat(big)
bigdf['totalsleep'] =bigdf['deepSleepSeconds'].fillna(0)+ bigdf['lightSleepSeconds'].fillna(0)+bigdf['remSleepSeconds'].fillna(0)  + bigdf['awakeSleepSeconds'].fillna(0)
bigdf['sleepend']=     bigdf.sleepEndTimestampGMT.apply(pd.Series)
bigdf['sleepstart']= bigdf.sleepStartTimestampGMT.apply(pd.Series)

bigdf['calendarDate'] = pd.to_datetime(bigdf.calendarDate)
Active_Data_Full = pd.merge(bigdf[['totalsleep','sleepend','sleepstart','remSleepSeconds','calendarDate']],Active_Data,how='inner',left_on=['calendarDate'],right_on=['date'])

Active_Data_Full['sleepend'] = pd.to_datetime(Active_Data_Full.sleepend).dt.time
Active_Data_Full['sleepstart'] =  pd.to_datetime(Active_Data_Full.sleepstart).dt.time

Active_Data_Full.to_csv('garmin_data.csv')


###seperate write up - does exercise result in more sleep, on average?

## if i can find hr data, his could be good for ts. clustering