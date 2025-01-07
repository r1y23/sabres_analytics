import requests
import pandas as pd
import hockey_scraper as scraper
import datetime
import os

#set data directory
DATA_FOLDER = '../data/raw'

def download_historical_data(start_year: int, end_year: int):
    '''
    Downloads Historical NHL data from start_year to end_year
    '''
    print(f'Downloading historical data from {start_year} to {end_year}')
    scraper.scrape_games(start_year=start_year, end_year=end_year, data_format='csv', output_dir=DATA_FOLDER)
    print("Historical data saved in the 'raw' data folder.")

def download_current_data():
    '''
    Downloads current NHL game and player data from NHL API.
    '''

    base_url = 'https://api.nhle.com/stats/rest/en/'

    #Fetch team stats
    team_stats_url = f'{base_url}team/summary'
    response = requests.get(team_stats_url)

    if response.status_code == 200:
        team_data = response.json()
        df_teams = pd.DataFrame(team_data['data'])
        df_teams.to_csv(os.path.join(DATA_FOLDER, 'current_team_stats.csv'), index=False)
        print('Current team stats saved')
    else:
        print('Failed to fetch current player stats.')


def download_game_logs(start_date: str, end_date: str):
    '''
    Downloads game logs for a specific date range.
    '''
    game_logs_url = f'https://statsapi.web.nhl.com/api/v1/schedule?startDate={start_date}&endDate={end_date}'
    response = requests.get(game_logs_url)

    if response.status_code == 200:
        schedule_data = response.json()
        games = []
        for date in schedule_data['dates']:
            for game in date['games']:
                games.append({
                    'gamePk': game['gamePk'],
                    'date' : game['gameDate'],
                    'homeTeam': game['teams']['home']['team']['name'],
                    'awayTeam': game['teams']['home']['team']['name'],
                    'venue': game['venue']['name']
                })
        df_games = pd.DataFrame(games)
        df_games.to_csv(os.path.join(DATA_FOLDER, 'game_logs.csv'), index=False)
        print("Game logs saved.")
    else:
        print("Failed to fetch game logs.")

if __name__ == "__main__":
    #Historical Data (e.g., from 2010 to 2023)
    download_historical_data(start_year=2010, end_year=2023)

    #Current Season Data
    download_current_data()

    #Game Logs for the last 7 days
    today = datetime.date.today()
    one_week_ago = today - datetime.timedelta(days=7)
    download_game_logs(start_date=str(one_week_ago), end_date=str(today))