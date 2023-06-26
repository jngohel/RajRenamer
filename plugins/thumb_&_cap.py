from pyrogram import Client, filters 
from helper.database import db
import os
from config import Config

@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    if len(message.command) == 1:
       return await message.reply_text("**__Gɪᴠᴇ Tʜᴇ Cᴀᴩᴛɪᴏɴ__\n\nExᴀᴍᴩʟᴇ:- `/set_caption {filename}\n\n💾 Sɪᴢᴇ: {filesize}\n\n⏰ Dᴜʀᴀᴛɪᴏɴ: {duration}`**")
    caption = message.text.split(" ", 1)[1]
    await db.set_caption(message.from_user.id, caption=caption)
    await message.reply_text("<b>sᴜᴄᴄᴇssꜰᴜʟʟʏ ᴄᴀᴘᴛɪᴏɴ sᴀᴠᴇᴅ ⚡️</b>")
   
@Client.on_message(filters.private & filters.command('del_caption'))
async def delete_caption(client, message):
    caption = await db.get_caption(message.from_user.id)  
    if not caption:
       return await message.reply_text("__**😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ**__")
    await db.set_caption(message.from_user.id, caption=None)
    await message.reply_text("**ᴄᴀᴘᴛɪᴏɴ ᴅᴇʟᴇᴛᴇᴅ 🌬**")
                                       
@Client.on_message(filters.private & filters.command(['see_caption', 'view_caption']))
async def see_caption(client, message):
    caption = await db.get_caption(message.from_user.id)  
    if caption:
       await message.reply_text(f"**ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ -**\n\n`{caption}`")
    else:
       await message.reply_text("**ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴄᴀᴘᴛɪᴏɴ ‼️**")


@Client.on_message(filters.private & filters.command(['view_thumb', 'viewthumb']))
async def viewthumb(client, message):    
    thumb = await db.get_thumbnail(message.from_user.id)
    if thumb:
       await client.send_photo(chat_id=message.chat.id, photo=thumb)
    else:
        await message.reply_text("<b>ʏᴏᴜ ᴅᴏɴ’ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴛʜᴜᴍʙɴᴀɪʟ 😕\nᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴛʜᴜᴍʙɴᴀɪʟ</b>") 
		
@Client.on_message(filters.private & filters.command(['del_thumb', 'delthumb']))
async def removethumb(client, message):
    await db.set_thumbnail(message.from_user.id, file_id=None)
    await message.reply_text("**ᴛʜᴜᴍʙɴᴀɪʟ ᴅᴇʟᴇᴛᴇᴅ 🚫**")
	
@Client.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    await message.reply_text("<b>ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ sᴇᴛ sᴜᴄᴄᴇssꜰᴜʟʟʏ 🥳\n\nsᴇɴᴅ /view_thumb ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴅᴅᴇᴅ ᴛʜᴜᴍʙɴᴀɪʟ</b>")
    await db.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)                


@Client.on_message(filters.command('send') & filters.user(Config.ADMIN))
async def send_msg(bot, message):
    if message.from_user.id not in ADMIN:
        await message.reply('ᴏɴʟʏ ᴛʜᴇ ʙᴏᴛ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ... 😑')
        return
    if not message.reply_to_message:
        return await message.reply('reply to any msg')
    
    try:
        _id = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("give user id!")
    
    try:
        user = await bot.get_users(_id)
    except Exception as e:
        return await message.reply_text(f"error: {e}")
        
    try:
        await message.reply_to_message.forward(int(user.id))
        await message.reply_text(f'sent to {user.mention}')
    except Exception as e:
        await message.reply_text(f"error: {e}")




