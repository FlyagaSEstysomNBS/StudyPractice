import json


cinema_data = {
    "cinema": "Синема Парк",
    "halls": {
        "1": {"name": "Красный", "seats": 120, "price": 350},
        "2": {"name": "Синий", "seats": 80, "price": 450}
    },
    "discounts": {"student": 0.2, "pensioner": 0.3}
}

filename = "cinema_config.json"

with open(filename, 'w', encoding="utf-8") as f:
    json.dump(cinema_data, f, ensure_ascii=False, indent=2)
print(f"Данные сохранены в {filename}")

with open(filename, 'r', encoding="utf-8") as f:
    loaded_data = json.load(f)
print("Данные успешно прочитаны из файла\n")


def get_hall(data, hall_id):
    try:
        hall_info = data["halls"][str(hall_id)]
        return hall_info
    except KeyError:
        print(f"Ошибка. Зал с ID \"{hall_id}\" не найден")
        return None

def get_discount(data, category):
    return data["discounts"].get(category, 0.0)


for hall_id, hall_info in loaded_data["halls"].items():
    print(f"Зал {hall_id}: {hall_info['name']} (мест: {hall_info['seats']}, цена: {hall_info['price']} Р)")

for category, discount in loaded_data["discounts"].items():
    print(f"Категория \"{category}\": скидка {discount * 100}%")

print("Ищем зал 1:", get_hall(loaded_data, "1"))
print("Ищем зал 3:", get_hall(loaded_data, "3"))

print("Скидка для студента:", get_discount(loaded_data, "student"))
print("Скидка для школьника:", get_discount(loaded_data, "schoolboy"))