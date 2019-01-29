import pandas as pd
import os
import matplotlib.pyplot as plt
import plotting_style as ps
import seaborn as sns
from textwrap import wrap

data_filename = "candidate_win_probabilities.csv"
data_dir = "../dat"
data_path = os.path.join(data_dir, data_filename)

data = pd.read_csv(data_path, header=0)
data['whenPulled'] = pd.to_datetime(data['whenPulled'])

figpath = "../out/conditional_winprobs.pdf"

def conditional_prob_barplot(data=data):
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
    sns.barplot(
        data=by_cand,
        x='candidate',
        y='probPresidentGivenNominee',
        palette=colors,
        ax=ax)
    
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

    fig.savefig(figpath)
