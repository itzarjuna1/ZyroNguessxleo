import os

API_ID = int(os.getenv("API_ID", "26208465"))
API_HASH = os.getenv("API_HASH", "bd4e2fe9c30486282417cdf9a93333b2")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8171323642:AAHI9S8T8dzrjZUK_RiahzLVQDXmulO_lqI")
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://harshmanjhi1801:webapp@cluster0.xxwc4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
GROUP_IDS = os.getenv("GROUP_IDS", "-1002056007523, -1002056007523")
START_IMG = os.getenv("START_IMG", "")

START_TEXT = """
"""

not_command_filter = filters.create(lambda _, __, msg: msg.text and not msg.text.startswith('/'))

COOLDOWN_PERIOD = 4 * 60 * 60
GUESS_TIMEOUT = 5 * 60
MAX_GUESSES = 1000000

# Rewards
COINS_PER_CORRECT = 20
BONUS_50 = 1000
BONUS_100 = 2000
