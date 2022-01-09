import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.io as pio
import datetime as dt

from statsmodels.tsa.seasonal import seasonal_decompose

pio.renderers.default = "browser"

chess_result = pd.read_csv('data.csv').query('speed == "blitz"')
garmin = pd.read_csv('garmin_data.csv')


garmin['sleep_end_epoch']=  (pd.to_datetime(garmin.sleepend) - dt.datetime(1970,1,1)).dt.total_seconds()*1000

garmin['sleep_start_epoch']=  (pd.to_datetime(garmin.sleepstart) - dt.datetime(1970,1,1)).dt.total_seconds()*1000

def helper(x):
    k=   (x-full.sleep_end_epoch >0).cumsum()
    ind = k.index[k==1][0]
    return((x-full.sleep_end_epoch.iloc[ind])/(60*1000*60)) ##must be sorted


full = pd.merge(chess_result,garmin,how='inner',left_on=['Date'],right_on=['date'])

full['time_awake'] = full.createdAt.apply(lambda x: helper(x))

full.query('time_awake<30').time_awake.hist(bins=40)

full['roll_rating_30'] = full.loc[::-1].my_rating.rolling(30).median().loc[::-1]
full['roll_30_delta'] = full['roll_rating_30'] -full.opp_rating
full['roll_rating_90'] = full.loc[::-1].my_rating.rolling(90).median().loc[::-1]
full['roll_90_delta'] = full['roll_rating_90'] -full.opp_rating
full['roll_rating_200'] = full.loc[::-1].my_rating.rolling(90).median().loc[::-1]
full['roll_200_delta'] = full['roll_rating_200'] -full.opp_rating


full['roll_rating_30'].iloc[::-1].reset_index().dropna().roll_rating_30.plot(ylim=[1400,2000])

full.to_csv('full.csv')
result = seasonal_decompose(full['roll_rating'].iloc[::-1].reset_index().dropna().roll_rating, model='additive',period=300)
result.plot()
plt.show()

######calculate how many games since awake
###### relative performance (median last 100 ELO vs opponent ELO ) - get rating change
full = pd.read_csv('full.csv')

oponents = full.opp_id.value_counts()
oponents.to_frame().reset_index().query('opp_id >3 and opp_id < 13')

DAY_SUM = full.groupby('Date', as_index=False).agg(
    n_games =pd.NamedAgg(column='session', aggfunc=len),
    n_session=pd.NamedAgg(column='session', aggfunc=lambda x:  x.value_counts().count()),
    rating_min = pd.NamedAgg(column='new_rating', aggfunc=min),
    rating_max = pd.NamedAgg(column='new_rating', aggfunc=max),
    rating_end = pd.NamedAgg(column='new_rating', aggfunc= lambda x: x.iloc[-1]),
    rating_open = pd.NamedAgg(column='my_rating', aggfunc= lambda x: x.iloc[0])
)
DAY_SUM['rating_var']= DAY_SUM['rating_max']-DAY_SUM['rating_min']





SESSION_SUM = full.groupby('session', as_index=False).agg(
    n_games =pd.NamedAgg(column='session', aggfunc=len),
    rating_min = pd.NamedAgg(column='new_rating', aggfunc=min),
    rating_max = pd.NamedAgg(column='new_rating', aggfunc=max),
    rating_end = pd.NamedAgg(column='new_rating', aggfunc= lambda x: x.iloc[-1]),
    rating_open = pd.NamedAgg(column='my_rating', aggfunc= lambda x: x.iloc[0]),
    time_awake = pd.NamedAgg(column = 'time_awake',aggfunc = max),
)
SESSION_SUM['rdiff'] = SESSION_SUM['rating_end'] - SESSION_SUM['rating_open']
SESSION_SUM['rdiff_norm'] = (SESSION_SUM['rating_end'] - SESSION_SUM['rating_open']) / SESSION_SUM['n_games']

sns.regplot(x ='time_awake', y='rdiff',data=SESSION_SUM.query('n_games>4 and time_awake<40'))
plt.show()
##do first 3 game affect result?

fig = go.Figure(data=go.Ohlc(x=DAY_SUM['Date'],
                    open=DAY_SUM['rating_open'],
                    high=DAY_SUM['rating_max'],
                    low=DAY_SUM['rating_min'],
                    close=DAY_SUM['rating_end']))
fig.show()
####fill in empty time slots. does taking break help?


## performance metrics:
#winrate
#points +-
#point

### analyse worst days. what went wrong?

#kalman filter?
#rolling sd
#varianc model

DAY_SUM_l = pd.melt(DAY_SUM[['Date','rating_min','rating_max','rating_end']],'Date')
sns.lineplot(x='Date', y='value', hue='variable',
             data=DAY_SUM_l)


WEEKDAY = DAY_SUM = full.groupby('day').agg(
    n_games =pd.NamedAgg(column='session', aggfunc=len),
    n_session=pd.NamedAgg(column='session', aggfunc=lambda x:  x.value_counts().count()),
    winp = pd.NamedAgg(column = 'score', aggfunc= lambda x: sum(x==1)/len(x))
)

window = DAY_SUM.n_games.rolling(3)
window.mean().plot()
plt.show()
### by weekday
##by hr
## -> variation
### ->density by hr / day


##### chess performance