import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

with open('games.json') as f:
  data = json.load(f)

  holder = pd.DataFrame.from_records(data)

  holder['date'] = pd.to_datetime(holder['createdAt'], unit='ms')

  holder['duration'] = holder['lastMoveAt'] - holder['createdAt'] / 1000

  holder['winner'] = holder['winner'].fillna('draw') ##add draws


  ##### date feature creation: Day of week, Date, hour is holiday?

  holder['hour'] = holder['date'].dt.hour

  holder['day'] = holder['date'].dt.weekday

  holder['Date'] =  holder['date'].dt.date


#####waas i white?
holder= holder.query('rated == True') ## only rated games

holder['MacaqueWhite'] = pd.Series([i.get('white').get('user').get('name') =='macaqueattack' for i in holder.players])
holder['MacaqueBlack'] = pd.Series([i.get('black').get('user').get('name') =='macaqueattack' for i in holder.players])


#0/1/0.5 score
holder['score'] = holder.MacaqueWhite*(holder.winner=='white') + holder.MacaqueBlack*(holder.winner=='black') + 0.5*(holder.winner=='draw')

#o/1 score
holder['win'] = holder.MacaqueWhite*(holder.winner=='white') + holder.MacaqueBlack*(holder.winner=='black')

### global lags

holder['lag1'] = holder.score.shift(1)
holder['lag1win'] = holder.score.shift(1)

holder['between_time'] = abs(holder.createdAt.diff())/(1000*60) #bin this later

cutoff = 20
#20 minute session cutoff

holder['consecutive'] = holder['between_time'] >20
holder['session'] = holder['consecutive'].cumsum()

holder['within_session'] = holder.groupby(['session']).cumcount()+1  ##within session

holder['within_day'] = holder.groupby(['Date']).cumcount()+1  ##within day



filtered = holder.dropna(subset = ['score','lag1'])    ##drop nas


filtered['score']= pd.to_numeric(filtered['score'])

filtered.to_csv('data.csv')
##feature :: sunglisht?  <--  needs my local clock
##garmin
##activities
#calorie
#steps

## TOTAL DAILY!
### rolling sum

#rating difference

##modelling 1) gam
##modelling 2) pycaret
##modelling 3) scikit-learn (from book)


  #### to Day - ts     Date / sTART sCORE / END SCORE / GAMES PLAYED