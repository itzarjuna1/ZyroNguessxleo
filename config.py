import os
from pyrogram import filters
from motor.motor_asyncio import AsyncIOMotorClient
from cachetools import TTLCache, LRUCache

API_ID = int(os.getenv("API_ID", "26208465"))
API_HASH = os.getenv("API_HASH", "bd4e2fe9c30486282417cdf9a93333b2")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7700977444:AAFF2yZB98wlEYnOGrjjvg5IFdXPlx1ouDY")
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://harshmanjhi1801:webapp@cluster0.xxwc4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
GROUP_IDS = os.getenv("GROUP_IDS", "-1002056007523, -1002056007523")
START_IMG = os.getenv("START_IMG", "")

START_TEXT = """
none
"""

not_command_filter = filters.create(lambda _, __, msg: msg.text and not msg.text.startswith('/'))

COOLDOWN_PERIOD = 4 * 60 * 60
GUESS_TIMEOUT = 5 * 60
MAX_GUESSES = 1000000

# Rewards
COINS_PER_CORRECT = 20
BONUS_50 = 1000
BONUS_100 = 2000

client_ddw = AsyncIOMotorClient(MONGO_URL, maxPoolSize=10)
db = client_ddw['hinata_waifu']
user_collection = db['gamimg_user_collection']
collection = db['gaming_anime_characters']

character_cache = LRUCache(maxsize=100)
user_cache = TTLCache(maxsize=1000, ttl=3600)

# Session and streak data
ongoing_sessions = {}
user_total_guesses = {}
streak_data = {group_id: {"current_streak": 0, "last_correct_user": None} for group_id in GROUP_IDS}

# Reaction emojis
emojis = ["👍", "😘", "❤️", "🔥", "🥰", "🤩", "💘", "😏", "🤯", "⚡️", "🏆", "🤭", "🎉"]

# Create chat filter
chat_filter = filters.chat(GROUP_IDS)
