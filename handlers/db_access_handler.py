from telethon import events

from bot_init import bot

from utils.users_db_func import get_all_users, delete_user
from utils.check_access import check_admin

@bot.on(events.NewMessage(pattern='/delete (\d+)'))
async def handle_delete_user(event):
    if await check_admin(event.sender_id):
        user_id = int(event.pattern_match.group(1))
        await delete_user(user_id)
        await event.reply(f'Пользователь с tg_id {user_id} был удален')

@bot.on(events.NewMessage(pattern='/users'))
async def handle_get_users(event):
    if await check_admin(event.sender_id):
        users = await get_all_users()
        if users:
            users_info = '\n'.join([f'ID: {user[0]}, Тег: @{user[1]}, Имя: {user[2]}' for user in users])
            await event.reply(f'Список всех пользователей:\n{users_info}')
        else:
            await event.reply('В базе данных нет пользователей')
