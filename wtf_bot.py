from handlers.start_handler import *
from handlers.vpn_handler import *
from handlers.support_handler import *
from handlers.post_message_handler import *
from handlers.db_access_handler import *
from handlers.ping_server_handler import *

from utils.logging_func import setup_logger

setup_logger("bot", "wtf_bot.log")




logger.info("Бот запущен...")
bot.run_until_disconnected()

