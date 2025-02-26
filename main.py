import datetime
import json
import logging
import os
import pytz
import requests
import time
import humanize

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

logging.basicConfig(level=logging.INFO)

user_id = os.getenv("STEAM_USER_ID")
api_key = os.getenv("STEAM_API_KEY")

calendar_id = os.getenv("GOOGLE_CALENDAR_ID")
service_account_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
credentials = Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
time_interval = int(os.getenv("TIME_INTERVAL", 60))

GENRE_genre_emoji_MAP = {
    "4X": "🌌",
    "Action": "🔥",
    "Adventure": "🏕️",
    "Anime": "🎌",
    "Battle Royale": "🏆",
    "Board Game": "🎲",
    "Building": "🏗️",
    "Bullet Hell": "💥",
    "Card & Board": "🃏",
    "Card Game": "🃏",
    "Casual": "☕",
    "City Builder": "🏙️",
    "Colony Sim": "🌐",
    "Comedy": "😂",
    "Crafting": "🔨",
    "Cyberpunk": "🦾",
    "Dating Sim": "❤️",
    "Detective": "🕵️‍♀️",
    "Dungeon Crawler": "🗝️",
    "Dystopian": "🏙️",
    "Economy": "💰",
    "Educational": "📚",
    "Espionage": "🕶️",
    "Exploration": "🧭",
    "Family Friendly": "👪",
    "Fantasy": "🐉",
    "Farming": "🌾",
    "Fighting": "🥊",
    "Fishing": "🎣",
    "Flight": "✈️",
    "Gothic": "🦇",
    "Hack & Slash": "🗡️",
    "Historical": "🏰",
    "Horror": "👻",
    "Hunting": "🏹",
    "Indie": "🎨",
    "JRPG": "🎎",
    "Life Sim": "🏡",
    "Looter Shooter": "💰🔫",
    "Lovecraftian": "🐙",
    "MMORPG": "🌐",
    "MOBA": "⚔️",
    "Management": "📈",
    "Match 3": "🔷🔶🔷",
    "Medieval": "⚔️",
    "Metroidvania": "🧩",
    "Military": "🎖️",
    "Minigames": "🎮",
    "Mining": "⛏️",
    "Multiplayer": "👥",
    "Music": "🎸",
    "Mystery": "🕵️‍♂️",
    "Narrative": "📝",
    "Noir": "🕶️",
    "Nonlinear": "🔀",
    "Open World": "🌍",
    "Party Game": "🎉",
    "Perma Death": "💀",
    "Physics": "⚙️",
    "Pinball": "🎱",
    "Pirates": "🏴‍☠️",
    "Platformer": "🦘",
    "Point & Click": "🖱️",
    "Politics": "🏛️",
    "Post-apocalyptic": "☢️",
    "Post-apocalyptic": "☢️",
    "Procedural Generation": "🔀",
    "Procedural Generation": "🔀",
    "Puzzle": "🧩",
    "Quick-Time Events": "⏩",
    "RPG": "⚔️",
    "Racing": "🏎️",
    "Real-Time": "⏱️",
    "Replay Value": "🔁",
    "Resource Management": "📊",
    "Retro": "🕹️",
    "Rhythm": "🎵",
    "Roguelike": "🎲",
    "Roguelite": "🎲",
    "Romance": "💖",
    "Sandbox": "🪵",
    "Satire": "😂",
    "Sci-Fi": "🚀",
    "Shooter": "🔫",
    "Short": "⏳",
    "Side Scroller": "➡️",
    "Silent Protagonist": "🤐",
    "Simulation": "🎛️",
    "Souls-like": "💀",
    "Space": "🌌",
    "Split Screen": "🖥️🖥️",
    "Sports": "🏆",
    "Stealth": "🕵️",
    "Steampunk": "⚙️",
    "Story Rich": "📚",
    "Strategy": "🧠",
    "Superhero": "🦸",
    "Supernatural": "🔮",
    "Surreal": "🌈",
    "Survival": "🛠️",
    "Text-Based": "📝",
    "Third-Person Shooter": "🔫",
    "Time Manipulation": "⏰",
    "Time Travel": "🕰️",
    "Top-Down Shooter": "🔝",
    "Touch-Friendly": "👆",
    "Tower Defense": "🛡️",
    "Trading": "💱",
    "Trains": "🚂",
    "Transport": "🚌",
    "Turn-Based": "🔄",
    "Twin Stick Shooter": "🎮",
    "Typing": "⌨️",
    "VR": "🕶️",
    "Vampire": "🧛",
    "Visual Novel": "📖",
    "Voice Control": "🎙️",
    "Voxel": "🔲",
    "Walking Simulator": "🚶",
    "War": "⚔️",
    "Wargame": "⚔️",
    "Web Publishing": "🌐",
    "Western": "🤠",
    "Wild West": "🤠",
    "Word Game": "🔤",
    "World War II": "🌍",
    "Zombies": "🧟",
    "Zombies": "🧟",
    "eSports": "🏅",
} #😌

def get_genre_genre_emoji(game_id):
    """Returns a string of genre_emojis for a list of game genres."""
    logging.info(f"🪓Executing {get_genre_genre_emoji.__name__} function")
    genres = get_game_genre(game_id)
    return "\n".join(f"{GENRE_genre_emoji_MAP.get(genre, '🎮')} {genre}" for genre in genres)


def get_game_genre(app_id):
    """Fetch game genre from Steam API using the app ID."""
    logging.info(f"🪓Executing {get_game_genre.__name__} function")
    url = f"http://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data[str(app_id)]["success"]:
            genres = data[str(app_id)]["data"].get("genres", [])
            return [genre["description"] for genre in genres]
        else:
            return None
    return None


