import requests
import json
import csv
import base64
import time


def fetch_github_file(owner, repo, path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"User-Agent": "MyCoolApp"}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 403:
            print("Достигнут лимит запросов к GitHub API (403). Ожидание")
            time.sleep(10)
            response = requests.get(url, headers=headers)

        response.raise_for_status()
        file_data = response.json()

        encoded_content = file_data["content"]

        decoded_bytes = base64.b64decode(encoded_content)
        decoded_str = decoded_bytes.decode("utf-8")

        return decoded_str
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")
        return None

OWNER = "FlyagaSEstysomNBS"
REPO = "ForStudyCsv"
FILE_PATH = "afisha.json"

print("Загрузка данных из GitHub...")
content_str = fetch_github_file(OWNER, REPO, FILE_PATH)

if content_str:
    try:
        data = json.loads(content_str)

        with open("afisha_from_github.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        with open("afisha_from_github.csv", "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["film", "price"], delimiter=";")
            writer.writeheader()
            writer.writerows(data)

        films_count = len(data)
        total_revenue = sum(item.get("price", 0) for item in data)

        print(f"Получено фильмов: {films_count}")
        print(f"Суммарная выручка: {total_revenue} Р")
        print("Сохраннено: afisha_from_github.json, afisha_from_github.csv")

    except json.JSONDecodeError:
        print("Ошибка: Файл с GitHub не является валидным JSON")