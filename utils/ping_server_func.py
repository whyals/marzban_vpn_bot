import subprocess
import requests

async def ping_server(host):

    try:
        result = subprocess.run(['ping', '-c', '4', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return f"✅ Сервер {host} отвечает на пинг.\n{result.stdout}"
        else:
            return f"❌ Сервер {host} не отвечает на пинг.\n{result.stderr}"
    except Exception as e:
        return f"Ошибка при выполнении пинга: {e}"

async def check_http(host):

    try:
        response = requests.get(f"http://{host}", timeout=5)
        return f"✅ Сервер {host} отвечает с кодом {response.status_code}"
    except requests.RequestException as e:
        return f"❌ Ошибка HTTP-запроса к серверу {host}: {e}"
