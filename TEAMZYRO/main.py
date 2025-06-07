# TEAMZYRO/main.py
import asyncio
import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from TEAMZYRO.IMPORT.module import start, nguess, autoclear
from TEAMZYRO import app

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("pyrate_limiter").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

# Initialize Pyrogram client
# Register handlers from modules
start.register(app)
nguess.register(app)
autoclear.register(app)

# Start the bot
if __name__ == "__main__":
    try:
        app.run()
    except Exception as e:
        LOGGER.error(f"Error starting bot: {e}")
    print("Bot started successfully!")
