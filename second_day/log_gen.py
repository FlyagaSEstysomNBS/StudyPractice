import random
from datetime import datetime, timedelta


def generate_test_log(filename="server.log", target_size_mb = 10):
    target_size_bytes = target_size_mb * 1024 * 1024
    levels = ["INFO", "ERROR", "WARNING", "DEBUG"]
    massages = [
        "Заказ создан",
        "Не удалось связаться с платежным шлюзом",
        "Пользователь авторизован",
        "Ошибка чтения из БД",
        "Обновлен статус заказа"
    ]

    curren_time = datetime(2026, 10, 19, 12, 0, 0)
    
    with open(filename, 'w', encoding="utf-8") as f:
        while f.tell() < target_size_bytes:
            level = random.choice(levels)
            msg = random.choice(massages)
            time_str = curren_time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{time_str} {level} {msg}\n")
            curren_time += timedelta(seconds=1)

print("Генерация файла \"server.log\"...")
generate_test_log()
print("Файл успешно создан\n")


def read_log(path, level=None):
    with open(path, 'r', encoding="utf-8") as f:
        for line in f:
            if level is None:
                yield line
            elif f"{level}" in line:
                yield line

print("Чтение и подсчет строк...")
count_info = 0
count_error = 0

for log_line in read_log("server.log"):
    if "INFO" in log_line:
        count_info += 1
    elif "ERROR" in log_line:
        count_error += 1

print(f"Количесто строк уровня INFO: {count_info}")
print(f"Количесто строк уровня ERROR: {count_error}")

error_lines = read_log("server.log", level="ERROR")
for _ in range(3):
    print(next(error_lines).strip())