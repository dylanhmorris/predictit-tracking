#!/usr/bin/env python3

##########################################
# name: candidate_timeseries_plot.py
# author: Dylan Morris <dhmorris@princeton.edu>
# description: generate a plot of conditional
# win probabilities for a single candidate
# as a function of time
# 
###########################################
import sys
import os
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import plotting_style as ps
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
register_matplotlib_converters()
import datetime

from analyze_data import read_data, get_cond_winprob_errors
from analyze_data import data_filename, data_dir


def candidate_timeseries_plot(candidate,
                              data,
                              nom_err=0.01,
                              pres_err=0.01,
                              x_padding = 5,
                              figsize = (10, 5)):
    
    fig, ax = plt.subplots(figsize=figsize)

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

    ax.set_xlim(left = (is_cand['whenPulled'].min() -
                        datetime.timedelta(days = x_padding)),
                right = (datetime.datetime.utcnow() +
                         datetime.timedelta(days = x_padding)))
    ax.set_ylim([0, 1])
    ax.set_xlabel("Date")
    ax.set_ylabel("implied probability of winning\n"
                  "presidency if nominated")
    ax.set_title("Conditional win probabilities\n"
                 "over time for {}".format(candidate))
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    script_path = os.path.relpath(sys.argv[0])
    if 'src' in script_path:
        run_data_dir = "dat"
        run_fig_dir = "out"
    else:
        run_data_dir = "../dat"
        run_fig_dir = "../out"

    if len(sys.argv) < 2:
        print("USAGE: {} <candidate> <output path>\n\n"
              "".format(sys.argv[0]))
    else:
        candidate = sys.argv[1]
        fig_path = sys.argv[2]

        print(fig_path)
        print("searching for candidate {}...".format(candidate))
        data = read_data(data_filename, run_data_dir)
        candidate_name_instances = data[data['candidate'].str.contains(candidate)]['candidate']
        if candidate_name_instances.empty:
            raise ValueError('Candidate matching name or '
                             'partial name "{}" not found'
                             ''.format(candidate))
        else:
            candidate_name = candidate_name_instances.iloc[0]
            print('Found candidate {}'.format(candidate_name))
            fig = candidate_timeseries_plot(candidate_name,
                                            data)    
            fig.savefig(fig_path)
