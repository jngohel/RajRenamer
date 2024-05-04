from pyrogram import Client, filters 
from helper.database import db
                                       
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
	
@Client.on_message(filters.private & filters.command(['add_thumb', 'addthumb']))
async def addthumbs(client, message):
    await message.reply_text("<b>ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ sᴇᴛ sᴜᴄᴄᴇssꜰᴜʟʟʏ 🥳\n\nsᴇɴᴅ /view_thumb ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴅᴅᴇᴅ ᴛʜᴜᴍʙɴᴀɪʟ</b>")
    await db.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)                











