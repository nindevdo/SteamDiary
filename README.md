<h1 align="center">🎮 SteamDiary 📅</h1>
<h2 align="center">Track your Steam gameplay & achievements!</h2>  
<p align="center">
  <img src="./img/banner.png" alt="steamdiary banner" width="100%" height="auto"/>
</p>

<h4 align="center">SteamDiary integrates with <b>google calendar</b> to log your <b>playtime⌛</b> & <b>🏆achievements</b> </br>never forget your epic gaming sessions again!</h4>

---
## 🎮 The Backstory of SteamDiary: From SaaS to Open Source

It all started with a simple idea: What if you could track your Steam gaming history in a calendar, like a personal gaming diary?

I envisioned a SaaS product that would:

✅ Automatically log your playtime into Google Calendar.

✅ Keep track of achievements and session durations.

✅ Give players a clear timeline of their gaming history.

I thought it was a no-brainer. Steam already had an API, and the idea of a "Steam activity tracker" sounded like something people would actually use.
### 🚧 The Steam API Wall
As I started digging into Steam's API, I quickly hit a major roadblock:
Steam doesn’t make personal user data easily accessible.
Unlike other modern platforms, there’s no OAuth-based API for users to grant access to their playtime, achievements, or game stats dynamically.

Instead, Steam forces each user to manually generate an API key, which makes automation nearly impossible for a SaaS business model.

I realized that without an official way to authenticate users dynamically, my SaaS idea was dead in the water.
### 🔥 The Pivot: Open Sourcing SteamDiary
At this point, I had two choices:
- Abandon the project and move on.
- Open source it and let others use it however they want.

Since the concept was already built and working, I figured:
"Why not just give it away?"

So I open-sourced SteamDiary, allowing:

- Anyone to run it on their own.
- Developers to contribute and improve it.
- Gamers to log their playtime, even if Steam doesn’t officially support it.

Now, SteamDiary is a fully open-source project, available for free on GitHub. No subscriptions, no restrictions—just pure automation for those who want it.
💡 What’s Next?

Even though I abandoned the SaaS model, I’m still improving SteamDiary.
- ✅ Making setup easier so non-tech users can deploy it quickly.
- ✅ Adding better logging & UI enhancements for tracking game sessions.
- ✅ Exploring potential workarounds for getting more Steam data.

If Steam ever opens up proper authentication, maybe I'll revisit the SaaS model. But for now, SteamDiary is for the community.

## 🚀 features  

✅ **automated logging** – adds events to your **google calendar** for every session you play.  
🏅 **achievement tracking** – logs achievements earned as calendar events, so you can flex your progress.  
🛠️ **easy setup** – just connect steam & google calendar, and you’re good to go!  

---

## 🔧 prerequisites  

before setting up **steamdiary**, make sure you have:  

🔑 **[steam api key](https://steamcommunity.com/dev/apikey)** – required to fetch your gameplay data.  
☁️ **google cloud project** – to access **google calendar api**.  
📅 **google calendar** – a calendar where steamdiary will log events.  
🐳 **docker & docker compose** – for easy deployment.  

---

## ⚙️ setup instructions  
[![Watch the video](https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

### 1️⃣ get your steam api key  

1. visit the **[steam api key registration page](https://steamcommunity.com/dev/apikey)**.  
2. log in with your **steam account**.  
3. register a **new api key** and **save it** for later.  

---

### 2️⃣ set up google calendar api  

#### 🌟 a) create a google cloud project  

1. open the **[google cloud console](https://console.cloud.google.com/)**.  
2. click **"select a project"** → **"new project"**.  
3. enter a project name & hit **create**.  

#### 📅 b) enable google calendar api  

1. in the **[api library](https://console.cloud.google.com/apis/library)**, search for **google calendar api**.  
2. click **"enable"**.  

#### 🔐 c) create a service account  

1. go to **apis & services** → **credentials**.  
2. click **"create credentials"** → **"service account"**.  
3. give it a name & hit **"create and continue"**.  
4. assign the role **project → editor** → **continue**.  
5. click **done**.  

#### 🔑 d) generate a service account key  

1. in **credentials**, click on your **newly created service account**.  
2. open the **keys** tab → **add key** → **create new key**.  
3. select **json** and click **create** (this will download the key file).  

#### 🔄 e) share google calendar with your service account  

1. open **[google calendar](https://calendar.google.com/)**.  
2. create a **new calendar** dedicated to steamdiary logs.  
3. in the **calendar settings**, under **"share with specific people"**, add the **service account email** with **"make changes to events"** permission.  
4. copy the **calendar id** (you’ll need this later).  

---

### 3️⃣ configure environment variables  

1. **clone the repository**:  

   ```bash
   git clone https://github.com/nindevdo/steamdiary.git
   cd steamdiary

place the downloaded service account json key file in the project's root directory.

create a .env file in the root directory with the following variables:

```
    google_calendar_id=your_calendar_id
    google_service_account_file=path_to_your_service_account_key.json
    steam_api_key=your_steam_api_key
    steam_user_id=your_steam_user_id
    time_interval=interval_in_minutes
```


### 4. deploy with docker

1. ensure docker and docker compose are installed.
2. build and run the docker container:
```
    docker-compose up --build
```

steamdiary will now monitor your steam gameplay and log events to your google calendar.
contributing

we welcome contributions! feel free to submit issues and pull requests.
