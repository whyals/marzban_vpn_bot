from telethon import events, Button

from bot_init import bot
from wtf_bot_config import SERVERS, DOWNLOAD_LINKS

from utils.check_access import check_access
from utils.vpn_func import get_or_create_vpn_key, get_config_content




@bot.on(events.NewMessage(pattern='Подключить VPN'))
async def connect_vpn(event):
    if not await check_access(event.sender_id):
        return

    vpn_buttons = [
        [Button.inline(display_name, f'vpn_{data["name_en"]}'.encode())]
        for display_name, data in SERVERS.items()
    ] + [[Button.url("Что лучше выбрать", "https://teletype.in/@why_als/0LpBk5NUMJ8#Xfxd")]]

    await bot.send_message(
        event.sender_id,
        'Выберите страну для подключения:',
        buttons=vpn_buttons
    )


@bot.on(events.CallbackQuery(pattern=b'vpn_.*'))
async def send_vpn_config(event):
    if not await check_access(event.sender_id):
        return

    user_id = event.sender_id
    sender = await event.get_sender()
    user_tag = f"@{sender.username}" if sender.username else f"user_{user_id}"

    country_code = event.data.decode().split('vpn_', 1)[1]


    server = next((s for s in SERVERS.values() if s["name_en"] == country_code), None)
    if not server:
        await event.respond('Ошибка: такая страна не поддерживается.')
        return

    try:
        subscription_url = await get_or_create_vpn_key(user_id, user_tag, country_code)

        base_url = server["url"]
        if not base_url:
            await event.respond('Ошибка: неизвестный сервер для выбранной страны.')
            return

        config_url = f"{base_url.rstrip('/')}{subscription_url}"
        config = await get_config_content(config_url)

        key_label = f"{country_code.upper()}_VLESS"
        config = config.split('#')[0] + f"#{key_label}"

        message = (
            f"Ваш VPN-ключ для {server['flag']} {server['name_ru']}:\n\n"
            f"```\n{config}\n```\n\n"
            f"{DOWNLOAD_LINKS}"
        )

        await event.respond(
            message,
            buttons=[Button.url("Гайд по подключению и настройкам", "https://teletype.in/@why_als/0LpBk5NUMJ8#Skwv")],
            parse_mode='md'
        )

    except Exception as e:
        await event.respond(f"Ошибка при получении конфигурации: {e}")
