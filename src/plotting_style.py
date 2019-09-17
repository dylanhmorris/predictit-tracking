#!/usr/bin/env python3

###############
# name: plotting_style.py
# description: fixes sensibile
# plotting default parameter
# values
#
###############

import matplotlib as mpl
import matplotlib.pyplot as plt

plt.style.use("seaborn-white")

mpl.rcParams['axes.labelsize']= "x-large"
mpl.rcParams['xtick.labelsize']= "x-large"
mpl.rcParams['ytick.labelsize']= "x-large"
mpl.rcParams['axes.titlesize']= "x-large"
mpl.rcParams['axes.formatter.use_mathtext'] = True
mpl.rcParams['axes.formatter.limits'] = ((-3, 3))
mpl.rcParams['axes.grid'] = True
mpl.rcParams['legend.frameon'] = True
mpl.rcParams['legend.fancybox'] = True
mpl.rcParams['legend.framealpha'] = 1
mpl.rcParams['text.usetex'] = True

party_cmap = {
        'dem': '#2062cc', # nicer blue than default
        'gop': '#ff3535'  # likewise nicer red
}

