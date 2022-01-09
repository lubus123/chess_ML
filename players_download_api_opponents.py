import berserk
import datetime as dt
import pandas as pd
import math
import time

API_TOKEN = 'gLzMEHBJWpJa2Zdk'

session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session=session)
full = pd.read_csv('full.csv')

oponents = full.opp_id.value_counts()
oponents = oponents.to_frame().reset_index().query('opp_id >3 and opp_id < 13')

##of my past opponents, how many am i bettert than? with less / more games?

## step one get my oponents names.


start = berserk.utils.to_millis(dt.datetime(2015, 12, 8))
end = berserk.utils.to_millis(dt.datetime(2022, 12, 9))

playerbase = []
ids = oponents['index'].unique()
j = time.time()
for n, i in enumerate(ids, start=1):
    try:

        a = client.games.export_by_player(i, since=start, until=end, max=50000)
        df = pd.DataFrame.from_dict(list(a))
        df['player'] = i
        df.to_csv('playerdata_o/' + i + '.csv')
        playerbase.append(df)
        print(str(round(n / len(ids), 4) * 100) + '% complete ' + 'Player:' + i + ' Games :' + str(len(df)))
        print('Elapsed time:' + str(round((time.time() - j) / 60, 2)))
    except Exception as e:
        print("An exception occurred" + str(e))

pd.concat(playerbase).to_csv('playerdata_o/big.csv')
print('Done')
