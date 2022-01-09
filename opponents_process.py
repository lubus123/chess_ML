import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.io as pio
import datetime as dt
import json
import ast

opps = pd.read_csv('playerdata_o/big.csv')
opps = opps.query('variant == "standard" and speed == "blitz"')

opps.player.value_counts().hist()

plt.show()

def process_o(x):
    try:
        v= ast.literal_eval(x.players).get('white').get('user').get('name') == x.player
    except Exception as e:
        v=None
    return(v)

opps['White'] =opps.apply(lambda row: process_o(row),axis=1)


jk =opps_red.players.apply(pd.Series)

opps['MacaqueWhite'] =opps.apply(lambda row: process_o(row),axis=1)
opps['MacaqueBlack']=  opps['MacaqueWhite'].apply(lambda x: not x)

opps['my_rating'] = opps.loc[1:2].apply(lambda row: row['players'].get('white' if row['MacaqueWhite'] else 'black').get('rating'), axis = 1)
opps['opp_rating'] = opps.apply(lambda row: row['players'].get('white' if row['MacaqueBlack'] else 'black').get('rating'), axis = 1)
opps['rating_diff']= opps['my_rating'] - opps['opp_rating']
opps['opp_id'] =opps.apply(lambda row: row['players'].get('white' if not row['MacaqueWhite'] else 'black').get('user').get('id'), axis = 1)

opps['my_rating_change'] = opps.apply(lambda row: row['players'].get('white' if row['MacaqueWhite'] else 'black').get('ratingDiff'), axis = 1)
opps['new_rating'] = opps['my_rating']+ opps['my_rating_change']