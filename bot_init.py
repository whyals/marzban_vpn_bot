import os
from telethon import TelegramClient

from wtf_bot_config import API_ID, API_HASH, BOT_TOKEN

SESSION_FOLDER = 'logs'
os.makedirs(SESSION_FOLDER, exist_ok=True)

SESSION_PATH = os.path.join(SESSION_FOLDER, 'als_bot_003')

bot = TelegramClient(SESSION_PATH, API_ID, API_HASH).start(bot_token=BOT_TOKEN)

