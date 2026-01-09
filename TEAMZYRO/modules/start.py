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
                InlineKeyboardButton("ᴅᴇᴠeʟᴏᴘᴇʀ 👨‍💻", url="https://t.me/uchiha_owner"),
                InlineKeyboardButton("Update Channel 📢", url="https://t.me/dark_musictm")
            ],
            [
                InlineKeyboardButton("ʜᴇʟᴘ ❓", callback_data="help_command"),
                InlineKeyboardButton("˹ Uᴘᴘᴇʀ ᴍᴏᴏɴ ᴜᴘᴅᴀᴛᴇs ˼ 🎧", url="https://t.me/snowy_hometown")
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

ʜᴇʀᴇ’ꜱ ʜᴏᴡ ᴛᴏ ᴜꜱᴇ ᴛʜᴇ ʙᴏᴛ:
ᴊᴏɪɴ ᴛʜᴇ ʀᴇQᴜɪʀᴇᴅ ᴄʜᴀɴɴᴇʟ: ᴇɴꜱᴜʀᴇ ʏᴏᴜ’ᴠᴇ ᴊᴏɪɴᴇᴅ  ᴛᴏ ᴜꜱᴇ ᴛʜᴇ ʙᴏᴛ.
ꜱᴛᴀʀᴛ ᴀ ɢᴀᴍᴇ: ᴜꜱᴇ /nguess ɪɴ ᴏɴᴇ ᴏꜰ ᴏᴜʀ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ɢʀᴏᴜᴘꜱ ᴛᴏ ꜱᴛᴀʀᴛ ɢᴜᴇꜱꜱɪɴɢ ᴀɴɪᴍᴇ ᴄʜᴀʀᴀᴄᴛᴇʀꜱ.
ɢᴜᴇꜱꜱ ᴛʜᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ: ᴡʜᴇɴ ᴀɴ ɪᴍᴀɢᴇ ɪꜱ ᴘᴏꜱᴛᴇᴅ, ᴛʏᴘᴇ ᴛʜᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ’ꜱ ɴᴀᴍᴇ ᴛᴏ ɢᴜᴇꜱꜱ. ʏᴏᴜ ʜᴀᴠᴇ 5 ᴍɪɴᴜᴛᴇꜱ ᴘᴇʀ ʀᴏᴜɴᴅ!
ᴇᴀʀɴ ʀᴇᴡᴀʀᴅꜱ: ᴄᴏʀʀᴇᴄᴛ ɢᴜᴇꜱꜱᴇꜱ ᴇᴀʀɴ 20 ᴄᴏɪɴꜱ, ᴀɴᴅ ꜱᴛʀᴇᴀᴋꜱ (50 ᴏʀ 100 ᴄᴏʀʀᴇᴄᴛ ɢᴜᴇꜱꜱᴇꜱ) ɢɪᴠᴇ ʙᴏɴᴜꜱ ʀᴇᴡᴀʀᴅꜱ (1000 ᴏʀ 2000 ᴄᴏɪɴꜱ).
ᴄᴏᴏʟᴅᴏᴡɴꜱ: ᴍᴀx 1,000,000 ɢᴜᴇꜱꜱᴇꜱ ʙᴇꜰᴏʀᴇ ᴀ 4-ʜᴏᴜʀ ᴄᴏᴏʟᴅᴏᴡɴ.

**Need more help?** Contact [🥀 ʜᴇx | Uᴄʜɪʜᴀ.](https://t.me/uchiha_owner) or join [˹ Uᴘᴘᴇʀ ᴍᴏᴏɴ ᴜᴘᴅᴀᴛᴇs ˼ 🎧](https://t.me/SNOWY_HOMETOWN) for support!
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
                InlineKeyboardButton("ᴅᴇᴠeʟᴏᴘᴇʀ 👨‍💻", url="https://t.me/uchiha_owner"),
                InlineKeyboardButton("Update Channel 📢", url="https://t.me/dark_musictm")
            ],
            [
                InlineKeyboardButton("ʜᴇʟᴘ ❓", callback_data="help_command"),
                InlineKeyboardButton("˹ Uᴘᴘᴇʀ ᴍᴏᴏɴ ᴜᴘᴅᴀᴛᴇs ˼ 🎧", url="https://t.me/snowy_hometown")
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



