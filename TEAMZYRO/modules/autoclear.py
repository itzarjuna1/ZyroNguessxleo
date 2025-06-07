# TEAMZYRO/IMPORT/module/autoclear.py
import asyncio
import time
import logging
from pyrogram import Client

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
LOGGER = logging.getLogger(__name__)

# External variables from nguess
from config import *

async def cleanup_sessions():
    while True:
        try:
            current_time = time.time()
            for chat_id in list(ongoing_sessions.keys()):
                session = ongoing_sessions[chat_id]
                if current_time - session["start_time"] > GUESS_TIMEOUT + 60:
                    del ongoing_sessions[chat_id]
            for user_id in list(user_total_guesses.keys()):
                if current_time - user_total_guesses.get(f"{user_id}_time", 0) > COOLDOWN_PERIOD:
                    del user_total_guesses[user_id]
                    if f"{user_id}_time" in user_total_guesses:
                        del user_total_guesses[f"{user_id}_time"]
        except Exception as e:
            LOGGER.error(f"Error in cleanup task: {e}")
        await asyncio.sleep(600)

def register(app):
    app.loop.create_task(cleanup_sessions())
