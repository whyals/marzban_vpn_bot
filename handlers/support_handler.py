from telethon import Button, events

from bot_init import bot
from wtf_bot_config import BANK_CARD, TON_WALLET, USDT_WALLET, BTC_WALLET

from utils.check_access import check_access
from utils.logging_func import setup_logger

logger = setup_logger("support_handler", "support_handler.log")


@bot.on(events.NewMessage(pattern='Поддержать автора'))
async def support_author(event):
    user_id = event.sender_id
    logger.info(f"Получен запрос на поддержку от пользователя {user_id}")

    if await check_access(user_id):
        logger.info(f"Пользователь {user_id} имеет доступ.")
        support_buttons = [
            [
                Button.inline('RUB', b'support_rub'),
                Button.inline('USDT', b'support_usdt'),
                Button.inline('BTC', b'support_btc'),
                Button.inline('TON', b'support_ton'),
            ]
        ]
        await bot.send_message(user_id, 'Если Вам очень понравился бот, можете поддержать автора копеечкой',
                               buttons=support_buttons)
    else:
        logger.warning(f"Пользователь {user_id} не имеет доступа.")


@bot.on(events.CallbackQuery(data=b'support_rub'))
async def support_rub(event):
    user_id = event.sender_id
    logger.info(f"Пользователь {user_id} выбрал поддержку RUB.")
    await event.respond(f'Спасибо за поддержку! Тинькофф Банк:\n`{BANK_CARD}`', parse_mode='md')


@bot.on(events.CallbackQuery(data=b'support_usdt'))
async def support_usdt(event):
    user_id = event.sender_id
    logger.info(f"Пользователь {user_id} выбрал поддержку USDT.")
    await event.respond(f'Спасибо за поддержку! Адрес:\n`{USDT_WALLET}`', parse_mode='md')


@bot.on(events.CallbackQuery(data=b'support_btc'))
async def support_btc(event):
    user_id = event.sender_id
    logger.info(f"Пользователь {user_id} выбрал поддержку BTC.")
    await event.respond(f'Спасибо за поддержку! Адрес:\n`{BTC_WALLET}`', parse_mode='md')


@bot.on(events.CallbackQuery(data=b'support_ton'))
async def support_ton(event):
    user_id = event.sender_id
    logger.info(f"Пользователь {user_id} выбрал поддержку TON.")
    await event.respond(f'Спасибо за поддержку! Адрес:\n`{TON_WALLET}`', parse_mode='md')
