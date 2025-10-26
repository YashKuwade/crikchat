import os
import json
from tqdm import tqdm
from collections import defaultdict

def count_without_stats(match_data=None):
    if "sport_event" not in match_data:
        return 0
    if "tournament" not in match_data["sport_event"]:
        return 0
    if "type" not in match_data["sport_event"]["tournament"]:
        return 0
    if match_data["sport_event"]["tournament"]["type"] == "t20i":
        if "statistics" not in match_data:
            return 0
        return 1
    return 0
    
def t20i_batter_summary(match_data=None):
    if ("sport_event" not in match_data 
        or "tournament" not in match_data["sport_event"] 
        or "type" not in match_data["sport_event"]["tournament"]
        or "statistics" not in match_data
        or "innings" not in match_data["statistics"]
        or match_data["sport_event"]["tournament"]["type"] != "t20i"):
        return False, {}
    
    gender = match_data["sport_event"]["tournament"]["gender"]
    
    batter_dict = {}
    for inning in match_data["statistics"]["innings"]:

        for team in inning["teams"]:
            if "batting" in team["statistics"]:
                players = team["statistics"]["batting"]["players"]
                # handle one player multiple countries later
                country =  team["name"]
                for player_data in players:
                    name = player_data["name"]
                    player_id = player_data["id"]
                    stats = player_data["statistics"]
                    try:
                        batter_dict[player_id] = defaultdict(int)
                        batter_dict[player_id]["name"] = name
                        batter_dict[player_id]["country"] = country
                        batter_dict[player_id]["gender"] = gender
                        batter_dict[player_id]["runs"] = stats["runs"]
                        batter_dict[player_id]["balls_faced"] = stats["balls_faced"]
                        batter_dict[player_id]["fours"] = stats["fours"]
                        batter_dict[player_id]["sixes"] = stats["sixes"]
                        batter_dict[player_id]["dot_balls"] = stats["dot_balls"]
                        batter_dict[player_id]["threes"] = stats["threes"]
                        batter_dict[player_id]["twos"] = stats["twos"]
                        batter_dict[player_id]["ones"] = stats["ones"]
                        batter_dict[player_id]["minutes_at_crease"] = stats["minutes_at_crease"]
                    except:
                        print(stats)
                        return False, {}
                    if "dismissal" in stats:
                        batter_dict[player_id]["wicket"] = 1
                    else:
                        batter_dict[player_id]["wicket"] = 0

                    if stats["runs"] >= 50:
                        batter_dict[player_id]["fifties"] = 1
                    else:
                        batter_dict[player_id]["fifties"] = 0

                    if stats["runs"] >= 100:
                        batter_dict[player_id]["centuries"] = 1
                    else:
                        batter_dict[player_id]["centuries"] = 0
                    
                    if stats["runs"] >= 150:
                        batter_dict[player_id]["one_fifties"] = 1
                    else:
                        batter_dict[player_id]["one_fifties"] = 0
                    
                    if stats["runs"] >= 200:
                        batter_dict[player_id]["double_century"] = 1
                    else:
                        batter_dict[player_id]["double_century"] = 0

                    if stats["runs"] == 0:
                        batter_dict[player_id]["ducks"] = 1
                    else:
                        batter_dict[player_id]["ducks"] = 0

    return True, batter_dict

if __name__ == "__main__":
    raw_path = os.getcwd() + '\\..\\data\\match_timelines\\'
    matches = os.listdir(raw_path)

    batter_dict = {}
    failed = 0
    for match in tqdm(matches):
        with open(raw_path + match) as f:
            m_data = json.load(f)
        
        if count_without_stats(m_data):
            failed += 1
    
    print(failed)

    #     flag, match_dict = t20i_batter_summary(m_data)
        
    #     if not flag:
    #         failed += 1
    #         continue
        
    #     for player in match_dict:
    #         if player not in batter_dict:
    #             batter_dict[player] = {}
            
    #         batter_dict[player]["name"] = match_dict[player]["name"]
    #         batter_dict[player]["country"] = match_dict[player]["country"]
    #         batter_dict[player]["gender"] = match_dict[player]["gender"]
    #         batter_dict[player]["runs"] = batter_dict[player].get("runs", 0) + match_dict[player]["runs"]
    #         batter_dict[player]["balls_faced"] = batter_dict[player].get("ball_faced", 0) + match_dict[player]["ball_faced"]
    #         batter_dict[player]["wickets"] = batter_dict[player].get("wickets", 0) + match_dict[player]["wicket"]
    #         batter_dict[player]["fours"] = batter_dict[player].get("fours", 0) + match_dict[player]["fours"]
    #         batter_dict[player]["sixes"] = batter_dict[player].get("sixes", 0) + match_dict[player]["sixes"]
    #         batter_dict[player]["ones"] = batter_dict[player].get("ones", 0) + match_dict[player]["ones"]
    #         batter_dict[player]["twos"] = batter_dict[player].get("twos", 0) + match_dict[player]["twos"]
    #         batter_dict[player]["threes"] = batter_dict[player].get("threes", 0) + match_dict[player]["threes"]
    #         batter_dict[player]["dot_balls"] = batter_dict[player].get("dot_balls", 0) + match_dict[player]["dot_balls"]
    #         batter_dict[player]["minutes_at_crease"] = batter_dict[player].get("minutes_at_crease", 0) + match_dict[player]["minutes_at_crease"]
    #         batter_dict[player]["fifties"] = batter_dict[player].get("fifties", 0) + match_dict[player]["fifties"]
    #         batter_dict[player]["hundreds"] = batter_dict[player].get("hundreds", 0) + match_dict[player]["hundreds"]
    #         batter_dict[player]["double_century"] = batter_dict[player].get("double_century", 0) + match_dict[player]["double_century"]
    #         batter_dict[player]["one_fifties"] = batter_dict[player].get("one_fifties", 0) + match_dict[player]["one_fifties"]
    #         batter_dict[player]["ducks"] = batter_dict[player].get("ducks", 0) + match_dict[player]["ducks"]

    #         # highest score
    #         batter_dict[player]["highest_score"] = max(batter_dict[player].get("highest_score", 0), match_dict[player]["runs"])
    # print(failed)
            
    # with open(os.getcwd() + '\\..\\output\\json_output\\t20i_batter_agg.json', 'w') as f:
    #     json.dump(batter_dict, f)
