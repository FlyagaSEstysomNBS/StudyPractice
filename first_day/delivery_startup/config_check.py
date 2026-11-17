import os
import sys


try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("ОШИБКА. Библиотека \"python-dotenv\" не установлена")
    print("Выполните в терминале: \"pip install python-dotenv\"")
    sys.exit(1)


REQUIRED_KEYS = [
    "PAYMENT_API_KEY",
    "DELIVERY_API_URL",
    "MAPS_API_KEY=test_map_key"
]


def check_config():
    print("Начало проверки конфигурации...\n")
    missing_keys = []
    found_keys = []

    for key in REQUIRED_KEYS:
        value = os.getenv(key)

        if value:
            if key == "PAYENT_API_KEY":
                display_value = f"({value[:4]}...)"
                print(f"{key}: задан{display_value}")
            else:
                print(f"{key}: задан")
        else:
            all_ok = False
            print(f"{key}: не задан. Проверьте .env")

    if all_ok:
        print("\nВсе ключи на месет. Можно работать")
    else:
        print("\nПредупреждение. Не все ключи настроены")


if __name__ == "__main__":
    check_config()