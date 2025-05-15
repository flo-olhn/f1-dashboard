import fastf1 as ff1
import pandas as pd
import numpy as np
from datetime import date
import datetime

current_season = date.today().year


def get_events(season: int = current_season):
    if season == current_season:
        return {
            "season": season,
            "passed_events": ff1.get_event_schedule(season, include_testing=False)[ff1.get_event_schedule(season, include_testing=False)['Session5DateUtc'] < datetime.datetime.now()].to_dict(orient='records'),
            "upcoming_events": ff1.get_event_schedule(season, include_testing=False)[ff1.get_event_schedule(season, include_testing=False)['Session5DateUtc'] > pd.to_datetime(datetime.datetime.now())].to_dict(orient='records')
        }
    else:
        return { 
            "season": season,
            "passed_events": ff1.get_event_schedule(season, include_testing=False).to_dict(orient='records') 
        }

def get_standings(season: int = current_season):
    races = []
    race_results = []
    sprints = []
    for event in get_events(season)['passed_events']:
        round_number = event['RoundNumber']

        # Sprint results
        if event['EventFormat'] in ['sprint_qualifying', 'sprint', 'sprint_shootout']:
            sprint_session = ff1.get_session(season, round_number, 'Sprint')
            sprint_session.load(telemetry=False, laps=False, weather=False, messages=False)
            
            sprint_results = sprint_session.results.copy()
            sprint_results['RoundNumber'] = round_number
            sprint_results['Position'] = np.where(np.isnan(sprint_results['Position']), None, sprint_results['Position'])
            
            # Save sprint results
            sprints.append(sprint_results)

        
        # Race results
        session = ff1.get_session(season, round_number, 'R')
        session.load(telemetry=False, laps=False, weather=False, messages=False)
        
        results_df = session.results.copy()
        results_df['RoundNumber'] = round_number
        results_df['Position'] = np.where(np.isnan(results_df['Position']), None, results_df['Position'])

        race_results.append(results_df[['DriverNumber', 'Abbreviation', 'Position', 'RoundNumber', 'TeamName']])
        races.append(session.results)

    all_results = []
    if races:
        all_results.extend(races)
    if sprints:
        all_results.extend(sprints)

    combined_results = pd.concat(all_results)

    driver_summary = combined_results.groupby(['DriverNumber', 'Abbreviation']).agg({'Points': 'sum'}).reset_index()
    driver_summary = driver_summary.sort_values(by='Points', ascending=False)

    all_race_results = pd.concat(race_results)
    position_dict = {}
    for driver in driver_summary['DriverNumber']:
        driver_results = all_race_results[all_race_results['DriverNumber'] == driver]
        positions = {int(row['RoundNumber']): row['Position'] for _, row in driver_results.iterrows()}
        position_dict[driver] = positions

    driver_summary['Positions'] = driver_summary['DriverNumber'].map(position_dict)

    team_summary = combined_results.groupby(['TeamName']).agg({'Points': 'sum'}).reset_index()
    team_summary = team_summary.sort_values(by='Points', ascending=False)

    return {
        "season": season,
        "driver_standings": driver_summary.to_dict(orient='records'),
        "team_standings": team_summary.to_dict(orient='records')
    }
