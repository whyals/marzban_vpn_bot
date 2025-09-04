from telethon import Button
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = int(os.getenv("ADMIN_ID"))

BTC_WALLET = os.getenv("BTC_WALLET")
TON_WALLET = os.getenv("TON_WALLET")
USDT_WALLET = os.getenv("USDT_WALLET")
BANK_CARD = os.getenv("BANK_CARD")

MARZBAN_LOGIN = os.getenv("MARZBAN_LOGIN")
MARZBAN_PASSWORD = os.getenv("MARZBAN_PASSWORD")


SERVERS = {
    f"{os.getenv('VPN_FINLAND_FLAG')} {os.getenv('VPN_FINLAND_NAME_RU')}": {
        "ip": os.getenv("VPN_FINLAND_IP"),
        "port": os.getenv("VPN_FINLAND_PORT"),
        "name_en": os.getenv("VPN_FINLAND_NAME_EN"),
        "name_ru": os.getenv("VPN_FINLAND_NAME_RU"),
        "flag": os.getenv("VPN_FINLAND_FLAG"),
        "url": f"http://{os.getenv('VPN_FINLAND_IP')}:{os.getenv('VPN_FINLAND_PORT')}"
    },
    f"{os.getenv('VPN_GERMANY_FLAG')} {os.getenv('VPN_GERMANY_NAME_RU')}": {
        "ip": os.getenv("VPN_GERMANY_IP"),
        "port": os.getenv("VPN_GERMANY_PORT"),
        "name_en": os.getenv("VPN_GERMANY_NAME_EN"),
        "name_ru": os.getenv("VPN_GERMANY_NAME_RU"),
        "flag": os.getenv("VPN_GERMANY_FLAG"),
        "url": f"http://{os.getenv('VPN_GERMANY_IP')}:{os.getenv('VPN_GERMANY_PORT')}"
    },
    f"{os.getenv('VPN_SPB_FLAG')} {os.getenv('VPN_SPB_NAME_RU')}": {
        "ip": os.getenv("VPN_SPB_IP"),
        "port": os.getenv("VPN_SPB_PORT"),
        "name_en": os.getenv("VPN_SPB_NAME_EN"),
        "name_ru": os.getenv("VPN_SPB_NAME_RU"),
        "flag": os.getenv("VPN_SPB_FLAG"),
        "url": f"http://{os.getenv('VPN_SPB_IP')}:{os.getenv('VPN_SPB_PORT')}"
    }
}

MENU_BUTTONS = [
    [Button.text('Подключить VPN', resize=True), Button.text('Поддержать автора', resize=True)],
    [Button.text('Проверить состояние серверов', resize=True)],
]

DOWNLOAD_LINKS = (
    "**Скачать приложение можно по ссылкам:**\n\n"
    "[IOS](https://apps.apple.com/ru/app/v2box-v2ray-client/id6446814690)\n"
    "[ANDROID](https://github.com/Matsuridayo/NekoBoxForAndroid/releases)\n"
    "[LINUX / WIN](https://github.com/Matsuridayo/NekoBoxForAndroid/releases)\n"
    "[MAC](https://github.com/abbasnaqdi/nekoray-macos/releases)"
)

