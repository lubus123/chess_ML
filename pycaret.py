#import classification module
from pycaret.classification import *
import pandas as pd
from pycaret.classification import interpret_model

filtered = pd.read_csv('full.csv')








filtered = filtered[['hour','day','time_awake','MacaqueWhite' ,'highlyActiveSeconds','activeKilocalories','between_time','score','lag1','within_session','within_day','last_3_days','rating_diff','roll_30_delta','roll_90_delta','roll_200_delta','averageStressLevel','remSleepSeconds']]

filtered = filtered.query('score != 0.5') ### no draws

#filtered['score'] = pd.as_binary(filtered['score'])

exp_clf = setup(filtered, target = 'score',html = False)


top3 = compare_models()
dt = create_model('rf')

plot_model(dt)

ensembled_dt = ensemble_model(dt)

tuned_dt = tune_model(ensembled_dt, optimize = 'AUC')
#evaluate_model(ensembled_dt)

interpret_model(dt)

interpret_model(dt,feature='time_awake', plot = 'correlation')