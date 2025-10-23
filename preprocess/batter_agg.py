import os
import uuid
import json
from collections import defaultdict

def process_batter_match(match_dict=None):
    """
    takes match data and aggregates stats for each batter per match
    """

    balls = defaultdict(int)
    runs = defaultdict(int)
    wickets = defaultdict(int)
    fours = defaultdict(int)
    sixes = defaultdict(int)
    dots = defaultdict(int)
    triples = defaultdict(int)
    doubles = defaultdict(int)
    singles = defaultdict(int)
    innings = match_dict['innings']

    # get the gender
    gender = match_dict["info"]["gender"]

    # add a match played for each player
    matches = defaultdict(int)
    for team in match_dict["info"]["players"]:
        for i in match_dict["info"]["players"][team]:
            matches[i+'|'+team] += 1

    # one inning per team
    for inning in innings:
        team_name = inning["team"]
        for over in inning["overs"]:
            for delivery in over["deliveries"]:
                batter = delivery["batter"]

                # ball faced increment
                balls[batter + '|' + team_name] += 1

                # runs scored increment
                runs[batter + '|' + team_name] += delivery["runs"]["batter"]

                # was there a wicket
                if "wickets" in delivery:
                    wickets[batter + '|' + team_name] += 1
                
                # how many runs were scored
                if delivery["runs"]["batter"] == 4:
                    fours[batter + '|' + team_name] += 1

                elif delivery["runs"]["batter"] == 6:
                    sixes[batter + '|' + team_name] += 1

                elif delivery["runs"]["batter"] == 3:
                    triples[batter + '|' + team_name] += 1

                elif delivery["runs"]["batter"] == 2:
                    doubles[batter + '|' + team_name] += 1

                elif delivery["runs"]["batter"] == 1:
                    singles[batter + '|' + team_name] += 1

                elif delivery["runs"]["batter"] == 0 and delivery["runs"]["total"] == 0:
                    dots[batter + '|' + team_name] += 1
    
    return {"balls": balls, "runs": runs, "wickets": wickets, "sixes": sixes, 
            "fours": fours, "triples": triples, "doubles": doubles, 
            "singles": singles, "dots": dots, "matches": matches, "gender": gender} #balls, runs, wickets, sixes, fours, triples, doubles, singles, dots