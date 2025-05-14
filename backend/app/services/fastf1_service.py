import fastf1 as ff1
import pandas as pd
import numpy as np
from datetime import date
import datetime

current_season = date.today().year


def get_events(season: int = current_season):
    if season == current_season:
        return {
            "passed_events": ff1.get_event_schedule(season, include_testing=False)[ff1.get_event_schedule(season, include_testing=False)['Session5DateUtc'] < datetime.datetime.now()].to_dict(orient='records'),
            "upcoming_events": ff1.get_event_schedule(season, include_testing=False)[ff1.get_event_schedule(season, include_testing=False)['Session5DateUtc'] > pd.to_datetime(datetime.datetime.now())].to_dict(orient='records')
        }
    else:
        return { "passed_events": ff1.get_event_schedule(season, include_testing=False).to_dict(orient='records') }

def get_driver_standings(season: int = current_season):
    global_ranking = pd.DataFrame()
    races = []
    for event in get_events(season)['passed_events']:
        round_number = event['RoundNumber']
        session = ff1.get_session(season, round_number, 'R')
        session.load(telemetry=False, laps=False, weather=False, messages=False)
        print(session.results['Position'].isna())
        # replace NaN with None
        session.results['Position'] = session.results['Position'].where(session.results['Position'].notna(), None)
        races.append(session.results)

    results = pd.concat(races)
    summary = results.groupby(['DriverNumber', 'Abbreviation']).agg({'Points': 'sum', 'Position': list}).reset_index()
    summary = summary.sort_values(by='Points', ascending=False)
    for positions in summary['Position']:
        for p in positions:
            if p.isna():
                p = None
            else:
                print(p)

    #print(summary)
    #for positions in summary['Position']:
    #    for p in positions:
    #        print(p == np.nan, p == float('nan'), p == None, p == 'nan', p == 'None')

    return {
        "season": season,
        "driver_standings": summary.to_dict(orient='records'),
    }

def get_constructor_standings(season: int = date.today().year):
    pass

