"""
Apache License 2.0
Copyright (c) 2022 @PYRO_BOTZ
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
Telegram Link : https://t.me/PYRO_BOTZ 
Repo Link : https://github.com/TEAM-PYRO-BOTZ/PYRO-RENAME-BOT
License Link : https://github.com/TEAM-PYRO-BOTZ/PYRO-RENAME-BOT/blob/main/LICENSE
"""

import re, os, time

id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "24781773")
    API_HASH  = os.environ.get("API_HASH", "ad907569f68cab06c733794fc91be7b6")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6210624556:AAFrgq8aU6inlrQoqeatdUqrcktEhYezeek") 
   
    # database config
    DB_NAME = os.environ.get("DB_NAME","renameaks2")     
    DB_URL  = os.environ.get("DB_URL","mongodb+srv://technicalaks77:technicalaks7777@cluster0.51wmuvb.mongodb.net/?retryWrites=true&w=majority")
 
    # other configs
    BOT_UPTIME  = time.time()
    ADMIN       = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1030335104').split()]
    FORCE_SUB   = os.environ.get("FORCE_SUB", "Aksbackup") 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001769642119"))

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    

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


