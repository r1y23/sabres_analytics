import requests
import pandas as pd
import hockey_scraper
import datetime
import os

#set data directory
DATA_FOLDER = '../data/raw'

def download_historical_data(start_year: int, end_year: int, with_shifts=True):
    '''
    Downloads Historical NHL data from start_year to end_year with shifts by default
    '''
    print(f'Downloading historical data from {start_year} to {end_year}')
    hockey_scraper.scrape_seasons([start_year, end_year], with_shifts, docs_dir=DATA_FOLDER)
    print("Historical data saved in the 'raw' data folder.")

def download_games(game_ids=[], with_shifts=True):
    '''
    Downloads Historical NHL data by game ID
    '''
    hockey_scraper.scrape_games(game_ids, with_shifts, docs_dir=DATA_FOLDER)

if __name__ == "__main__":
    print("Welcome to the NHL Data Scraper!")
    print("Please select an option:")
    print("1. Download historical season data")
    print("2. Download specific game data")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == '1':
        try:
            start_year = int(input("Enter the starting year (e.g., 2010): ").strip())
            end_year = int(input("Enter the ending year (e.g., 2023): ").strip())
            with_shifts = input("Include shifts data? (yes or no): ").strip().lower() == 'yes'
            download_historical_data(start_year, end_year, with_shifts)
        except ValueError:
            print("Invalid input. Please enter valid years.")
    elif choice == '2':
        try:
            game_ids_input = input("Enter Game IDs separated by commas (e.g., 2021020001,2021020002): ").strip()
            game_ids = [int(game_id.strip()) for game_id in game_ids_input.split(',')]
            with_shifts = input("Include shifts data? (yes or no): ").strip().lower() == 'yes'
            download_games(game_ids, with_shifts)
        except ValueError:
            print("Invalid input. Please enter valid game IDs.")
    else:
        print("Invalid choice. Please restart the program and select 1 or 2.")