#!/usr/bin/env python3

import pandas as pd
import os
import numpy as np

data_filename = "candidate_win_probabilities.csv"
data_dir = "../dat"

def read_data(data_filename=data_filename,
              data_dir=data_dir):
    data_path = os.path.join(data_dir, data_filename)
    data = pd.read_csv(data_path, header=0)
    data['whenPulled'] = pd.to_datetime(data['whenPulled'])
    
    return data 



def get_cond_winprob_errors(
        data,
        nom_err=0.01,
        pres_err=0.01):
    
    min_probs = ((data['probPresident'] - pres_err) /
                 (data['probNominee'] + nom_err)).clip(0, 1)
    
    max_probs = ((data['probPresident'] + pres_err) /
                 (data['probNominee'] - nom_err)).clip(0, 1)
    
    errors = np.vstack([data['probPresidentGivenNominee'] - min_probs,
                        max_probs - data['probPresidentGivenNominee']])

    return errors
