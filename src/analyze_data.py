#!/usr/bin/env python3

import pandas as pd
import os
import matplotlib.pyplot as plt
import plotting_style as ps
import seaborn as sns
from textwrap import wrap
import sys
import numpy as np

data_filename = "candidate_win_probabilities.csv"
data_dir = "../dat"
fig_filename = "conditional_winprobs.pdf"
fig_dir = "../out/"

def read_data(data_filename=data_filename,
              data_dir=data_dir):
    data_path = os.path.join(data_dir, data_filename)
    data = pd.read_csv(data_path, header=0)
    data['whenPulled'] = pd.to_datetime(data['whenPulled'])
    
    return data 

def conditional_prob_plot(data,
                          plot_type="pointplot",
                          nom_err=0.01,
                          pres_err=0.01,
                          figpath=None):

    plotting_funcs = {
        "barplot": sns.barplot,
        "pointplot": sns.pointplot
    }

    plotting_func = plotting_funcs.get(plot_type,
                                       sns.pointplot)
    
    has_cond = data[data['probPresidentGivenNominee'].notna()]
    by_cand = has_cond.groupby('candidate')
    by_cand = by_cand.apply(lambda grp: grp.nlargest(1, 'whenPulled'))
    by_cand = by_cand.sort_values(by='probPresidentGivenNominee')

    fig_width = 15
    fig_height = 4
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    party_cmap = {
        'dem': '#2062cc', # nicer blue than default
        'gop': '#ff3535'  # likewise nicer red
    }

    colors = [party_cmap.get(party, 'grey') for
              party in by_cand['party']]

    print(by_cand[['candidate', 'probPresidentGivenNominee']])
    
    plotting_func(
        data=by_cand,
        x='candidate',
        y='probPresidentGivenNominee',
        palette=colors,
        ci=[0.25, 0.75],
        join=False,
        ax=ax)

    min_probs = ((by_cand['probPresident'] - pres_err)/(by_cand['probNominee'] + nom_err)).clip(0, 1)
    max_probs = ((by_cand['probPresident'] + pres_err)/(by_cand['probNominee'] - nom_err)).clip(0, 1)

    errors = np.vstack([by_cand['probPresidentGivenNominee'] - min_probs,
                        max_probs - by_cand['probPresidentGivenNominee']])
    print(errors)
        
    ax.errorbar(
        x=by_cand['candidate'],
        y=by_cand['probPresidentGivenNominee'],
        yerr=errors,
        color=colors,
        fmt='none')
    
    xticklabs = ['\n'.join(str(lab).split())
                 for lab in by_cand['candidate']]

    ax.set_ylabel("implied win probability\nif nominated",
                  fontsize='x-large')
    ax.set_xlabel('')

    ax.set_xticklabels(xticklabs,
                       fontsize='medium')
    ax.set_ylim([0, 1])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    
    fig.tight_layout()

    if figpath is not None:
        fig.savefig(figpath)

    return True


if __name__ == "__main__":
    script_path = os.path.relpath(sys.argv[0])
    if 'src' in script_path:
        run_data_dir = "dat"
        run_fig_dir = "out"
    else:
        run_data_dir = "../dat"
        run_fig_dir = "../out"
        
    fig_path = os.path.join(run_fig_dir, fig_filename)

    data = read_data(data_filename, run_data_dir)
    conditional_prob_plot(data,
                          figpath=fig_path)    
