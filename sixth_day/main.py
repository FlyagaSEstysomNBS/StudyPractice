import argparse
import sys
import time
from openai import AuthenticationError
from data_utils import load_and_filter_csv, save_csv
from ai_client import TranslatorClient
from logger import logger, log_execution


@log_execution
def process_catalog(input_path: str, output_path: str, target_lang: str, delay: float) -> None:
    df = load_and_filter_csv(input_path)

    if df.empty:
        print("Нет данных")
        logger.warning("Обработка остановлена: файл не содержит данных для перевода")
        return

    try:
        translator = TranslatorClient()
    except ValueError as e:
        print(f"Ошибка конфигурации: {e}")
        sys.exit(1)

    translated_titles = []
    translated_descriptions = []
    total = len(df)

    logger.info(f"Начинаем перевод {total} карточек на язык: {target_lang}")

    for idx, row in df.iterrows():
        try:
            t_title, t_desc = translator.translate_card(
                title=row["title"],
                description=row["description"],
                target_lang=target_lang
            )
            translated_titles.append(t_title)
            translated_descriptions.append(t_desc)
            logger.info(f"[{idx + 1}/{total}] Переведено: {row['title'][:40]}...")

        except AuthenticationError:
            print("Ошибка: неверный API-ключ. Проверьте переменную OLLAMA_API_KEY в файле .env")
            sys.exit(1)
        except Exception as e:
            logger.error(f"[{idx + 1}/{total}] Не удалось перевести карточку после 3 попыток: {e}")
            translated_titles.append("[ОШИБКА ПЕРЕВОДА]")
            translated_descriptions.append("[ОШИБКА ПЕРЕВОДА]")

        if idx < total - 1 and delay > 0:
            time.sleep(delay)

    df[f"title_{target_lang.lower()}"] = translated_titles
    df[f"description_{target_lang.lower()}"] = translated_descriptions

    save_csv(df, output_path)
    print(f"Готово! Обработано карточек: {total}. Результат в {output_path}")


def main():
    parser = argparse.ArgumentParser(description="AI-переводчик карточек товаров из CSV")
    parser.add_argument("--input", "-i", default="input.csv", help="Путь к входному CSV-файлу")
    parser.add_argument("--output", "-o", default="output.csv", help="Путь к выходному CSV-файлу")
    parser.add_argument("--lang", "-l", default="English", help="Язык перевода (по умолчанию: English)")
    parser.add_argument("--delay", "-d", type=float, default=0.5, help="Пауза между запросами в секунд")

    args = parser.parse_args()
    process_catalog(args.input, args.output, args.lang, args.delay)


if __name__ == "__main__":
    main()