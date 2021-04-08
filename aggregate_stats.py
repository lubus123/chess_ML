import pandas as pd


filtered = pd.read_csv('data.csv')

filtered.groupby('Date').count().iloc[:,1].plot()

