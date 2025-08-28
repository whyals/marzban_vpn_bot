from telethon import events, Button
import asyncio

from bot_init import bot

from wtf_bot_config import ADMIN_ID

from utils.users_db_func import add_user

async def confirm_registration(user_id, user_tag, user_name):
    confirm_buttons = [
        [Button.inline('Подтвердить', b'confirm'), Button.inline('Отклонить', b'deny')]
    ]
    access_level_buttons = [
        [Button.inline('main', b'main'), Button.inline('friend', b'friend'), Button.inline('noname', b'noname')]
    ]

    async with bot.conversation(ADMIN_ID) as conv:
        try:
            message = await conv.send_message(f"Запрос на регистрацию от пользователя {user_name} @{user_tag}", buttons=confirm_buttons)
            confirm_response = await conv.wait_event(events.CallbackQuery, timeout=300)

            if confirm_response.data == b'confirm':
                confirm_status = 'confirmed'
                await confirm_response.delete()
                await conv.send_message("Выберите уровень доступа:", buttons=access_level_buttons)
                access_level_response = await conv.wait_event(events.CallbackQuery, timeout=300)

                if access_level_response.data == b'main':
                    access_level = 'main'
                elif access_level_response.data == b'friend':
                    access_level = 'friend'
                elif access_level_response.data == b'noname':
                    access_level = 'noname'

                await access_level_response.delete()
                await conv.send_message(f'Вы одобрили заявку от {user_name} и присвоили уровень доступа: {access_level}')
            elif confirm_response.data == b'deny':
                confirm_status = 'denied'
                access_level = 'denied'
                await confirm_response.delete()
                await conv.send_message('Вы отклонили заявку на регистрацию.')

        except asyncio.TimeoutError:
            await message.delete()
            await add_user(user_id, user_tag, user_name, 'cancelled')
            await bot.send_message(user_id, 'Время на подтверждение истекло. Пожалуйста, повторите попытку.')
            await bot.send_message(ADMIN_ID, 'Время на подтверждение истекло. Пожалуйста, повторите попытку.')
            confirm_status = 'timeout'
            access_level = 'denied'

    return confirm_status, access_level
