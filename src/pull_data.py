#!/usr/bin/env python3

#########################
#
# name: pull_data.py
# description: gets the data
# of interest (probability of
# winning nomination
# and probability of
# winning general,
# calculates implied conditional
# win prob and writes output to
# csv
###########################

import urllib.request
import urllib.parse
import json
import datetime
import pytz
import csv
import os
import sys

# global url/path parameters 
api_prefix = "https://www.predictit.org/api/marketdata/markets/"
outdir = "../out"
csv_name = "candidate_win_probabilities.csv"
csv_path = os.path.join(outdir, csv_name)

dem_nominee_id = 3633
gop_nominee_id = 3653
pres_winner_id = 3698

def mkdirp(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_market(market_id, api_prefix=api_prefix):
    full_url = urllib.request.urljoin(api_prefix, str(market_id))
    response = urllib.request.urlopen(full_url)
    txtdata = response.read()
    result = json.loads(txtdata)
    if result is None:
        raise ValueError("No parseable market found for market id "
                         "{}".format(market_id))
    return result


def prune_market(market_dict, min_price):
    return {contract['name']: contract for
            contract in market_dict['contracts']
            if contract['bestBuyYesCost'] > min_price}


def get_latest_prices(min_price = 0.01):

    markets = {
        "dem-nominee": get_market(dem_nominee_id),
        "gop-nominee": get_market(gop_nominee_id),
        "pres-winner": get_market(pres_winner_id)
    }

    markets = {market_name: prune_market(market, min_price)
               for market_name, market in markets.items()}

    return markets

def calc_conditional_prob(candidate_id,
                          nominee_market,
                          pres_market,
                          win_prob_key="bestBuyYesCost"):
    win_nom = nominee_market.get(candidate_id, {}).get(win_prob_key)
    win_pres = pres_market.get(candidate_id, {}).get(win_prob_key)
    if win_nom is not None and win_pres is not None:
        return win_pres / win_nom
    else:
        return None
    
def pull_current_data(win_prob_key="bestBuyYesCost"):

    current_datetime = datetime.datetime.now(pytz.utc)
    
    data = get_latest_prices()

    results = []
    
    for party in ['dem', 'gop']:
        party_results = data[party + '-nominee']
        for candidate in party_results.keys():
            pres_prob = data['pres-winner'].get(candidate, {}).get(win_prob_key, None)
            nom_prob = party_results.get(candidate, {}).get(win_prob_key, None)
            cond_prob = calc_conditional_prob(candidate,
                                              party_results,
                                              data['pres-winner'])
            new_row = {
                'candidate': candidate,
                'party': party,
                'probNominee': nom_prob,
                'probPresident': pres_prob,
                'probPresidentGivenNominee': cond_prob,
                'whenPulled': current_datetime.isoformat()
            }

            results.append(new_row)

        pass

    return results 


def pull_and_save_data(csv_path=csv_path):

    new_data = pull_current_data()

    mkdirp(csv_path)
    
    with open(csv_path, 'a+') as f:
        f.seek(0)  # jump to the beginning of the file
        try:
            header = next(csv.reader(f))
            dict_writer = csv.DictWriter(f, header)  # header found
        except StopIteration:  # no header found
            header = list(new_data[0].keys())
            dict_writer = csv.DictWriter(f, header)
            dict_writer.writeheader()
        f.seek(0,2)  # jump back to the end of the file
        for data_row in new_data:
            try:
                dict_writer.writerow(data_row)
            except ValueError:
                print("Error writing row to csv. "
                      "Check for header/key mismatch\n\n"
                      "Header: {}\n"
                      "Keys: {}\n\n".format(header, data_row.keys()))
                raise
    print("Data successfully pulled and written to csv "
          "{}".format(csv_path))
    
if __name__ == "__main__":
    script_path = os.path.relpath(sys.argv[0])
    if 'src' in script_path:
        run_outdir = "out"
    else:
        run_outdir = "../out"
    out_path = os.path.join(run_outdir, csv_name)
        
    pull_and_save_data(csv_path=out_path)
