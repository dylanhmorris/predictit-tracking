#!/usr/bin/env python3

##########################################
# name: candidate_timeseries_plot.py
# date: 2019-01-30
# author: Dylan Morris <dhmorris@princeton.edu>
# description: generate a plot of conditional
# win probabilities for a single candidate
# as a function of time
# 
###########################################
import pandas as pd
import plotting_style as ps
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import datetime

from analyze_data import read_data, get_cond_winprob_errors
from analyze_data import data_filename, data_dir

def candidate_timeseries_plot(candidate,
                              data,
                              nom_err=0.01,
                              pres_err=0.01):
    
    fig, ax = plt.subplots()

    has_cond = data[data['probPresidentGivenNominee'].notna()]
    has_cond = has_cond[has_cond['whenPulled'].notna()]
    is_cand_inds = has_cond['candidate'] == candidate
    is_cand = has_cond[is_cand_inds]
    is_cand = is_cand.sort_values(by='whenPulled')
    colors = [ps.party_cmap.get(party, 'grey')
              for party in is_cand['party']]
    is_cand.set_index('whenPulled')
    
    sns.scatterplot(
        data=is_cand,
        x='whenPulled',
        y='probPresidentGivenNominee',
        color=colors[0],
        ax=ax)
    
    errors = get_cond_winprob_errors(
        is_cand,
        nom_err=nom_err,
        pres_err=pres_err)
    
    ax.errorbar(
        x=is_cand['whenPulled'],
        y=is_cand['probPresidentGivenNominee'],
        yerr=errors,
        color=colors,
        fmt='none')

    ax.set_xlim(left=is_cand['whenPulled'].min() - datetime.timedelta(days=1),
                right=datetime.datetime.utcnow())
    ax.set_xlabel("Date")
    ax.set_ylabel("implied probability of winning\n"
                  "presidency if nominated")
    ax.set_title("Conditional win probabilities\n"
                 "over time for {}".format(candidate))
    fig.tight_layout()
