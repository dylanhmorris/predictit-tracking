import numpy as np
from pull_data import get_all_markets
import operator

def dutchbook_profit(prices):
    return len(prices) - np.sum(prices) - 1

def dutchbook_percent(prices):
    return dutchbook_profit(prices) / np.sum(prices)

def calc_breakeven(profit_take = 0.1,
                   withdrawal_take = 0.05,
                   input_multiplier = 1):
    wt = 1 - withdrawal_take
    pt = 1 - profit_take
    return (((1 / wt) - input_multiplier) / pt)

def best_dutchbook(market_contracts):
    sorted_prices = sorted(
        [item['bestBuyNoCost'] for item in market_contracts
         if item['bestBuyNoCost'] is not None])
    dutchbook_percentages = [
        dutchbook_percent(sorted_prices[:x]) for
        x in range(1, len(sorted_prices))]
    if len(dutchbook_percentages) > 0:
        result = max(dutchbook_percentages)
    else:
        result = None
    return result

def get_all_dutchbooks():
    market_data = get_all_markets()
    dutchbook_data = {
        market['shortName'] : best_dutchbook(market['contracts'])
        for market in market_data}

    def prune_func(val):
        if val is not None:
            return val > 0
        return False
    
    pruned_dutchbook_data = {
        key: val for key, val in dutchbook_data.items()
        if prune_func(val)}

    return pruned_dutchbook_data

def get_best_dutchbook():

    dbs = get_all_dutchbooks()
    best = max(dbs.items(), key=operator.itemgetter(1))[0]
    return (best, dbs[best])
