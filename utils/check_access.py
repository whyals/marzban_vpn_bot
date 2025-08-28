from telethon import Button

from bot_init import bot
from wtf_bot_config import ADMIN_ID

from utils.users_db_func import get_user

async def check_access(user_id):
    user = await get_user(user_id)
    if user and user[3] == 'denied':
        await bot.send_message(user_id, 'Вы были заблокированы администратором', buttons=[Button.text('Вы заблокированны', resize=True)])
        return False
    elif user and user[3] == 'cancelled':
        await bot.send_message(user_id, 'Вы еще не зарегистрированы, нажмите /start')
        return False
    elif user:
        return True
    else:
        await bot.send_message(user_id, 'Вы еще не зарегистрированы, нажмите /start')

        return False

async def check_admin(user_id):
    user = await get_user(user_id)
    if user[0] == ADMIN_ID:
        return True
    else:
        return False