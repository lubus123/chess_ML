#import classification module
from pycaret.classification import *


filtered = pd.read_csv('data.csv')

filtered = filtered[['hour','day','MacaqueWhite','score','lag1','within_session','within_day']]
#intialize the setup (in Notebook env)

#intialize the setup (in Non-Notebook env)
exp_clf = setup(filtered, target = 'score', html = False)


best_specific = compare_models(whitelist = ['dt','rf','xgboost'],exp_clf)

top3 = compare_models(n_select = 3)