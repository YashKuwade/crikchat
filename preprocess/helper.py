import os
import json
from tqdm import tqdm
import pandas as pd
from collections import defaultdict
from functools import reduce

def match2match_to_global_bat():
    raw_path = os.getcwd() + '\\..\\data\\match_batter_agg'
    matches = os.listdir(raw_path)
    batter_dict = {"balls": defaultdict(int), "runs": defaultdict(int), "wickets": defaultdict(int), 
                   "fours": defaultdict(int), "sixes": defaultdict(int), "dots": defaultdict(int), 
                   "triples": defaultdict(int), "doubles": defaultdict(int), "singles": defaultdict(int), 
                   "matches": defaultdict(int), "innings": defaultdict(int)} # innings
    
    for match in tqdm(matches):
        with open(raw_path + '\\' + match) as f:
            m_data = json.load(f)
            for kind in batter_dict:
                if kind == "innings": continue
                if kind == "balls":
                    for player in m_data[kind]:
                        batter_dict["innings"][player] += 1
                for player in m_data[kind]:
                    batter_dict[kind][player] += m_data[kind][player]
    
    with open(os.getcwd() + '\\..\\output\\batter_agg.json', 'w') as f:
        json.dump(batter_dict, f)

def global_bat2csv():
    with open(os.getcwd() + '\\..\\output\\batter_agg.json', 'r') as f:
        bat_data = json.load(f)
    
    balls_df = pd.DataFrame(data=bat_data["balls"].items(), columns=["player", "balls"])
    wickets_df = pd.DataFrame(data=bat_data["wickets"].items(), columns=["player", "wickets"])
    runs_df = pd.DataFrame(data=bat_data["runs"].items(), columns=["player", "runs"])
    sixes_df = pd.DataFrame(data=bat_data["sixes"].items(), columns=["player", "sixes"])
    fours_df = pd.DataFrame(data=bat_data["fours"].items(), columns=["player", "fours"])
    singles_df = pd.DataFrame(data=bat_data["singles"].items(), columns=["player", "singles"])
    doubles_df = pd.DataFrame(data=bat_data["doubles"].items(), columns=["player", "doubles"])
    triples_df = pd.DataFrame(data=bat_data["triples"].items(), columns=["player", "triples"])
    dots_df = pd.DataFrame(data=bat_data["dots"].items(), columns=["player", "dots"])
    matches_df = pd.DataFrame(data=bat_data["matches"].items(), columns=["player", "matches"])
    innings_df = pd.DataFrame(data=bat_data["innings"].items(), columns=["player", "innings"])
    
    dataframes = [balls_df, wickets_df, runs_df, sixes_df, fours_df, singles_df, doubles_df, triples_df, dots_df, matches_df, innings_df]
    
    final = reduce(lambda left, right: pd.merge(left, right, on="player", how='left'), dataframes)
    final["country"] = final["player"].apply(lambda x: x.split("|")[1])
    final["player"] = final["player"].apply(lambda x: x.split("|")[0])
    final.to_csv(os.getcwd() + '\\..\\output\\tabular\\batter_agg.csv', index=False)

if __name__ == '__main__':
    global_bat2csv()