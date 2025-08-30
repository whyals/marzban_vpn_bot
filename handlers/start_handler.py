from telethon import events, Button

from bot_init import bot
from wtf_bot_config import MENU_BUTTONS

from utils.check_access import check_access
from utils.users_db_func import add_user, get_user
from utils.registration_func import confirm_registration
from utils.logging_func import setup_logger

logger = setup_logger("start_handler", "start_handler.log")


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_info = await event.get_sender()
    user_id = user_info.id

    logger.info(f"/start вызван пользователем ID: {user_id}, Username: {user_info.username}")

    user = await get_user(user_id)
    logger.debug(f"Данные пользователя из БД: {user}")

    if not user or user[3] == 'cancelled':
        await bot.send_message(
            user_id,
            'Ожидайте подтверждения регистрации',
            buttons=[Button.text('Ожидайте подтверждения', resize=True)]
        )
        logger.info(f"Отправлено сообщение о подтверждении регистрации пользователю {user_id}")

        confirm_status, access_level = await confirm_registration(
            user_id, user_info.username, user_info.first_name
        )
        logger.debug(f"Статус подтверждения: {confirm_status}, Уровень доступа: {access_level}")

        await add_user(user_id, user_info.username, user_info.first_name, access_level)

        if confirm_status == 'confirmed':
            logger.info(f"Пользователь {user_id} добавлен в БД и подтверждён (доступ: {access_level})")
            await bot.send_message(
                user_id,
                'Регистрация прошла успешно, теперь Вы можете использовать бота.',
                buttons=MENU_BUTTONS,
                parse_mode='markdown'
            )
        else:
            logger.info(f"Пользователь {user_id} добавлен в БД, но регистрация отклонена")
            await bot.send_message(
                user_id,
                'Регистрация отклонена',
                buttons=[Button.text('Вы заблокированы', resize=True)]
            )
        return

    if await check_access(user_id):
        await bot.send_message(user_id, 'Вы уже зарегистрированы', buttons=MENU_BUTTONS)
        logger.info(f"Пользователь {user_id} уже зарегистрирован")
        return

    await bot.send_message(
        user_id,
        'Вы были заблокированы администратором',
        buttons=[Button.text('Вы заблокированы', resize=True)]
    )
    logger.info(f"Пользователь {user_id} заблокирован администратором")

