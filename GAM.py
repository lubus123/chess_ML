
import pygam as pg
import pandas as pd
import matplotlib.pyplot as plt
filtered = pd.read_csv('full.csv')

filtered = filtered.query('score != 0.5').query('time_awake<24')
gam  = pg.LogisticGAM(pg.s(0,basis='cp')+pg.f(1)+pg.s(2)+pg.s(3)+pg.s(4) +pg.s(5)).fit(X=filtered[['hour','day','within_day','last_3_days','rating_diff','time_awake']],y=filtered['win'])

gam.summary()

##hour has to be a cyclical smoother
def draw_terms(gam, plt=None):
        for i, term in enumerate(gam.terms):
          if term.isintercept:
            continue

          XX = gam.generate_X_grid(term=i)
          pdep, confi = gam.partial_dependence(term=i, X=XX, width=0.95)

          plt.figure()
          plt.plot(XX[:, term.feature], pdep)
          plt.plot(XX[:, term.feature], confi, c='r', ls='--')
          plt.title(repr(term))
          plt.show()
draw_terms(gam,plt)