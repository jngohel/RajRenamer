import os
import time
import humanize
from config import Config
from PIL import Image
from asyncio import sleep
from helper.database import db
from pyrogram.file_id import FileId
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from hachoir.parser import createParser
from pyrogram.enums import MessageMediaType
from hachoir.metadata import extractMetadata
from helper.utils import progress_for_pyrogram, convert, humanbytes
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

FORWARD_CHANNEL = [-1002101130781, -1002084343343]

@Client.on_message(filters.private & (filters.document | filters.video))
async def rename_start(client, message):
    aks_id = message.from_user.id
    aks = message.from_user.mention
    if await db.has_premium_access(aks_id):
        if message.media:
            file = getattr(message, message.media.value)
            caption = message.caption
            if file.file_size > 2000 * 1024 * 1024:
                return await message.reply_text("<b>🔆 sᴏʀʀʏ ʙʀᴏ ɪ ᴄᴀɴ'ᴛ ʀᴇɴᴀᴍᴇ 2ɢʙ+ ꜰɪʟᴇ 💢</b>")
            try:
                text = f"""<b>ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴍᴇ ᴛᴏ ᴅᴏ ᴡɪᴛʜ ᴛʜɪs ꜰɪʟᴇ??\n\nꜰɪʟᴇ ɴᴀᴍᴇ - <code>{caption}</code></b>"""
                buttons = [[
                    InlineKeyboardButton("ʀᴇɴᴀᴍᴇ", callback_data="rename"),
			        InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="cancel")
                ]]
                await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
            except FloodWait as e:
                await sleep(e.value)
                text = f"""<b>ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴍᴇ ᴛᴏ ᴅᴏ ᴡɪᴛʜ ᴛʜɪs ꜰɪʟᴇ??\n\nꜰɪʟᴇ ɴᴀᴍᴇ - <code>{caption}</code></b>"""
                buttons = [[
                    InlineKeyboardButton("ʀᴇɴᴀᴍᴇ", callback_data="rename"),
                    InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="cancel")
                ]]
                await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply_text("<i>ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜɪs ʙᴏᴛ ᴏɴʟʏ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ᴄᴀɴ ᴜsᴇ ɪᴛ 😐\n\nɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ, ᴛʜᴇɴ ᴍsɢ ʜᴇʀᴇ ᴀɴᴅ ɢᴇᴛ ᴀᴄᴄᴇss - @Aks_support01_bot</i>")

@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    user_id = update.message.chat.id
    date = update.message.date
    await update.message.delete()
    await update.message.reply_text("<b>ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ɴᴇᴡ ꜰɪʟᴇ ɴᴀᴍᴇ 😋</b>",	
    reply_to_message_id=update.message.reply_to_message.id,  
    reply_markup=ForceReply(True))	

@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if isinstance(reply_message.reply_markup, ForceReply):
        new_file_name = message.text 
        await message.delete() 
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = getattr(file, file.media.value)
        if not "." in new_file_name:
            if "." in media.file_name:
                extn = media.file_name.rsplit('.', 1)[-1]
            else:
                extn = "mkv"
            new_name = new_file_name + "." + extn
        await reply_message.delete()
        button = [[InlineKeyboardButton("📁 ᴅᴏᴄᴜᴍᴇɴᴛ",callback_data = "upload_document")]]
        if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
            button.append([InlineKeyboardButton("🎥 ᴠɪᴅᴇᴏ", callback_data = "upload_video")])
        await message.reply(
            text=f"<b>sᴇʟᴇᴄᴛ ᴛʜᴇ ᴏᴜᴛᴘᴜᴛ ꜰɪʟᴇ ᴛʏᴘᴇ\n\nꜰɪʟᴇ ɴᴀᴍᴇ:- `{new_file_name}`</b>",
            reply_to_message_id=file.id,
            reply_markup=InlineKeyboardMarkup(button)
        )

@Client.on_callback_query(filters.regex("upload"))
async def doc(bot, update):
    new_file_name = update.message.text
    new_filename = new_file_name.split(":-")[1]
    file = update.message.reply_to_message
    ms = await update.message.edit("<b>ᴛʀʏɪɴɢ ᴛᴏ ʀᴇɴᴀᴍɪɴɢ…</b>")
    file_path = f"downloads/{new_filename}"
    try:
        path = await bot.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ sᴛᴀʀᴛᴇᴅ…", ms, time.time()))                    
    except Exception as e:
        return await ms.edit(e)
    duration = 0
    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    except:
        pass
    ph_path = None
    user_id = int(update.message.chat.id) 
    media = getattr(file, file.media.value)
    c_thumb = await db.get_thumbnail(update.message.chat.id)
    caption = f"<b>{new_filename}</b>" 
    if (media.thumbs or c_thumb):
        if c_thumb:
            ph_path = await bot.download_media(c_thumb) 
        else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
    await ms.edit("ᴛʀʏɪɴɢ ᴛᴏ ᴜᴘʟᴏᴀᴅɪɴɢ…")
    type = update.data.split("_")[1]
    try:
        if type == "document":
            sent = await bot.send_document(
                update.message.chat.id,
                document=path,
                thumb=ph_path, 
                caption=caption, 
                progress=progress_for_pyrogram,
                progress_args=("ᴜᴘʟᴏᴀᴅɪɴɢ sᴛᴀʀᴛᴇᴅ 📥", ms, time.time())
            )
        elif type == "video":
            sent = await bot.send_video(
                update.message.chat.id,
                video=path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("ᴜᴘʟᴏᴀᴅɪɴɢ sᴛᴀʀᴛᴇᴅ 📥", ms, time.time())
            )
    except Exception as e:          
        os.remove(path)
        if ph_path:
            os.remove(ph_path)
        return await ms.edit(f" Eʀʀᴏʀ {e}")

    if user_id in Config.ADMIN:
        for id in FORWARD_CHANNEL:
            await sent.copy(chat_id=id)
    await ms.delete() 
    os.remove(path) 
    if ph_path:
        os.remove(ph_path)

@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot, update):
    try:
        await update.message.delete()
    except:
        return

