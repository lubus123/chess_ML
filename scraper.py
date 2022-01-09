import statsmodels
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


from statsmodels.tsa.seasonal import seasonal_decompose,STL


url_lock = 'https://en.wikipedia.org/wiki/COVID-19_lockdowns'

url = 'https://database.lichess.org/'
dfs = pd.read_html(url)
dfs_lock = pd.read_html(url_lock)
formats = ['Antichess','Atomic', 'Fischer Random','Crazyhouse','Horde','King of the Hill','Racing Kings','Three-Check','Standard']

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

dfs_j['compression_ratio']=dfs_j['ngames']/dfs_j['size_mb']



sns.set_style("darkgrid")
g = sns.FacetGrid(dfs_j, col="type",  sharey =False,col_wrap=3)
g.map_dataframe(sns.lineplot, x="DT", y="ngames")
g.set_axis_labels("Date", "Games")
xformatter = mdates.DateFormatter("%y")
g.axes[0].xaxis.set_major_formatter(xformatter)
g.add_legend()
plt.savefig('Games_Total.png', bbox_inches = "tight")

sns.set_style("darkgrid")
g = sns.FacetGrid(dfs_j, col="type",  sharey =False,col_wrap=3)
g.map_dataframe(sns.lineplot, x="DT", y="compression_ratio")
g.set_axis_labels("Compression Ratio", "Games")
xformatter = mdates.DateFormatter("%y")
g.axes[0].xaxis.set_major_formatter(xformatter)
g.add_legend()
plt.savefig('Games_Compression.png', bbox_inches = "tight")


plt.show()
dfs_j.ngames = pd.to_numeric(dfs_j.ngames)
dfs_j.type = pd.to_string
df_2 = dfs_j[['ngames','DT','type']].pivot_table(index = 'DT',columns = 'type',values= 'ngames').fillna('0')


for col in  df_2.columns:
    df_2[col] = pd.to_numeric(df_2[col], errors='coerce')

growth = (df_2 -df_2.shift(1)) /df_2.shift(1)
growth = growth.reset_index().melt('DT')

g = sns.FacetGrid(growth, col="type",  sharey =False,col_wrap=3)
g.map_dataframe(sns.lineplot, x="DT", y="value")
g.set_axis_labels("Date", "Games")
xformatter = mdates.DateFormatter("%y")
g.axes[0].xaxis.set_major_formatter(xformatter)
g.add_legend()
plt.savefig('Games_Growth.png', bbox_inches = "tight")

r_S = df_2.sum(1)

df_2 = df_2.divide(r_S, axis=0)

d_p_w = df_2.reset_index().melt('DT')

d_p_w['value'] *= 100

g=sns.lineplot(x='DT', y='value', hue='type', data=d_p_w.query('type != "Standard"'),)
plt.xlabel("Date")
plt.ylabel("% Total Lichess Games")
plt.savefig('perc_Total.png', bbox_inches = "tight")

g=sns.lineplot(x='DT', y='ngames', hue='type', data=dfs_j.query('type != "Standard"'))

plt.show()


decomp_df = dfs_j.query('type == "Atomic"')

result = STL(decomp_df.ngames.iloc[::-1].to_numpy() ,period=12).fit()
result.plot()
plt.show()


import ruptures as rpt

# generate signal
n
# detection
algo = rpt.Pelt(model="rbf").fit(decomp_df.ngames.iloc[::-1].to_numpy())
result_cpt = algo.predict(pen=10)

# display
rpt.display(decomp_df.ngames.iloc[::-1].to_numpy(),result_cpt)
plt.show()


#### estimate the time cost of 'queens gambit'

