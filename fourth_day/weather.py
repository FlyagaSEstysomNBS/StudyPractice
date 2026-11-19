import requests


def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 401:
            print(f"Ошибка 401: Неверный API ключ.")
            return

        if response.status_code == 404:
            print(f"Ошибка 404: Город \"{city}\" не найден")
            return

        response.raise_for_status()

        data = response.json()

        current = data["current_condition"][0]

        temp = current["temp_C"]
        humidity = current["humidity"]

        description = current["weatherDesc"][0]["value"]

        print(f"{city}: {temp} °C, {description}, влажность {humidity}%")

    except requests.exceptions.Timeout:
        print(f"Ошибка: превышено время ожидания для города: {city}")
    except requests.exceptions.ConnectionError:
        print(f"Ошибка: проблемы с интернет-соединением при запросе для {city}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка: при запросе погоды для {city}: {e}")


get_weather("Санкт-Петербург")
get_weather("юбвфжвцэа")
get_weather("Новосибирск")