import aiohttp
import uuid
import re
import base64
import socket

from wtf_bot_config import SERVERS, MARZBAN_LOGIN, MARZBAN_PASSWORD

from utils.vpn_keys_db_func import get_vpn_key, add_vpn_key
from utils.logging_func import setup_logger

logger = setup_logger("vpn_func", "vpn_func.log")


async def get_access_token(base_url):
    try:
        connector = aiohttp.TCPConnector(family=socket.AF_INET)
        async with aiohttp.ClientSession(connector=connector) as session:
            url = f"{base_url}/api/admin/token" # тут ломается
            data = {"username": MARZBAN_LOGIN, "password": MARZBAN_PASSWORD}
            async with session.post(url, data=data, ssl=False) as response:
                if response.status == 200:
                    token = (await response.json())["access_token"]
                    logger.info(f"Токен успешно получен для {base_url}")
                    return token
                else:
                    error_text = await response.text()
                    logger.error(f"Ошибка получения токена: {response.status} - {error_text}")
                    raise Exception(f"Ошибка токена: {response.status} - {error_text}")
    except Exception as e:
        logger.error(f"Исключение при получении токена: {str(e)}")
        raise


def format_name(name, user_id):

    logger.info(f"Очистка имени пользователя: {name}")
    cleaned_name = re.sub(r'[^a-z0-9_]', '', name.lower().replace('@', ''))
    vpn_name = f"{cleaned_name}_{user_id}"
    vpn_name = vpn_name[:32]
    if len(vpn_name) < 3:
        vpn_name = vpn_name + "_" * (3 - len(vpn_name))
    logger.info(f"Очищенное имя пользователя: {vpn_name}")
    return vpn_name


async def get_or_create_vpn_key(user_id, user_name, country_code):
    for server in SERVERS.values():
        if server["name_en"] == country_code:
            base_url = f"http://{server['ip']}:{server['port']}"
            break
    else:
        logger.error(f"URL для страны {country_code} не настроен")
        raise ValueError(f"URL для страны {country_code} не настроен.")


    logger.info(f"Проверка ключа в базе для tg_id={user_id}, country={country_code}")
    vpn_key = get_vpn_key(user_id, country_code)
    if vpn_key:
        logger.info(f"Ключ найден в базе: {vpn_key}")
        return vpn_key


    formated_name = format_name(user_name, user_id)
    try:
        access_token = await get_access_token(base_url)
    except Exception as e:
        logger.error(f"Не удалось подключиться к серверу {base_url}: {str(e)}")
        raise Exception(f"Сервер {country_code} недоступен. Попробуйте позже.")


    connector = aiohttp.TCPConnector(family=socket.AF_INET)
    async with aiohttp.ClientSession(connector=connector) as session:

        url = f"{server['url']}/api/user/{formated_name}"

        headers = {"Authorization": f"Bearer {access_token}"}
        async with session.get(url, headers=headers, ssl=False) as response:
            if response.status == 200:
                user_data = await response.json()
                subscription_url = user_data.get("subscription_url")
                logger.info(f"Пользователь найден, subscription_url: {subscription_url}")
                add_vpn_key(user_id, country_code, subscription_url)
                return subscription_url
            elif response.status != 404:
                error_text = await response.text()
                logger.error(f"Ошибка проверки пользователя: {response.status} - {error_text}")
                raise Exception(f"Ошибка проверки пользователя: {response.status} - {error_text}")


        logger.info(f"Создание нового пользователя {formated_name} на {base_url}")
        unique_uuid = str(uuid.uuid4())

        user_data = {
            "username": formated_name,
            "proxies": {
                "vless": {"id": unique_uuid}
            },
            "inbounds": {
                "vless": ["VLESS TCP REALITY"]
            },
            "expire": 0,
            "data_limit": 0,
            "data_limit_reset_strategy": "no_reset"
        }

        url = f"{base_url}/api/user"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        async with session.post(url, json=user_data, headers=headers, ssl=False) as response:
            if response.status == 200:
                subscription_url = (await response.json()).get("subscription_url")
                logger.info(f"Пользователь создан, subscription_url: {subscription_url}")
                add_vpn_key(user_id, country_code, subscription_url)
                return subscription_url
            else:
                error_text = await response.text()
                logger.error(f"Ошибка создания пользователя: {response.status} - {error_text}")
                raise Exception(f"Ошибка создания ключа: {response.status} - {error_text}")


async def get_config_content(config_url):
    logger.info(f"Получение конфигурации по URL: {config_url}")
    try:
        connector = aiohttp.TCPConnector(family=socket.AF_INET)  # Только IPv4
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(config_url, ssl=False) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Ошибка загрузки конфигурации: {response.status} - {error_text}")
                    raise Exception(f"Ошибка загрузки конфигурации: {response.status}")

                raw_bytes = await response.read()
                try:
                    decoded_config = base64.b64decode(raw_bytes).decode("utf-8").strip()
                except Exception as e:
                    logger.error(f"Ошибка декодирования Base64: {e}")
                    raise Exception("Ошибка декодирования: возможно, данные повреждены или это не подписка.")

                config_lines = decoded_config.replace('\r', '').split('\n')
                config_lines = [line.strip() for line in config_lines if line.strip()]

                for line in config_lines:
                    if line.startswith("vless://"):
                        logger.info(f"Найден ключ VLESS: {line}")
                        return line

                logger.error("Ключ не найден в конфигурации.")
                raise Exception("Ключ не найден в конфигурации.")
    except Exception as e:
        logger.error(f"Ошибка при получении конфигурации: {e}")
        raise

