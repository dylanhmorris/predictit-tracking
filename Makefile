FIGS = out/conditional_winprobs.png out/conditional_winprobs.pdf

.PHONY: datapull update
update: datapull $(FIGS)

datapull:
	./src/pull_data.py

out/conditional_winprobs.%: dat/candidate_win_probabilities.csv
	./src/conditional_winprob_plot.py $@

