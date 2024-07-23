# SteamDiary

SteamDiary integrate with Google Calendar adding time played and achievements
A simple application that can be used to add google calendar events for game time played for all steam games.

![calendar event](./img/calendar_event.png)

# @T&Ts:

- This will only log time played while the user is online. However, if you want to be sneaky and have two machines with Steam installed then you can go invisible on the machine you're gaming on and online on the one you are not.

# Prerequisites:

- Steam API key
- Google Calendar API key
- Google Calendar ID
- docker-compose & docker
- Google Cloud Project

# How to use:

- Clone the repo
- Install docker and docker-compose
- Create a `.env` file in the root of the project
- Add the following environment variables to the `.env` file
  - GOOGLE_CALENDAR_ID
  - GOOGLE_SERVICE_ACCOUNT_FILE
  - STEAM_API_KEY
  - STEAM_USER_ID
  - TIME_INTERVAL
- Setup a google cloud project and enable the google calendar API
- Create a service account and download the json file
- Create a new calendar
  - go to calendar settings and share the calendar with the service account email
  - note down the calendar id
- Add the json file to the root of the project
- export your environment variables set in docker-compose file
- Run the program and `docker-compose up`
- benefit...
