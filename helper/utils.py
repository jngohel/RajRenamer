import math, time
from datetime import datetime
from pytz import timezone
import re
from PIL import Image
import os
from config import Config, Txt 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:        
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
        progress = "{0}{1}".format(
            ''.join(["⬢" for i in range(math.floor(percentage / 5))]),
            ''.join(["⬡" for i in range(20 - math.floor(percentage / 5))])
        )            
        tmp = progress + Txt.PROGRESS_BAR.format( 
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),            
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text=f"{ud_type}\n\n{tmp}",               
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ᴄᴀɴᴄᴇʟ", callback_data="close")]])                                               
            )
        except:
            pass

def humanbytes(size):    
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'ʙ'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "ᴅ, ") if days else "") + \
        ((str(hours) + "ʜ, ") if hours else "") + \
        ((str(minutes) + "ᴍ, ") if minutes else "") + \
        ((str(seconds) + "ꜱ, ") if seconds else "") + \
        ((str(milliseconds) + "ᴍꜱ, ") if milliseconds else "")
    return tmp[:-2] 

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

async def send_log(b, u):
    if Config.LOG_CHANNEL is not None:
        curr = datetime.now(timezone("Asia/Kolkata"))
        date = curr.strftime('%d %B, %Y')
        time = curr.strftime('%I:%M:%S %p')
        await b.send_message(
            Config.LOG_CHANNEL,
            f"<b>NEW_USER_RENAME_BOT</b>\nDate:- {date}\nTime:- {time}\n\nUser:- {u.mention}\nId:- `{u.id}`\nUsername:- @{u.username}\n\nBy: {b.mention}"
        )
        
async def get_seconds(time_string):
    def extract_value_and_unit(ts):
        value = ""
        unit = ""
        index = 0
        while index < len(ts) and ts[index].isdigit():
            value += ts[index]
            index += 1
        unit = ts[index:]
        if value:
            value = int(value)
        return value, unit
    value, unit = extract_value_and_unit(time_string)
    if unit == 's':
        return value
    elif unit == 'min':
        return value * 60
    elif unit == 'hour':
        return value * 3600
    elif unit == 'day':
        return value * 86400
    elif unit == 'month':
        return value * 86400 * 30
    elif unit == 'year':
        return value * 86400 * 365
    else:
        return 0

def extract_post_id(link):
    match = re.search(r"/(\d+)/?$", link)
    if match:
        return int(match.group(1))
    return None

def check_caption(caption):
    caption = re.sub(r'@\w+\b', '', caption)
    caption = re.sub(r'http[s]?:\/\/\S+', '', caption)
    return caption.strip()
    
async def rename_in_video(bot, update, file_id):
    new_filename = check_caption(update.caption)
    file_path = f"downloads/{new_filename}"
    message = update.reply_to_message
    c_thumb = file_id
    file = update.document or update.video or update.audio
    AKS = await update.reply_text("renaming this file....")
    ms = await AKS.edit("```Trying To Upload...```")
    time.sleep(2)
    c_time = time.time()
    try:
        path = await bot.download_media(message=file, progress=progress_for_pyrogram, progress_args=("``` Trying To Download...```", ms, c_time))
    except Exception as e:
        await ms.edit(str(e))
        return
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name = f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)
    duration = 0
    metadata = extractMetadata(createParser(file_path))
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds
    caption = f"<b>{new_filename}</b>"
    thumb_path = await bot.download_media(c_thumb) 
    try:
       with Image.open(thumb_path) as img:
	       img = img.convert("RGB")
	       img.save(thumb_path, "JPEG")
    except Exception as e:
        await ms.edit(f"Thumbnail processing error: {str(e)}")
    value = 2090000000
    if value < file.file_size:
        await ms.edit("```Trying To Upload...```")
        try:
            c_time = time.time()
            file = await app.send_video(update.chat.id, video=file_path, thumb=thumb_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("```Trying To Uploading```", ms, c_time))
            from_chat = file.chat.id
            mg_id = file.id
            time.sleep(2)
            await bot.copy_message(update.from_user.id, from_chat, mg_id)
            await ms.delete()
            os.remove(file_path)
            try:
                os.remove(thumb_path)
            except:
                pass
        except Exception as e:
            await ms.edit(str(e))
            os.remove(file_path)
            try:
                os.remove(thumb_path)
            except:
                return
    else:
        await ms.edit("```Trying To Upload...```")
        try:
            c_time = time.time()
            await bot.send_video(update.chat.id, video=file_path, thumb=thumb_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("```Trying To Uploading```", ms, c_time))
            os.remove(file_path)
        except Exception as e:
            await ms.edit(str(e))
            os.remove(file_path)
            return


