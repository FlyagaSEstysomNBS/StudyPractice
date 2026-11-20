import os
import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("HF_API_KEY")


def ask_ai(prompt):
    model_url = "https://router.huggingface.co/hf-inference/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"

    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"inputs": prompt}

    response = requests.post(model_url, headers=headers, json=payload)

    response.raise_for_status()
    
    result = response.json()
    return result[0][0]


reviews = [
    "Доставили быстро, все супер!",
    "Товар пришел разбитым, ужас.",
    "Нормально, но могло быть лучше."
]

for review in reviews:
    result = ask_ai(review)

    label = result['label']
    score = round(result['score'], 3)

    print(f"\"{review}\" -> {label} ({score})")