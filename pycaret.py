#import classification module
from pycaret.classification import *
import pandas as pd


filtered = pd.read_csv('data.csv')

filtered = filtered[['hour','day','MacaqueWhite','score','lag1','within_session','within_day','last_3_days','rating_diff']]

filtered = filtered.query('score != 0.5') ### no draws

filtered['score'] = pd.as_binary(filtered['score'])

exp_clf = setup(filtered, target = 'score',html = False)


best_specific = compare_models(whitelist = ['dt','rf','xgboost'])

top3 = compare_models()
dt = create_model('lightgbm')

plot_model(dt)

ensembled_dt = ensemble_model(dt)

evaluate_model(ensembled_dt)

interpret_model(dt)