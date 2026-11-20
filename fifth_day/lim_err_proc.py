import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

if not HF_API_KEY:
    print("Внимание: ключ HF_API_KEY не найден в файле .env")

def ask_ai(prompt):
    model_url = "https://router.huggingface.co/hf-inference/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}

    for attempt in range(3):
        try:
            print(f"Попытка {attempt + 1}/3 - Отправка запроса к AI...")

            response = requests.post(model_url, headers=headers, json=payload, timeout=10)

            if response.status_code == 401:
                print("Ошибка: 401 - Неверный API ключ")
                return {"label": "ERROR", "score": 0.0}

            if response.status_code in [429, 503]:
                wait_time = 2 ** attempt
                print(f"Ошибка {response.status_code} Сервер занят. Ждем {wait_time} сек")
                time.sleep(wait_time)
                continue

                response.raise_for_status()

            result = response.json()
            print(f"Успех - Ответ получен")
            return result[0][0]
    
        except requests.exceptions.RequestException as e:
            print(f"Сетевая ошибка {e}")
            if attempt == 2:
                return {"label": "ERROR", "score": 0.0}
            time.sleep(1)

    print("Провал не удалось получить ответ после 3 попыток")
    return {"label": "ERROR", "score": 0.0}