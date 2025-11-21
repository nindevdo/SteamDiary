import datetime
import requests
import logging
import os
import time
import humanize
import json
import base64

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar"]

logging.basicConfig(level=logging.INFO)

USER_ID = os.getenv("STEAM_USER_ID")
API_KEY = os.getenv("STEAM_API_KEY")

CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "./.credentials.json")

# Check if we have base64 credentials to write to file
GOOGLE_SERVICE_ACCOUNT_JSON_B64 = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON_B64")
if GOOGLE_SERVICE_ACCOUNT_JSON_B64:
    # Decode base64 credentials and write to the expected file location
    try:
        json_str = base64.b64decode(GOOGLE_SERVICE_ACCOUNT_JSON_B64).decode('utf-8')
        with open(SERVICE_ACCOUNT_FILE, 'w') as f:
            f.write(json_str)
        logging.info(f"✅ Credentials written to {SERVICE_ACCOUNT_FILE} from environment variable")
    except Exception as e:
        logging.error(f"❌ Failed to write credentials from environment variable: {e}")
        raise

# Use the service account file (either existing or just created from env var)
if os.path.exists(SERVICE_ACCOUNT_FILE):
    CREDENTIALS = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
else:
    raise ValueError(f"Credentials file not found at {SERVICE_ACCOUNT_FILE} and no GOOGLE_SERVICE_ACCOUNT_JSON_B64 environment variable provided")

CAL_SERVICE = build("calendar", "v3", credentials=CREDENTIALS)
STEAM_OPENID_URL = "https://steamcommunity.com/openid/login"
STEAM_API_KEY_URL = "https://steamcommunity.com/dev/apikey"
TIME_INTERVAL = int(os.getenv("TIME_INTERVAL", 60))

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
}  # 😌


def get_genre_genre_emoji(game_id):
    """Returns a string of genre_emojis for a list of game genres."""
    logging.info(f"🪓Executing {get_genre_genre_emoji.__name__} function")
    genres = get_game_genre(game_id)
    if not genres:
        return "🎮 No genre data available"
    return "\n".join(
        f"{GENRE_genre_emoji_MAP.get(genre, '🎮')} {genre}" for genre in genres
    )


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
def get_games_for_user(USER_ID):
    logging.info(f"🪓Executing {get_games_for_user.__name__} function")

    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={API_KEY}&steamid={USER_ID}&format=json"

    response = requests.get(url)
    if response.status_code == 200:
        games = response.json()["response"]["games"]
        return games
    else:
        logging.info("Failed to retrieve games for user.")
        return []


# Get recently played games for user
def get_recently_played_games_for_user(USER_ID):
    logging.info(f"🪓Executing {get_recently_played_games_for_user.__name__} function")

    url = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={API_KEY}&steamid={USER_ID}&format=json"

    response = requests.get(url)
    if response.status_code == 200:
        games = response.json()["response"]["games"]
        return games
    else:
        logging.error("Failed to retrieve recently played games for user.")
        return []


# Use GetPlayerSummaries to get user information for gameid for realtime in game time tracking for total time played
def get_player_summaries(USER_ID):
    logging.info(f"🪓Executing {get_player_summaries.__name__} function")
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={API_KEY}&steamids={USER_ID}&format=json"

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


def get_game_name(game_id, data={}):
    logging.info(f"🪓 Executing {get_game_name.__name__} function")

    url = f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={API_KEY}&appid={game_id}&format=json"
    response = requests.get(url)

    if response.status_code == 200 and response.json().get("game") != {}:
        game = response.json()["game"]
        return game.get("gameName")
    elif (
        "response" in data
        and "players" in data["response"]
        and len(data["response"]["players"]) > 0
    ):
        gameextrainfo = data["response"]["players"][0].get("gameextrainfo")
        return gameextrainfo
    elif "steamid" in data and "gameextrainfo" in data:
        gameextrainfo = data["gameextrainfo"]
        return gameextrainfo
    else:
        return "Unknown Game"


