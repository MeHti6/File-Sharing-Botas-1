#(©)CodeXBotz

import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()

#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7739260996:AAFqXV5tM69LSCbBHWF9flg-bU8kqsIY5gU")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "21193086"))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "c777f51828848e91a710f25a4d99616d")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001493351320"))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "1285296096"))

#Port
PORT = os.environ.get("PORT", "8080")

#Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://bruh5556:bruh5556@cluster0.rrkdj3r.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "filesharexbot")

#force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1001725487477"))
JOIN_REQUEST_ENABLE = os.environ.get("JOIN_REQUEST_ENABLED", None)

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

#start message
START_PIC = os.environ.get("START_PIC","")
START_MSG = os.environ.get("START_MESSAGE", ".\
\
اول باید کانال بکاپ جوین شی تا بتونی فیلم بگیری  .\
کانال بکاپ : \
https://t.me/joinchat/nVWYqlrYP8w3NTAx\
 (اول باید کانال بالا عضو شید بعد دوباره فیلمی که میخواید رو بفرستید استارت بزنید ) ")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", " سلام.\
\
اول باید کانال بکاپ جوین شی تا بتونی فیلم بگیری  .\
کانال بکاپ : \
https://t.me/joinchat/nVWYqlrYP8w3NTAx\
 (اول باید کانال بالا عضو شید بعد دوباره فیلمی که میخواید بگیرید رو انتخاب کنید )  ")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

# Auto delete time in seconds.
AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "30"))
AUTO_DELETE_MSG = os.environ.get("AUTO_DELETE_MSG", "توجه! ویدیو ارسال شده در سی ثانیه آینده حذف می شود.")
AUTO_DEL_SUCCESS_MSG = os.environ.get("AUTO_DEL_SUCCESS_MSG", "فایل حذف شد برای دریافت دوباره از کانال استفاده کنید.")

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "."

ADMINS.append(OWNER_ID)
ADMINS.append(1285296096)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
