from telethon import events, Button
import subprocess
import asyncio

from bot_init import bot
from wtf_bot_config import MARZBAN_LOGIN, MARZBAN_PASSWORD, SERVERS

from utils.vpn_func import get_access_token
from utils.logging_func import setup_logger

logger = setup_logger("ping_server", "ping_server.log")


async def check_ping(host):
    logger.info(f"Проверка пинга для хоста: {host}")
    try:
        result = subprocess.run(['ping', '-c', '4', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            logger.info(f"Пинг успешен для {host}")
            return "✅ Сервер пингуется", result.stdout
        else:
            logger.warning(f"Пинг не удался для {host}")
            return "❌ Сервер не пингуется", result.stdout
    except Exception as e:
        logger.error(f"Ошибка при проверке пинга для {host}: {str(e)}")
        return f"Ошибка при проверке пинга: {e}", None


async def check_packets(detailed_ping):
    logger.info("Проверка получения пакетов")
    if detailed_ping and (
        "4 packets transmitted, 4 packets received" in detailed_ping or
        "4 packets transmitted, 4 received" in detailed_ping
    ):
        logger.info("Все пакеты получены")
        return "✅ Все пакеты получены"
    else:
        logger.warning("Пакеты не получены или потеряны")
        return "❌ Пакеты не получены или потеряны"


async def check_token(server):
    logger.info(f"Проверки токена для сервера: {server['name_ru']}")
    try:
        base_url = server["url"]


        logger.info(f"Используемый URL для получения токена: {base_url}/api/admin/token")
        logger.info(f"Передаваемые данные: username={MARZBAN_LOGIN}, password=[HIDDEN]")

        token = await get_access_token(base_url)
        logger.info(f"Токен успешно получен для {server['name_ru']}: {token[:10]}... (обрезан для безопасности)")
        return "✅ VPN клиент работает"
    except Exception as e:
        logger.error(f"Ошибка при получении токена для {server['name_ru']}: {str(e)}")
        return f"❌ VPN клиент не работает: {str(e)}"


@bot.on(events.NewMessage(pattern='Проверить состояние серверов'))
async def handler(event):
    logger.info("Получена команда 'Проверить состояние серверов'")
    buttons = [[Button.inline(name, data=server["ip"])] for name, server in SERVERS.items()]
    await event.reply("Выберите сервер для проверки:", buttons=buttons)


@bot.on(events.CallbackQuery(pattern=r'^\d+\.\d+\.\d+\.\d+$'))
async def callback(event):
    host = event.data.decode("utf-8")
    server_name, server = next(((name, srv) for name, srv in SERVERS.items() if srv["ip"] == host), (host, None))
    logger.info(f"Начало проверки сервера: {server_name} ({host})")

    await event.edit(f"🔍 Проверка сервера **{server_name}**...\n\nОжидание проверки пинга...")
    await asyncio.sleep(1)

    ping_result, detailed_ping = await check_ping(host)
    await event.edit(f"🔍 Проверка сервера **{server_name}**...\n\n{ping_result}\nОжидание проверки пакетов...")
    await asyncio.sleep(1)

    packet_result = await check_packets(detailed_ping)
    message = f"🔍 Проверка сервера **{server_name}**...\n\n{ping_result}\n{packet_result}"

    await event.edit(f"{message}\nОжидание проверки токена...")
    await asyncio.sleep(1)

    token_result = await check_token(server) if server else "❌ Сервер не найден"
    message = (
        f"🔍 Отчет проверки сервера **{server_name}**:\n\n"
        f"{ping_result}\n"
        f"{packet_result}\n"
        f"{token_result}\n\n"
        f"Если заметили ошибку, обратитесь к @why_als"
    )
    button = Button.inline("Подробная проверка", data=f"detail_{host}")
    logger.info(f"Проверка завершена для {server_name}")
    await event.edit(message, buttons=[[button]])


@bot.on(events.CallbackQuery(pattern=r'^detail_\d+\.\d+\.\d+\.\d+$'))
async def handle_detail(event):
    host = event.data.decode("utf-8").split("_")[1]
    server_name, server = next(((name, srv) for name, srv in SERVERS.items() if srv["ip"] == host), (host, None))
    logger.info(f"Начало подробной проверки сервера: {server_name} ({host})")

    await event.edit(f"🔍 Повторная проверка сервера **{server_name}**...\n\nОжидание проверки пинга...")
    await asyncio.sleep(1)

    ping_result, detailed_ping = await check_ping(host)
    await event.edit(f"🔍 Повторная проверка сервера **{server_name}**...\n\n{ping_result}\nОжидание проверки пакетов...")
    await asyncio.sleep(1)

    packet_result = await check_packets(detailed_ping)
    message = f"🔍 Повторная проверка сервера **{server_name}**...\n\n{ping_result}\n{packet_result}"

    await event.edit(f"{message}\nОжидание проверки токена...")
    await asyncio.sleep(1)

    token_result = await check_token(server) if server else "❌ Сервер не найден"
    message = (
        f"🔍 Подробный отчет проверки сервера **{server_name}**:\n\n"
        f"{ping_result}\n"
        f"{packet_result}\n"
        f"{token_result}\n\n"
        f"**Детальная информация пинга:**\n```\n{detailed_ping if detailed_ping else 'Нет данных'}\n```\n"
        f"Если заметили ошибку, обратитесь к @why_als"
    )
    logger.info(f"Подробная проверка завершена для {server_name}")
    await event.edit(message)