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
                   "matches": defaultdict(int), "innings": defaultdict(int), "fifties": defaultdict(int),
                   "centuries": defaultdict(int), "one_fifties": defaultdict(int), "double_centuries": defaultdict(int),
                   "ducks": defaultdict(int), "highest_score": defaultdict(int)} # innings
    
    for match in tqdm(matches):
        with open(raw_path + '\\' + match) as f:
            m_data = json.load(f)
            for kind in batter_dict:
                if kind in {"innings", "highest_score", "fifties", "centuries", "one_fifties", "double_centuries", "ducks"}: 
                    continue
                elif kind == "balls":
                    for player in m_data[kind]:
                        batter_dict["innings"][player] += 1
                elif kind == "runs":
                    for player in m_data[kind]:
                        batter_dict["highest_score"][player] = max(m_data["runs"][player], batter_dict["highest_score"][player])
                    if m_data["runs"][player] >= 200:
                        batter_dict["double_centuries"][player] += 1
                    if m_data["runs"][player] >= 150:
                        batter_dict["one_fifties"][player] += 1
                    if m_data["runs"][player] >= 100:
                        batter_dict["centuries"][player] += 1
                    if m_data["runs"][player] >= 50:
                        batter_dict["fifties"][player] += 1
                    if m_data["runs"][player] == 0:
                        batter_dict["ducks"][player] += 1
                else:
                    for player in m_data[kind]:
                        batter_dict[kind][player] += m_data[kind][player]
    
    with open(os.getcwd() + '\\..\\output\\json_output\\batter_agg.json', 'w') as f:
        json.dump(batter_dict, f)

def global_bat2csv():
    with open(os.getcwd() + '\\..\\output\\json_output\\batter_agg.json', 'r') as f:
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
    fifties_df = pd.DataFrame(data=bat_data["fifties"].items(), columns=["player", "fifties"])
    centuries_df = pd.DataFrame(data=bat_data["centuries"].items(), columns=["player", "centuries"])
    one_fifties_df = pd.DataFrame(data=bat_data["one_fifties"].items(), columns=["player", "one_fifties"])
    double_centuries_df = pd.DataFrame(data=bat_data["double_centuries"].items(), columns=["player", "double_centuries"])
    ducks_df = pd.DataFrame(data=bat_data["ducks"].items(), columns=["player", "ducks"])
    highest_score_df = pd.DataFrame(data=bat_data["highest_score"].items(), columns=["player", "highest_score"])
    
    dataframes = [balls_df, wickets_df, runs_df, sixes_df, fours_df, singles_df, doubles_df, triples_df, dots_df, matches_df, innings_df,
                  fifties_df, centuries_df, one_fifties_df, double_centuries_df, ducks_df, highest_score_df]
    
    final = reduce(lambda left, right: pd.merge(left, right, on="player", how='left'), dataframes)
    final["country"] = final["player"].apply(lambda x: x.split("|")[1])
    final["player"] = final["player"].apply(lambda x: x.split("|")[0])
    final.to_csv(os.getcwd() + '\\..\\output\\tabular\\batter_agg.csv', index=False)

if __name__ == '__main__':
    global_bat2csv()