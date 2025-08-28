from telethon import events

from bot_init import bot
from wtf_bot_config import ADMIN_ID, MENU_BUTTONS

from utils.check_access import check_admin, check_access
from utils.users_db_func import get_all_users
from utils.logging_func import setup_logger

logger = setup_logger("support_handler", "support_handler.log")


async def broadcast_message(message_text):
    users = await get_all_users()
    user_ids = [user[0] for user in users]

    for user_id in user_ids:
        try:
            await bot.send_message(user_id, message_text, parse_mode='markdown', buttons=MENU_BUTTONS)
            print(f'Сообщение отправлено пользователю {user_id}')
        except Exception as e:
            print(f'Не удалось отправить сообщение пользователю {user_id}: {e}')



@bot.on(events.NewMessage(pattern='/post'))
async def handle_post_command(event):
    if await check_admin(event.sender_id):
        async with bot.conversation(event.chat_id, timeout=300) as conv:

            await conv.send_message(
                "Пожалуйста, введите текст сообщения. Отправьте /cancel для отмены.")

            response = await conv.get_response()

            if response.text == '/cancel':
                await conv.send_message("Отменено.")
                return

            message = (response.text)
            await broadcast_message(message)
            await conv.send_message("Сообщение успешно отправлено всем пользователям!")
    else:
        await event.reply('Много хочешь')

@bot.on(events.NewMessage(pattern='/message (\d+)'))
async def handle_message_command(event):
    if await check_admin(event.sender_id):
        user_id = int(event.pattern_match.group(1))
        async with bot.conversation(event.chat_id, timeout=300) as conv:

            await conv.send_message(
                f"Пожалуйста, введите текст сообщения для пользователя с tg_id {user_id}. Отправьте /cancel для отмены.")

            response = await conv.get_response()

            if response.text == '/cancel':
                await conv.send_message("Отменено.")
                return

            message = response.text
            try:
                await bot.send_message(user_id, message)
                await conv.send_message(f'Сообщение успешно отправлено пользователю с tg_id {user_id}')
            except Exception as e:
                await conv.send_message(f'Не удалось отправить сообщение пользователю {user_id}: {e}')
    else:
        await event.reply('Много хочешь')


@bot.on(events.NewMessage(pattern='/feedback'))
async def handle_feedback_command(event):
    user_id = event.sender_id
    name = event.sender.first_name or "Без имени"
    tag = event.sender.username or "Без тега"

    if await check_access(user_id):
        async with bot.conversation(event.chat_id, timeout=300) as conv:
            await conv.send_message(
                "Пожалуйста, введите текст обратной связи. Отправьте /cancel для отмены.")
            response = await conv.get_response()

            if response.text == '/cancel':
                await conv.send_message("Отменено.")
                return

            message = f'#feedback от пользователя {name} @{tag}\n\n{response.text}'
            await bot.send_message(ADMIN_ID, message)
            await conv.send_message("Спасибо за обратную связь!")
    else:
        await event.reply("У вас нет доступа к этой команде.")