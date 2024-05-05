import os
import asyncio
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
message_queue = asyncio.Queue()
batch_data = {}

def extract_post_id(link):
    match = re.search(r"/(\d+)/?$", link)
    if match:
        return int(match.group(1))
    return None
	
def check_caption(caption):
    caption = re.sub(r'@\w+\b', '', caption)  # Remove usernames
    caption = re.sub(r'http[s]?:\/\/\S+', '', caption)  # Remove URLs
    return caption.strip()

async def rename_in_video(bot, update, file_id):
    try:
        new_filename = await check_caption(update.caption)
        file_path = f"downloads/{new_filename}"
        message = update.reply_to_message
        c_thumb = file_id
        file = None
        
        # Find the file in the message
        if message.media:
            file = message.media

        if not file:
            await update.reply("No media found in the message.")
            return

        AKS = await update.reply("Renaming this file...")
        ms = await AKS.edit("Trying to upload...")
        time.sleep(2)
        c_time = time.time()

        # Download the file
        try:
            path = await bot.download_media(file, file_path)
        except Exception as e:
            await ms.edit(str(e))
            return

        # Rename the file
        old_file_name = f"{path}"
        os.rename(old_file_name, file_path)

        # Process thumbnail
        thumb_path = None
        if c_thumb:
            thumb_path = f"downloads/thumb_{new_filename}.jpg"
            try:
                thumb_path = await bot.download_media(c_thumb)
                with Image.open(thumb_path) as img:
                    img = img.convert("RGB")
                    img.save(thumb_path, "JPEG")
            except Exception as e:
                await ms.edit(f"Thumbnail processing error: {str(e)}")
                return

        # Upload the video
        caption = f"<b>{new_filename}</b>"
        duration = getattr(file, 'duration', 0)
        try:
            c_time = time.time()
            await bot.send_video(update.chat.id, video=file_path, thumb=thumb_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("Trying to upload...", ms, c_time))
            os.remove(file_path)
            if thumb_path:
                os.remove(thumb_path)
        except Exception as e:
            await ms.edit(str(e))
            os.remove(file_path)
            if thumb_path:
                os.remove(thumb_path)
    except Exception as e:
        await update.reply(f"Error: {str(e)}")

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

@Client.on_message(filters.private & filters.command(["batch"]))
async def batch_rename(client, message):
    try:
        if len(message.command) != 3:
            await message.reply("Usage: /batch start_post_link end_post_link")
            return

        start_post_link = message.command[1]
        end_post_link = message.command[2]
        start_post_id = extract_post_id(start_post_link)
        end_post_id = extract_post_id(end_post_link)

        if start_post_id is None or end_post_id is None:
            await message.reply("Invalid post links provided. Usage: /batch start_post_link end_post_link")
            return

        source_channel_id = -1002084343343
        dest_channel_id = -1002101130781

        await message.reply_text("Please provide a thumbnail image for the batch. Send a photo.")

        # Store batch data
        batch_data[message.chat.id] = {
            "start_post_id": start_post_id,
            "end_post_id": end_post_id,
            "source_channel_id": source_channel_id,
            "dest_channel_id": dest_channel_id,
        }
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

# Thumbnail handling
@Client.on_message(filters.private & filters.photo)
async def thumbnail_img_received(client, message):
    try:
        chat_id = message.chat.id
        if chat_id not in batch_data:
            await message.reply_text("No batch data found.")
            return

        file_id = str(message.photo.file_id)
        await db.set_thumbnail(message.chat.id, file_id)
        await message.reply_text("**Your Custom Thumbnail Saved Successfully ☑️**")

        data = batch_data.pop(chat_id)

        start_post_id = data["start_post_id"]
        end_post_id = data["end_post_id"]
        source_channel_id = data["source_channel_id"]
        dest_channel_id = data["dest_channel_id"]
        thumbnail_file_id = str(message.photo.file_id)

        await message.reply_text("Renaming started...")
        for post_id in range(start_post_id, end_post_id + 1):
            await message_queue.put((source_channel_id, dest_channel_id, post_id, thumbnail_file_id))

        while not message_queue.empty():
            source_id, dest_id, post_id, thumbnail_file_id = await message_queue.get()
            try:
                AKS = await client.copy_message(
                    chat_id=dest_id,
                    from_chat_id=source_id,
                    message_id=post_id
                )
                await rename_in_video(client, AKS, thumbnail_file_id)
                await client.delete_messages(dest_id, AKS.id)
                await client.delete_messages(dest_id, AKS.id + 1)
            except Exception as e:
                await message.reply_text(f"Error processing post {post_id}: {str(e)}")

        await message.reply_text("Renaming completed.")
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")