# Get games for user
def get_games_for_user(user_id):
    logging.info(f"🪓Executing {get_games_for_user.__name__} function")

    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={api_key}&steamid={user_id}&format=json"

    response = requests.get(url)
    if response.status_code == 200:
        games = response.json()["response"]["games"]
        return games
    else:
        logging.info("Failed to retrieve games for user.")
        return []


# Get recently played games for user
def get_recently_played_games_for_user(user_id):
    logging.info(f"🪓Executing {get_recently_played_games_for_user.__name__} function")

    url = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={api_key}&steamid={user_id}&format=json"

    response = requests.get(url)
    if response.status_code == 200:
        games = response.json()["response"]["games"]
        return games
    else:
        logging.error("Failed to retrieve recently played games for user.")
        return []


# Use GetPlayerSummaries to get user information for gameid for realtime in game time tracking for total time played
def get_player_summaries(user_id):
    logging.info(f"🪓Executing {get_player_summaries.__name__} function")
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&steamids={user_id}&format=json"

    response = requests.get(url)
    logging.info(f"Request: {url}")
    logging.info(f"Response: {response}")
    if response.status_code == 200:
        user = response.json()["response"]["players"][0]
        logging.info(f"User: {user}")
        return user
    else:
        logging.error("Failed to retrieve user information.")
        return {}


def main(user_id):
    logging.info(f"🪓Executing {main.__name__} function")
    previous_gameid = None
    start_time = None
    total_time_played = {}  # Dictionary to store total time played for each game
    while True:
        try:
            data = get_player_summaries(user_id)
            # Extract gameid from response data
            current_gameid = data.get("gameid")
            logging.info("=============================================")
            logging.info(f"data: {data}")
            logging.info(f"Current gameid: {current_gameid}")
            logging.info(f"Previous gameid: {previous_gameid}")
            logging.info("=============================================")
            # Check if gameid has changed
            if current_gameid != previous_gameid:
            #if previous_gameid is not None and current_gameid != previous_gameid:
                # If this is not the first game, calculate the duration of the previous game
                if start_time is not None and previous_gameid is not None:
                    end_time = time.time()
                    duration = end_time - start_time
                    gamename = get_game_name(previous_gameid, data)
                    logging.info(f"Game {gamename} ended at {end_time}. Duration: {duration} seconds")
                    # Update total time played for the previous game
                    total_time_played[gamename] = (
                        total_time_played.get(gamename, 0) + duration
                    )
                    logging.info(f"Total time played for {gamename}: {total_time_played[gamename]} seconds")
                    add_event_to_calendar(gamename, previous_gameid, duration, start_time, end_time)

                # Log beginning time for the new game
                start_time = time.time()
                gamename = get_game_name(current_gameid, data)
                logging.info("=============================================")
                logging.info(f"Game {gamename} started at {start_time}")
                logging.info(f"Total time played: {humanize.naturaldelta(total_time_played)}")
                logging.info(f"Current gameid: {current_gameid}")
                logging.info(f"Previous gameid: {previous_gameid}")
                logging.info(f"Data: {data}")
                # Update previous_gameid
                previous_gameid = current_gameid
                logging.info(f"updated previous_gameid: {previous_gameid}")
                logging.info("=============================================")

            # Wait for 1 minute
            time.sleep(time_interval)

        except Exception as e:
            logging.error(f"Error occurred: {e}")
            # Wait for 1 minute before retrying
            time.sleep(time_interval)


def get_game_name(game_id, data={}):
    logging.info(f"🪓 Executing {get_game_name.__name__} function")

    url = f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={api_key}&appid={game_id}&format=json"
    response = requests.get(url)
    logging.info("----------------------------------------------------")
    logging.info(f"gameid: {game_id}")
    logging.info(f"data: {data}")
    logging.info(f"Request: {url}")
    logging.info(f"Response: {response.json()}")
    logging.info("----------------------------------------------------")
    
    if response.status_code == 200 and response.json().get("game") != {}:
        game = response.json()["game"]
        logging.info(f"Game: {game}")
        return game.get("gameName")
    elif 'response' in data and 'players' in data['response'] and len(data['response']['players']) > 0:
        gameextrainfo = data['response']['players'][0].get('gameextrainfo')
        logging.info(f"GameExtraInfo: {gameextrainfo}")
        return gameextrainfo
    elif 'steamid' in data and 'gameextrainfo' in data:
        gameextrainfo = data['gameextrainfo']
        logging.info(f"GameExtraInfo: {gameextrainfo}")
        return gameextrainfo
    else:
        return "Unknown Game"


def unix_to_iso8601(timestamp):
    logging.info(f"🪓Executing {unix_to_iso8601.__name__} function")

    """Convert Unix timestamp to ISO 8601 format."""
    return datetime.datetime.fromtimestamp(
        timestamp, tz=datetime.timezone.utc
    ).isoformat()


def add_event_to_calendar(gamename, game_id, duration, start_time, end_time):
    logging.info(f"🪓Executing {add_event_to_calendar.__name__} function")
    genre_emoji = get_genre_genre_emoji(game_id)
    time_played = humanize.naturaldelta(duration)

    service = build("calendar", "v3", credentials=credentials)

    summary = f"🎮 {gamename}"
    location = "📔 SteamDiary"
    description = f":Played {gamename} for {time_played}⌛: \n{genre_emoji}"

    event = {
        "summary": summary,
        "colorId": 1,
        "location": location,
        "description": description,
        "start": {"dateTime": unix_to_iso8601(start_time), "timeZone": "UTC"},
        "end": {"dateTime": unix_to_iso8601(end_time), "timeZone": "UTC"},
    }

    logging.info(f"➕ Adding event to calendar: {event}")
    return service.events().insert(calendarId=calendar_id, body=event).execute()


if __name__ == "__main__":
    main(user_id)
