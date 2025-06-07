# TEAMZYRO/IMPORT/module/nguess.py
import time
import logging
import random
import re
import asyncio
from html import escape
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant
from motor.motor_asyncio import AsyncIOMotorClient
from cachetools import TTLCache, LRUCache
from config import *

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
LOGGER = logging.getLogger(__name__)

# Non-command filter
def not_command(_, __, message):
    return message.text and not message.text.startswith('/')

not_command_filter = filters.create(not_command)

async def react_to_message(chat_id, message_id, bot_token):
    try:
        random_emoji = random.choice(emojis)
        url = f'https://api.telegram.org/bot{bot_token}/setMessageReaction'
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'reaction': [{"type": "emoji", "emoji": random_emoji}]
        }
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: requests.post(url, json=params))
        if response.status_code != 200:
            LOGGER.warning(f"Failed to set reaction. Status code: {response.status_code}")
    except Exception as e:
        LOGGER.error(f"Error setting reaction: {e}")

async def get_random_character():
    try:
        total_characters = await collection.count_documents({})
        if total_characters == 0:
            LOGGER.warning("No characters found in the database.")
            return None
        random_skip = random.randint(0, total_characters - 1)
        random_character = await collection.find_one(skip=random_skip)
        if not random_character:
            LOGGER.warning("Failed to fetch random character.")
            return None
        character_cache[str(random_character["_id"])] = random_character
        if not hasattr(get_random_character, "recent_characters"):
            get_random_character.recent_characters = []
        for _ in range(3):
            if str(random_character["_id"]) in get_random_character.recent_characters:
                random_skip = random.randint(0, total_characters - 1)
                random_character = await collection.find_one(skip=random_skip)
                if random_character:
                    character_cache[str(random_character["_id"])] = random_character
            else:
                break
        get_random_character.recent_characters.append(str(random_character["_id"]))
        if len(get_random_character.recent_characters) > 10:
            get_random_character.recent_characters.pop(0)
        return random_character
    except Exception as e:
        LOGGER.error(f"Error fetching random character: {e}")
        return None


async def get_fresh_character(chat_id):
    if not hasattr(get_fresh_character, "recent_by_chat"):
        get_fresh_character.recent_by_chat = {}
    if chat_id not in get_fresh_character.recent_by_chat:
        get_fresh_character.recent_by_chat[chat_id] = []
    for _ in range(5):
        character = await get_random_character()
        if not character:
            return None
        if character["_id"] not in get_fresh_character.recent_by_chat[chat_id]:
            get_fresh_character.recent_by_chat[chat_id].append(character["_id"])
            if len(get_fresh_character.recent_by_chat[chat_id]) > 20:
                get_fresh_character.recent_by_chat[chat_id].pop(0)
            return character
    return character

async def get_user_data(user_id):
    cache_key = f"user_{user_id}"
    if cache_key in user_cache:
        return user_cache[cache_key]
    user = await user_collection.find_one({"id": user_id})
    if user:
        user_cache[cache_key] = user
    return user

async def update_user_balance(user_id, coins_to_add):
    try:
        cache_key = f"user_{user_id}"
        if cache_key in user_cache:
            user = user_cache[cache_key]
            new_balance = user.get("balance", 0) + coins_to_add
            user["balance"] = new_balance
            user_cache[cache_key] = user
        await user_collection.update_one(
            {"id": user_id},
            {"$inc": {"balance": coins_to_add}},
            upsert=True
        )
    except Exception as e:
        LOGGER.error(f"Error updating user balance: {e}")

async def send_character(message, character):
    try:
        await message.reply_photo(
            photo=character["img_url"],
            caption="✨ Guess the character's name! \n\n⏳ You have 5 minutes to guess.",
        )
    except KeyError as e:
        LOGGER.error(f"Missing key in character data (ID: {character.get('id', 'Unknown ID')}): {e}")
        await message.reply("⚠️ Character data is incomplete. /nguess")
    except Exception as e:
        LOGGER.error(f"Error sending image: {e}")
        await message.reply("⚠️ Unable to send the character image. /nguess")

def register(app):
    @app.on_message(filters.command("nguess") & filters.group)
    async def start_nguess(client: Client, message: Message):
        from config import BOT_TOKEN
        chat_id = message.chat.id
        user_id = message.from_user.id

        # Check if the group is allowed
        if chat_id not in GROUP_IDS:
            await message.reply("❌ This command only works in the main group chat!")
            return

        # Start a new session
        random_character = await get_fresh_character(chat_id)
        if not random_character:
            await message.reply("⚠️ Error fetching character. Please try again later.")
            return

        ongoing_sessions[chat_id] = {
            "current_character": random_character,
            "start_time": time.time(),
            "guesses": {},
            "guessed": False
        }
        await send_character(message, random_character)

    @app.on_message(filters.text & not_command_filter & chat_filter)
    async def handle_guess(client: Client, message: Message):
        from config import BOT_TOKEN
        chat_id = message.chat.id
        user_id = message.from_user.id

        if chat_id not in ongoing_sessions or "current_character" not in ongoing_sessions[chat_id]:
            return

        session = ongoing_sessions[chat_id]
        current_character = session["current_character"]

        if "name" not in current_character:
            LOGGER.error(f"Character data missing 'name' key: {current_character}")
            return

        if time.time() - session["start_time"] > GUESS_TIMEOUT and not session["guessed"]:
            await message.reply("⏳ Time's up! Moving to the next character.")
            next_character = await get_fresh_character(chat_id)
            if next_character:
                ongoing_sessions[chat_id] = {
                    "current_character": next_character,
                    "start_time": time.time(),
                    "guesses": {},
                    "guessed": False
                }
                await send_character(message, next_character)
            return

        if session["guessed"]:
            return

        guess = message.text.strip().lower()
        correct_name = current_character["name"].strip().lower()

        if re.search(r'\b' + re.escape(guess) + r'\b', correct_name):
            session["guessed"] = True
            asyncio.create_task(react_to_message(chat_id, message.id, BOT_TOKEN))
            if chat_id in streak_data:
                streak_data[chat_id]["current_streak"] += 1
                streak_data[chat_id]["last_correct_user"] = user_id
                current_streak = streak_data[chat_id]["current_streak"]
            else:
                streak_data[chat_id] = {"current_streak": 1, "last_correct_user": user_id}
                current_streak = 1
            await update_user_balance(user_id, 20)
            await message.reply(
                f"🎉 Correct! You've earned 20 coins!\n"
                f"Current Streak in this group: {current_streak}! 🎉"
            )
            if current_streak in [50, 100]:
                reward = 1000 if current_streak == 50 else 2000
                await update_user_balance(streak_data[chat_id]["last_correct_user"], reward)
                await message.reply(
                    f"🏆 Streak {current_streak} achieved in this group by "
                    f"[User](tg://user?id={streak_data[chat_id]['last_correct_user']})! 🎉\n"
                    f"They've been rewarded with {reward} coins! 💰"
                )
                streak_data[chat_id]["current_streak"] = 0
                streak_data[chat_id]["last_correct_user"] = None
            next_character = await get_fresh_character(chat_id)
            if next_character:
                ongoing_sessions[chat_id] = {
                    "current_character": next_character,
                    "start_time": time.time(),
                    "guesses": {},
                    "guessed": False
                }
                await send_character(message, next_character)

    @app.on_message(filters.command("nguess") & filters.private)
    async def nguess_dm_block(client: Client, message: Message):
        await message.reply("❌ This command can only be used in groups!")
