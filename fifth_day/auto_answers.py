import csv
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
            print(f"ОТВЕТ ОТ СЕРВЕРА")
            print(result)
            print()
            
            if isinstance(result, list):
                return result[0]
            elif isinstance(results, dict):
                return result
            else:
                return {"label": "ERROR", "score": 0.0}
    
        except requests.exceptions.RequestException as e:
            print(f"Сетевая ошибка {e}")
            if attempt == 2:
                return {"label": "ERROR", "score": 0.0}
            time.sleep(1)

    print("Провал не удалось получить ответ после 3 попыток")
    return {"label": "ERROR", "score": 0.0}


reviews_data = []
try:
    with open("reviews.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            reviews_data.append(row)
except FileNotFoundError:
    print("Файл reviews.csv не найден. Создаю тестовый...")
    reviews_data = [
        {"reviews": "Отличный товар, очень доволен!"},
        {"reviews": "Куртка пришла с браком, ужас."},
        {"reviews": "Нормально, но доставка долгая."}
    ]

results = []

for item in reviews_data:
    review_text = item.get("review", "")

    if not review_text:
        continue

    print(f"Анализируем: {review_text[:30]}...")

    ai_result = ask_ai(review_text)
    sentiment = ai_result["label"]

    if sentiment == "NEGATIVE":
        reply = "Здравствуйте! приносим извинения за доставленные неудобства. Свяжемся с вами в течение 24 часов."
    elif sentiment == "POSITIVE":
        reply = "Спасибо за отзыв! Рады, что вам понравилось."
    else:
        reply = "Спасибо за ваш отзыв! Мы учтем ваши пожелания."
    
    results.append({
        "review": review_text,
        "sentiment": sentiment,
        "reply": reply
    })

with open("reviews_with_replies.csv", "w", encoding="utf-8-sig", newline="") as f:
    fieldnames = ["review", "sentiment", "reply"]
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")

    writer.writeheader()
    writer.writerows(results)

print("\nГотово. Результаты сохранены в reviews_with_replies.csv")