FIGS = out/conditional_winprobs.pdf

.PHONY: datapull update
update: datapull $(FIGS)

datapull:
	./src/pull_data.py

out/conditional_winprobs.pdf: dat/candidate_win_probabilities.csv
	./src/analyze_data.py