# TEAMZYRO/IMPORT/module/start.py
from pyrogram import Client, filters
from pyrogram.types import Message
from config import GOKU_PIC, GOKU_TEXT

def register(app):
    @app.on_message(filters.command("start") & filters.private)
    async def start_command(client: Client, message: Message):
        await message.reply_photo(
            photo=START_PIC,
            caption=START_TEXT,
            parse_mode="markdown"
        )
