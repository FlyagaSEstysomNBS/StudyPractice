import functools
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("CardTranslator")


def log_execution(func):
    """
    Декоратор для логирования вызова функции, времени выполнения и ошибок
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Запуск функции \"{func.__name__}\"...")
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start_time
            logger.info(f"Функция \"{func.__name__}\" успешно завершена за {elapsed:.2f} секунд")
            return result
        except Exception as e:
            elapsed = time.perf_counter() - start_time
            logger.error(f"ОШИБКА. в функции \"{func.__name__}\" спустя {elapsed:.2f} секунд: {e}")
            raise
    return wrapper