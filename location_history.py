import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


chess_result = pd.read_csv('data.csv')
with open('LOCATION_HISTORY\Location History.json') as f:
  data = json.load(f)

  holder = pd.DataFrame.from_records(data)
  holder = holder.locations.apply(pd.Series)

holder = holder[['timestampMs','latitudeE7','longitudeE7']]

holder = holder[holder.timestampMs.apply(lambda x: x.isnumeric())]
holder.timestampMs= holder.timestampMs.astype('double')
min_time= chess_result.createdAt.min()
holder = holder.query(f'timestampMs> {min_time}')

holder.to_csv('location_processed.csv')

## need to cluster lat/long
## add closest value clust to chess
##