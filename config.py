import os
from pyrogram import filters
from motor.motor_asyncio import AsyncIOMotorClient
from cachetools import TTLCache, LRUCache

API_ID = int(os.getenv("API_ID","37467897"))
API_HASH = os.getenv("API_HASH", "b1c9ba3d6180a099e35d6498d8434bf0")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://knight4563:knight4563@cluster0.a5br0se.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
GROUP_IDS = [int(gid.strip()) for gid in os.getenv("GROUP_IDS", "-1003228624224").split(",")]
START_PIC = os.getenv("START_IMG", "https://files.catbox.moe/1hoql3.jpg")

START_MESSAGE = """
🌟 Wᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ Aɴɪᴍᴇ Cʜᴀʀᴀᴄᴛᴇʀ Gᴜᴇssɪɴɢ Bᴏᴛ! 🌟

💗Gᴇᴛ ʀᴇᴀᴅʏ ᴛᴏ ᴛᴇsᴛ ʏᴏᴜʀ ᴀɴɪᴍᴇ ᴋɴᴏᴡʟᴇᴅɢᴇ ɪɴ ᴀɴ ᴇxᴄɪᴛɪɴɢ ɢᴜᴇssɪɴɢ ɢᴀᴍᴇ! 🎮  
🗻Gᴜᴇss ᴛʜᴇ ᴀɴɪᴍᴇ ᴄʜᴀʀᴀᴄᴛᴇʀs ғʀᴏᴍ ɪᴍᴀɢᴇs ɪɴ ᴏᴜʀ sᴜᴘᴘᴏʀᴛᴇᴅ ɢʀᴏᴜᴘs ᴀɴᴅ ᴇᴀʀɴ ᴄᴏɪɴs ғᴏʀ ᴇᴠᴇʀʏ ᴄᴏʀʀᴇᴄᴛ ᴀɴsᴡᴇʀ! 💰  

💞Tʜɪs ʙᴏᴛ ɪs ᴏᴘᴇɴ-sᴏᴜʀᴄᴇ, ʙᴜɪʟᴛ ᴡɪᴛʜ ❤️ ʙʏ ᴛʜᴇ ᴄᴏᴍᴍᴜɴɪᴛʏ ғᴏʀ ᴀɴɪᴍᴇ ғᴀɴs ʟɪᴋᴇ ʏᴏᴜ! Jᴏɪɴ ᴛʜᴇ ғᴜɴ, ᴛʀᴀᴄᴋ ʏᴏᴜʀ sᴛʀᴇᴀᴋs, ᴀɴᴅ ᴄʟɪᴍʙ ᴛʜᴇ ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅs! 🏆  

👇 Usᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ʟᴇᴀʀɴ ᴍᴏʀᴇ ᴏʀ sᴛᴀʀᴛ ᴘʟᴀʏɪɴɢ!
- 🥳Usᴇ /ɴɢᴜᴇss ɪɴ ᴀ sᴜᴘᴘᴏʀᴛᴇᴅ ɢʀᴏᴜᴘ ᴛᴏ ʙᴇɢɪɴ.
- ☃️Jᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ғᴏʀ ɴᴇᴡs ᴀɴᴅ ᴜᴘᴅᴀᴛᴇs!
- 💯Nᴇᴇᴅ ʜᴇʟᴘ? Hɪᴛ ᴛʜᴇ Hᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀ.

🔍Bᴏᴛ Vᴇʀsɪᴏɴ: 𝟸.𝟶  
🥀**ᴍᴀᴅᴇ ʙʏ💗:** [ ✦ sᴇɢғᴀᴜʟᴛᴇᴅ ❕](https://t.me/owner_of_itachi)
| 🌙 Pᴏᴡᴇʀᴇᴅ ʙʏ [˹ Uᴘᴘᴇʀ ᴍᴏᴏɴ ᴜᴘᴅᴀᴛᴇs ˼ 🎧](https://t.me/dark_musictm)
"""

not_command_filter = filters.create(lambda _, __, msg: msg.text and not msg.text.startswith('/'))

COOLDOWN_PERIOD = 4 * 60 * 60
GUESS_TIMEOUT = 5 * 60
MAX_GUESSES = 1000000

client_ddw = AsyncIOMotorClient(MONGO_URL, maxPoolSize=10)
db = client_ddw['hinata_waifu']
user_collection = db['gamimg_user_collection']
collection = db['gaming_anime_characters']

character_cache = LRUCache(maxsize=100)
user_cache = TTLCache(maxsize=1000, ttl=3600)

ongoing_sessions = {}
user_total_guesses = {}
streak_data = {group_id: {"current_streak": 0, "last_correct_user": None} for group_id in GROUP_IDS}

emojis = ["👍", "😘", "❤️", "🔥", "🥰", "🤩", "💘", "😏", "🤯", "⚡️", "🏆", "🤭", "🎉"]

chat_filter = filters.chat(GROUP_IDS)
