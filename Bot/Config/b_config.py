import os
from dotenv import load_dotenv
import time

# Load environment variables from a .env file
load_dotenv()

# Bot Token and Webhook URL
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Start Image
START_IMG = os.getenv("START_IMG", 'https://i.ibb.co/d4RQ9Df/file-1353.jpg')

# Start Time
START_TIME = int(time.time())

# Channel and Group IDs
MAIN_CHANNEL = os.getenv("MAIN_CHANNEL", '-1001824105670')
MAIN_GROUP = int(os.getenv("MAIN_GROUP", -1001857744371))
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", '-1001824105670')
LOG_CHAT = int(os.getenv("LOG_CHAT", -1002092856252))
TEMP_CHAT = int(os.getenv("TEMP_CHAT", -1002092856252))

# Sudo Users
SUDO_USERS = list(map(int, os.getenv("SUDO_USERS", "1895952308").split(',')))

# Update Channel Invite Link
UPDATE_CHANNEL_INVITE_LINK = os.getenv("UPDATE_CHANNEL_INVITE_LINK", 'https://t.me/Anime_DownLord')

# GogoAnime Credentials
GOGO_ACC = os.getenv("GOGO_ACC")
GOGO_PW = os.getenv("GOGO_PW")
