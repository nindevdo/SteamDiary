<h1 align="center">🎮SteamDiary📅</h1>
<h2 align="center">Track your Steam gameplay and achievements automatically in Google Calendar!</h2>  
<p align="center">
  <img src="./img/banner.png" alt="steamdiary banner" width="100%" height="auto"/>
</p>

<h3 align="center">SteamDiary integrates with **google calendar** to log your **playtime** and **achievements** automatically </br>never forget your epic gaming sessions again! 🏆✨ </h3>

---

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
