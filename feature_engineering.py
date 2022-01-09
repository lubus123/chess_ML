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


holder['MacaqueWhite'] =holder.players.apply(lambda row: row.get('white').get('user').get('name') =='macaqueattack')
holder['MacaqueBlack']=  holder['MacaqueWhite'].apply(lambda x: not x)

holder['my_rating'] = holder.apply(lambda row: row['players'].get('white' if row['MacaqueWhite'] else 'black').get('rating'), axis = 1)
holder['opp_rating'] = holder.apply(lambda row: row['players'].get('white' if row['MacaqueBlack'] else 'black').get('rating'), axis = 1)
holder['rating_diff']= holder['my_rating'] - holder['opp_rating']
holder['opp_id'] =holder.apply(lambda row: row['players'].get('white' if not row['MacaqueWhite'] else 'black').get('user').get('id'), axis = 1)

holder['my_rating_change'] = holder.apply(lambda row: row['players'].get('white' if row['MacaqueWhite'] else 'black').get('ratingDiff'), axis = 1)
holder['new_rating'] = holder['my_rating']+ holder['my_rating_change']


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

holder['last_3_days']=  holder.createdAt.loc[::-1].expanding(1).apply(lambda x: sum(abs(max(x)-x) <1000*60*60*72 )).loc[::-1]

#explore hoe my ( then others) rating fluctuates. in particular, around the xx00 resistance points . do people stop playinh once this is hit? should the?

filtered = holder.dropna(subset = ['score','lag1'])    ##drop nas

filtered =filtered.iloc[:-100] #drop 100 last rows for last_3 warm-up


filtered['score']= pd.to_numeric(filtered['score'])

filtered.to_csv('data.csv')
##feature :: sunglisht?  <--  needs my local clock

##activities


##modelling 1) gam
##modelling 2) pycaret
##modelling 3) scikit-learn (from book)


  #### to Day - ts     Date / sTART sCORE / END SCORE / GAMES PLAYED