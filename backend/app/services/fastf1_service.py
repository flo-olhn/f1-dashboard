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
    races = []
    for event in get_events(season)['passed_events']:
        round_number = event['RoundNumber']
        session = ff1.get_session(season, round_number, 'R')
        session.load(telemetry=False, laps=False, weather=False, messages=False)
        session.results['Position'] = np.where(np.isnan(session.results['Position']), None, session.results['Position'])
        races.append(session.results)

    results = pd.concat(races)
    summary = results.groupby(['DriverNumber', 'Abbreviation']).agg({'Points': 'sum', 'Position': list}).reset_index()
    summary = summary.sort_values(by='Points', ascending=False)

    return {
        "season": season,
        "driver_standings": summary.to_dict(orient='records'),
    }

def get_constructor_standings(season: int = date.today().year):
    pass