def unix_to_iso8601(timestamp):
    logging.info(f"🪓Executing {unix_to_iso8601.__name__} function")

    """Convert Unix timestamp to ISO 8601 format."""
    return datetime.datetime.fromtimestamp(
        timestamp, tz=datetime.timezone.utc
    ).isoformat()


def get_achievement_schema(app_id):
    """Fetch achievement names and descriptions."""
    url = f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/"
    params = {"key": API_KEY, "appid": app_id}

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {}

    data = response.json()
    achievements = (
        data.get("game", {}).get("availableGameStats", {}).get("achievements", [])
    )

    # Create a mapping of apiname → (real name, description)
    return {
        ach["name"]: (ach["displayName"], ach["description"]) for ach in achievements
    }


def get_player_achievements(steam_id, app_id):
    """Fetch player achievements and match with real names."""
    url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {"key": API_KEY, "steamid": steam_id, "appid": app_id}

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"Error fetching data: {response.status_code}"

    data = response.json()

    if not data.get("playerstats") or "achievements" not in data["playerstats"]:
        return "No achievements data found."

    achievements = data["playerstats"]["achievements"]

    # Get achievement names from schema
    achievement_names = get_achievement_schema(app_id)

    for achievement in achievements:
        apiname = achievement["apiname"]
        unlocked = achievement["achieved"] == 1
        unlock_time = achievement["unlocktime"]

        # Convert timestamp to human-readable format if unlocked
        readable_time = (
            datetime.datetime.utcfromtimestamp(unlock_time).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if unlocked
            else "Not unlocked"
        )

        # Get real name and description safely
        achievement_info = achievement_names.get(apiname, None)

        if achievement_info:
            real_name, description = achievement_info
        else:
            real_name, description = apiname, "No description available"

        print(
            f"🏆 {real_name} - {('✅ Unlocked' if unlocked else '❌ Locked')} at {readable_time}"
        )
        print(f"   📝 {description}\n")


def get_unlocked_achievements(steam_id, app_id):
    """Fetch only unlocked achievements with timestamps."""
    url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {"key": API_KEY, "steamid": steam_id, "appid": app_id}

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"⚠️ Error fetching achievements: {response.status_code}")
        return []

    data = response.json()
    achievements = data.get("playerstats", {}).get("achievements", [])

    return [
        {"apiname": ach["apiname"], "unlocktime": ach["unlocktime"]}
        for ach in achievements
        if ach["achieved"] == 1
    ]


def get_achievement_schema(app_id):
    """Fetch achievement names & descriptions."""
    url = f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/"
    params = {"key": API_KEY, "appid": app_id}

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("⚠️ Error fetching achievement schema")
        return {}

    data = response.json()
    achievements = (
        data.get("game", {}).get("availableGameStats", {}).get("achievements", [])
    )

    return {ach["name"]: ach.get("displayName", ach["name"]) for ach in achievements}


