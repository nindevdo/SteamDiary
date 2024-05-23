import requests
import os
import json
import time

#from google.oauth2 import service_account
#from googleapiclient.discovery import build
#from datetime import datetime, timedelta

user_id = os.getenv("STEAM_USER_ID")
api_key = os.getenv("STEAM_API_KEY")

#service_account_file = 'path/to/service_account_file.json'  # Path to your service account JSON file
#calendar_id = 'Your_Calendar_ID'

# Get games for user
def get_games_for_user(user_id):
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={api_key}&steamid={user_id}&format=json"

    response = requests.get(url)
    if response.status_code == 200:
        games = response.json()["response"]["games"]
        return games
    else:
        print("Failed to retrieve games for user.")
        return []

# Get recently played games for user
def get_recently_played_games_for_user(user_id):
    url = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={api_key}&steamid={user_id}&format=json"

    response = requests.get(url)
    if response.status_code == 200:
        games = response.json()["response"]["games"]
        return games
    else:
        print("Failed to retrieve recently played games for user.")
        return []

# Use GetPlayerSummaries to get user information for gameid for realtime in game time tracking for total time played
def get_player_summaries(user_id):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&steamids={user_id}&format=json"

    response = requests.get(url)
    if response.status_code == 200:
        user = response.json()["response"]["players"][0]
        game = get_game_name(user.get('gameid'))
        print(f"User {user.get('personaname')} is currently playing game {game}")
        return user
    else:
        print("Failed to retrieve user information.")
        return {}


def main(user_id):
    previous_gameid = None
    start_time = None
    total_time_played = {}  # Dictionary to store total time played for each game
    while True:
        try:
            data = get_player_summaries(user_id)  

            # Extract gameid from response data
            current_gameid = data.get('gameid')

            # Check if gameid has changed
            if current_gameid != previous_gameid:
                # If this is not the first game, calculate the duration of the previous game
                if start_time is not None:
                    end_time = time.time()
                    duration = end_time - start_time
                    gamename = get_game_name(previous_gameid)
                    print(f"Game {gamename} ended at {end_time}. Duration: {duration} seconds")
                    # Update total time played for the previous game
                    total_time_played[gamename] = total_time_played.get(gamename, 0) + duration
                    add_event_to_calendar(gamename, duration, start_time, end_time)

                
                # Log beginning time for the new game
                start_time = time.time()
                gamename = get_game_name(current_gameid)
                print(f"Game {gamename} started at {start_time}")

                # Update previous_gameid
                previous_gameid = current_gameid

            # Wait for 1 minute
            time.sleep(60)

        except Exception as e:
            print("Error occurred:", e)

            # Wait for 1 minute before retrying
            time.sleep(60)

# Get the game name by game id
def get_game_name(game_id):
    url = f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={api_key}&appid={game_id}&format=json"

    response = requests.get(url)
    if response.status_code == 200:
        game = response.json()["game"]
        return game.get('gameName')
    else:
        print("Failed to retrieve game information.")
        return None
 

def add_event_to_calendar(gamename, duration, start_time, end_time):
    # Authenticate with the Google Calendar API using a service account

    credentials = service_account.Credentials.from_service_account_file(service_account_file)
    service = build('calendar', 'v3', credentials=credentials)
    event_summary = f"🧙 {gamename}"
    event_description = f"SteamDiary entry for {gamename} with {duration} time played."
    print(event_description)
    return
    # Create event body
    event = {
        'summary': event_summary,
        'description': event_description,
        'start': {
            'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Your_Timezone_Here',  # e.g., 'America/New_York'
        },
        'end': {
            'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Your_Timezone_Here',  # e.g., 'America/New_York'
        },
    }

    # Add event to calendar
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


if __name__ == "__main__":
    main(user_id)