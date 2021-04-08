import os
import json

import pandas as pd

user_input = 'STEPS_KCAL'
directory = os.listdir(user_input)

searchstring = 'UDSFile'
data_s = []
for fname in directory:
    if os.path.isfile(user_input + os.sep + fname):
        # Full path
        if 'UDS' in fname:
            with open(user_input + os.sep + fname) as f:
                data_s.append(json.load(f))
