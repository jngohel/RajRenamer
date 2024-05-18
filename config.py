import re, os, time
id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    API_ID    = os.environ.get("API_ID", "24781773")
    API_HASH  = os.environ.get("API_HASH", "ad907569f68cab06c733794fc91be7b6")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6210624556:AAFrgq8aU6inlrQoqeatdUqrcktEhYezeek") 
    DB_NAME = os.environ.get("DB_NAME","renameaks2")     
    DB_URL  = os.environ.get("DB_URL","mongodb+srv://technicalaks77:technicalaks7777@cluster0.51wmuvb.mongodb.net/?retryWrites=true&w=majority")
    BOT_UPTIME  = time.time()
    ADMIN       = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1030335104').split()]
    FORCE_SUB   = os.environ.get("FORCE_SUB", "Aksbackup") 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001769642119"))
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))   

    #this 3 vars is for auto renaming
    IS_VIDEO_MODE = True
    DEST_CHANNEL_ID = int(os.environ.get("DEST_CHANNEL_ID", "-1002015035745"))
    SOURCE_CHANNEL_ID = int(os.environ.get("SOURCE_CHANNEL_ID", "-1002085038189"))
    
class Txt(object):
    # part of text configuration
    START_TXT = """<i>ᴛʜɪs ɪs ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ & ᴘᴏᴡᴇʀꜰᴜʟ ʀᴇɴᴀᴍᴇ ʙᴏᴛ, ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ ʏᴏᴜ ᴄᴀɴ ʀᴇɴᴀᴍᴇ & ᴄʜᴀɴɢᴇ ᴛʜᴜᴍʙɴᴀɪʟ ᴏꜰ ʏᴏᴜʀ ꜰɪʟᴇ, ᴊᴜsᴛ sᴇɴᴛ ᴍᴇ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴅᴏᴄᴜᴍᴇɴᴛ, ᴠɪᴅᴇᴏ ᴀɴᴅ ᴇɴᴛᴇʀ ɴᴇᴡ ꜰɪʟᴇ ɴᴀᴍᴇ ᴛᴏ ʀᴇɴᴀᴍᴇ ɪᴛ</i>"""
    
    HELP_TXT = """<b>🌄 ʜᴏᴡ ᴛᴏ sᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ 🌄
    
/start - sᴇɴᴅ ᴀɴʏ ᴘʜᴏᴛᴏ ʙᴏᴛ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ sᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ
/del_thumb - ᴛᴏ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴏʟᴅ ᴛʜᴜᴍʙɴᴀɪʟ
/view_thumb - ᴛᴏ ᴠɪᴇᴡs ᴛᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ


🧾 ʜᴏᴡ ᴛᴏ sᴇᴛ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ 🧾

/set_caption - ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ sᴇᴛ ᴀ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ
/see_caption - ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴠɪᴇᴡ ʏᴏᴜʀ ᴀᴅᴅᴇᴅ ᴄᴀᴘᴛɪᴏɴ
/del_caption - ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ

ᴇx - <code>/set_caption ꜰɪʟᴇ ɴᴀᴍᴇ - {filename}
sɪᴢᴇ - {filesize}
ᴅᴜʀᴀᴛɪᴏɴ - {duration}</code>


❓ ʜᴏᴡ ᴛᴏ ʀᴇɴᴀᴍᴇ ᴀɴʏ ꜰɪʟᴇ ❓

sᴇɴᴅ ᴀɴʏ ꜰɪʟᴇ & ᴛʏᴘᴇ ɴᴇᴡ ꜰɪʟᴇ ɴᴀᴍᴇ ᴀɴᴅ sᴇʟᴇᴄᴛ ᴛʜᴇ ꜰᴏʀᴍᴀᴛ [ ᴅᴏᴄᴜᴍᴇɴᴛ, ᴠɪᴅᴇᴏ, ᴀᴜᴅɪᴏ ]

🕵 ɪꜰ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ᴛʜᴇɴ ᴍsɢ ʜᴇʀᴇ - <a href=https://t.me/Aks_support01_bot>ᴛᴇᴀᴍ</a></b>"""


    PROGRESS_BAR = """\n
sɪᴢᴇ - {1} | {2}
ᴅᴏɴᴇ - {0}%
sᴘᴇᴇᴅ - {3}/s
ᴛɪᴍᴇ - {4}"""


