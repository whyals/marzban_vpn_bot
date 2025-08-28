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

VPN_OPTIONS = dict(
    item.split(":", 1) for item in os.getenv("VPN_OPTIONS").split(";")
)

MARZBAN_URLS = dict(
    item.split(":", 1) for item in os.getenv("MARZBAN_URLS").split(";")
)

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

