import csv


filename = "afisha.csv"

seances = [
    {"film": "Дюна", "time": "12:30", "hall": "Красный", "price": 350},
    {"film": "Дюна", "time": "15:30", "hall": "Синий", "price": 450},
    {"film": "Оппенгеймер", "time": "18:00", "hall": "Красный", "price": 350},
    {"film": "Оппенгеймер", "time": "21:00", "hall": "Синий", "price": 450},
    {"film": "Драйв", "time": "14:00", "hall": "Красный", "price": 350}
]


with open(filename, 'w', encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["film", "time", "hall", "price"])

    for seance in seances:
        row = [seance["film"], seance["time"], seance["hall"], seance["price"]]
        writer.writerow(row)

print(f"Афиша сохранена в {filename}")

with open(filename, 'r', encoding="utf-8-sig") as f:
    reader = csv.reader(f, delimiter=";")
    header = next(reader)

    print(f"Колонки: {header}")
    print("-" * 40)

    for row in reader:
        film, time, hall, price = row
        print(f"Фильм: {film:<15} | Время: {time} | Зал: {hall:<10} | Цена: {price} Р")