def achievement_exists(title):
    """Check if an achievement event already exists in Google Calendar."""
    events_result = (
        CAL_SERVICE.events()
        .list(
            calendarId=CALENDAR_ID,
            q=title,  # Search by event title
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    return len(events_result.get("items", [])) > 0


def add_achievement_to_calendar(title, gamename, unlock_time):
    """Add an achievement as a Google Calendar event."""
    print(title)
    readable_time = datetime.datetime.utcfromtimestamp(unlock_time).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    print(readable_time)

    if achievement_exists(title):
        print(f"✅ Achievement '{title}' already exists in Google Calendar.")
        return

    event_time = datetime.datetime.utcfromtimestamp(unlock_time).isoformat() + "Z"

    event = {
        "summary": f"🏆 {gamename} 🔓:\n{title}",
        "description": f"🎖️ Achievement '{title}' unlocked on Steam. for {gamename}",
        "start": {"dateTime": event_time, "timeZone": "UTC"},
        "end": {"dateTime": event_time, "timeZone": "UTC"},
    }

    CAL_SERVICE.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    print(f"🎉 Added achievement '{title}' to Google Calendar for {gamename}!")


def sync_achievements_to_calendar(steam_id, gamename, app_id):
    """Fetch new achievements and add them to Google Calendar."""
    print("🔍 Checking for new achievements...")

    achievements = get_unlocked_achievements(steam_id, app_id)
    achievement_names = get_achievement_schema(app_id)

    for ach in achievements:
        apiname = ach["apiname"]
        unlock_time = ach["unlocktime"]
        title = achievement_names.get(
            apiname, apiname
        )  # Default to apiname if not found

        add_achievement_to_calendar(title, gamename, unlock_time)


# Run the script
def add_event_to_calendar(gamename, game_id, duration, start_time, end_time):
    logging.info(f"🪓Executing {add_event_to_calendar.__name__} function")
    genre_emoji = get_genre_genre_emoji(game_id)
    time_played = humanize.naturaldelta(duration)

    summary = f"🎮 {gamename}"
    location = "📔 SteamDiary"
    description = f"{gamename} for {time_played}⌛: \n{genre_emoji}"

    event = {
        "summary": summary,
        "colorId": 1,
        "location": location,
        "description": description,
        "start": {"dateTime": unix_to_iso8601(start_time), "timeZone": "UTC"},
        "end": {"dateTime": unix_to_iso8601(end_time), "timeZone": "UTC"},
    }

    logging.info(f"➕ Adding event to calendar: {event}")
    return CAL_SERVICE.events().insert(calendarId=CALENDAR_ID, body=event).execute()


def main(USER_ID):
    logging.info(f"🪓Executing {main.__name__} function")
    previous_gameid = None
    start_time = None
    total_time_played = {}  # Dictionary to store total time played for each game
    while True:
        try:
            data = get_player_summaries(USER_ID)
            # Extract gameid from response data
            current_gameid = data.get("gameid")
            logging.info("=============================================")
            logging.info(f"data: {data}")
            logging.info(f"Current gameid: {current_gameid}")
            logging.info(f"Previous gameid: {previous_gameid}")
            logging.info("=============================================")
            # Check if gameid has changed
            if current_gameid != previous_gameid:
                # if previous_gameid is not None and current_gameid != previous_gameid:
                # If this is not the first game, calculate the duration of the previous game
                if start_time is not None and previous_gameid is not None:
                    end_time = time.time()
                    duration = end_time - start_time
                    gamename = get_game_name(previous_gameid, data)
                    logging.info(
                        f"Game {gamename} ended at {end_time}. Duration: {duration} seconds"
                    )
                    # Update total time played for the previous game
                    total_time_played[gamename] = (
                        total_time_played.get(gamename, 0) + duration
                    )
                    logging.info(
                        f"Total time played for {gamename}: {total_time_played[gamename]} seconds"
                    )
                    add_event_to_calendar(
                        gamename, previous_gameid, duration, start_time, end_time
                    )
                    sync_achievements_to_calendar(USER_ID, gamename, previous_gameid)

                # Log beginning time for the new game
                start_time = time.time()
                gamename = get_game_name(current_gameid, data)
                logging.info("=============================================")
                logging.info(f"Game {gamename} started at {start_time}")
                logging.info(
                    f"Total time played: {humanize.naturaldelta(total_time_played)}"
                )
                logging.info(f"Current gameid: {current_gameid}")
                logging.info(f"Previous gameid: {previous_gameid}")
                # Update previous_gameid
                previous_gameid = current_gameid
                logging.info(f"updated previous_gameid: {previous_gameid}")
                logging.info("=============================================")

            # Wait for 1 minute
            time.sleep(TIME_INTERVAL)

        except Exception as e:
            logging.error(f"Error occurred: {e}")
            # Wait for 1 minute before retrying
            time.sleep(TIME_INTERVAL)


if __name__ == "__main__":
    main(USER_ID)
