
import pygam as pg
import pandas as pd

filtered = pd.read_csv('data.csv')

gam  = pg.LogisticGAM(pg.s(0)+pg.s(1)+pg.s(2)+pg.f(3)+pg.f(4)).fit(X=filtered[['hour','day','within_day','lag1win','MacaqueWhite']],y=filtered['win'])

gam.summary()

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
