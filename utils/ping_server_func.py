import subprocess
import requests

from utils.logging_func import setup_logger

logger = setup_logger("ping_server", "ping_server.log")

async def ping_server(server):

    host = server["ip"]
    logger.info(f"Проверка пинга для {server['flag']} {server['name_ru']} ({host})")

    try:
        result = subprocess.run(['ping', '-c', '4', host],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return f"✅ Сервер {server['flag']} {server['name_ru']} ({host}) отвечает на пинг.\n{result.stdout}"
        else:
            return f"❌ Сервер {server['flag']} {server['name_ru']} ({host}) не отвечает на пинг.\n{result.stderr}"
    except Exception as e:
        return f"Ошибка при выполнении пинга для {server['flag']} {server['name_ru']} ({host}): {e}"


async def check_http(server):

    host = server["ip"]
    url = f"http://{host}:{server['port']}"  # используем порт из сервера
    logger.info(f"Проверка HTTP для {server['flag']} {server['name_ru']} ({url})")

    try:
        response = requests.get(url, timeout=5)
        return f"✅ Сервер {server['flag']} {server['name_ru']} отвечает на HTTP с кодом {response.status_code}"
    except requests.RequestException as e:
        return f"❌ Ошибка HTTP-запроса к серверу {server['flag']} {server['name_ru']} ({url}): {e}"