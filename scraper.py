from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
url = 'https://database.lichess.org/'
dfs = pd.read_html(url)

formats = ['Antichess','Atomic', 'Fischer Random','Crazyhouse','Horde','King of the Hill','Racing Kings','Three-Check','Standard']

l2=[]
for n,i in enumerate(dfs):
    i['type'] = formats[n]

dfs_j= pd.concat(dfs)
dfs_j['DT'] =  pd.to_datetime(dfs_j['Month'], format='%Y - %B', errors='coerce')
    # .dt.strftime('%m-%y')
dfs_j = dfs_j.dropna(subset=['DT'])
dfs_j['size_num'] = dfs_j['Size'].str.replace('([A-Za-z]+)', '')
dfs_j['size_unit'] = dfs_j['Size'].str.extract('([A-Za-z]+)')

MB_CONVERSION = pd.DataFrame({'unit':['MB','kB','GB'] , 'cf':[1,0.001,1000]})

dfs_j = pd.merge(dfs_j, MB_CONVERSION, how ='left', left_on = 'size_unit', right_on='unit')
dfs_j['size_mb'] = pd.to_numeric(dfs_j['size_num']) * dfs_j['cf']
dfs_j['ngames'] = pd.to_numeric(dfs_j.Games)

g = sns.FacetGrid(dfs_j, col="type",  sharey =False,col_wrap=3)
g.map_dataframe(sns.lineplot, x="DT", y="ngames")
g.set_axis_labels("Date", "Games")
xformatter = mdates.DateFormatter("%y")
g.axes[0].xaxis.set_major_formatter(xformatter)
g.add_legend()
plt.show()

dfs_j.ngames = pd.to_numeric(dfs_j.ngames)
df_2 = dfs_j[['ngames','DT','type']].pivot(index='DT',columns = ['type'],values= ['ngames']).fillna('0')


for col in  df_2.columns:
    df_2[col] = pd.to_numeric(df_2[col], errors='coerce')

r_S = df_2.sum(1)

df_p = df_2.divide(r_S, axis=0)






# import urllib.request
#
# fp = urllib.request.urlopen(url)
# mybytes = fp.read()
#
# mystr = mybytes.decode("utf8")
# fp.close()
#
# soup = BeautifulSoup(mystr, 'html.parser')

import pandas
