from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import *
from pyrogram import enums
from pyrogram.types import InputMediaPhoto

def register(app):
    @app.on_message(filters.command("start") & filters.private)
    async def start_command(client: Client, message: Message):
        # Define inline buttons
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Developer 👨‍💻", url="https://t.me/MrZyro"),
                InlineKeyboardButton("Update Channel 📢", url="https://t.me/Zyro_Network")
            ],
            [
                InlineKeyboardButton("Help ❓", callback_data="help_command"),
                InlineKeyboardButton("Repo 💡", url="https://github.com/MrZyro/ZyroNguess")
            ]
        ])

        # Send start message with photo and buttons
        await message.reply_photo(
            photo=START_PIC,
            caption=START_MESSAGE,
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=keyboard
        )

    # Handle the Help button callback
    @app.on_callback_query(filters.regex("help_command"))
    async def help_callback(client: Client, callback_query):
        help_text = """
**Help - Anime Character Guessing Bot** 🛠️

Here's how to use the bot:
1. **Join the Required Channel**: Ensure you've joined [TEAM ZYRO](https://t.me/) to use the bot.
2. **Start a Game**: Use `/nguess` in one of our supported groups to start guessing anime characters.
3. **Guess the Character**: When an image is posted, type the character's name to guess. You have 5 minutes per round!
4. **Earn Rewards**: Correct guesses earn 20 coins, and streaks (50 or 100 correct guesses) give bonus rewards (1000 or 2000 coins).
5. **Cooldowns**: Max 1,000,000 guesses before a 4-hour cooldown.

**Need more help?** Contact [Mr Zyro](https://t.me/MeZyro) or join [TEAM ZYRO](https://t.me/Zyro_Network) for support!
        """
        await callback_query.message.edit_text(
            text=help_text,
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Back to Start", callback_data="back_to_start")]
            ])
        )

    # Handle the Back to Start button callback
    @app.on_callback_query(filters.regex("back_to_start"))
    async def back_to_start_callback(client: Client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Developer 👨‍💻", url="https://t.me/xeno_kakarot"),
                InlineKeyboardButton("Update Channel 📢", url="https://t.me/PiratesMainchat")
            ],
            [
                InlineKeyboardButton("Help ❓", callback_data="help_command"),
                InlineKeyboardButton("Repo 💡", url="https://github.com/MrZyro/ZyroNguess")
            ]
        ])
        await callback_query.message.edit_media(
            media=InputMediaPhoto(
                media=START_PIC,
                caption=START_MESSAGE,
                parse_mode=enums.ParseMode.MARKDOWN
            ),
            reply_markup=keyboard
        )
        await callback_query.answer()



