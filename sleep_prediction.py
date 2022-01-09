from pycaret.regression import *
import pandas as pd
from pycaret.classification import interpret_model

holder =  pd.read_csv('garmin_data.csv')

holder['calendarDate'] =  pd.to_datetime(holder['calendarDate'])
holder['day'] = holder['calendarDate'].dt.day_name()

filtered= holder[['totalsleep','day','activeKilocalories','highlyActiveSeconds','totalSteps','sleep_dp1']].dropna()


exp_clf = setup(filtered, target = 'sleep_dp1',html = False)


top3 = compare_models()
dt = create_model('rf')

plot_model(dt)

ensembled_dt = ensemble_model(dt)

tuned_dt = tune_model(ensembled_dt, optimize = 'AUC')
#evaluate_model(ensembled_dt)

interpret_model(dt)

interpret_model(dt,feature='time_awake', plot = 'correlation')