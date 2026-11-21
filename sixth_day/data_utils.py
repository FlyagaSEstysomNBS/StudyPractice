import os
import pandas as pd
from logger import logger, log_execution


@log_execution
def load_and_filter_csv(file_path: str) -> pd.DataFrame:
    """
    Загружает CSV-файл и фильтрует пустые карточки товаров
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Предупреждение. Файл не найден: {file_path}")

    try:
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    except pd.errors.EmptyDataError:
        logger.warning("Передан абсолютно пустой файл")
        return pd.DataFrame()

    if df.empty:
        return df

    required_cols = {"title", "description"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"В CSV отсутствуют обязательные колонки: {required_cols - set(df.columns)}")

    initial_count = len(df)
    df = df.dropna(subset=["title", "description"], how="all").copy()
    df["title"] = df["title"].fillna("").astype(str).str.strip()
    df["description"] = df["description"].fillna("").astype(str).str.strip()
    df = df[(df["title"] != "") | (df["description"] != "")]

    filtered_count = initial_count - len(df)
    if filtered_count > 0:
        logger.info(f"Отфильтровано пустых записей: {filtered_count}")

    return df.reset_index(drop=True)


@log_execution
def save_csv(df: pd.DataFrame, output_path: str) -> None:
    """
    Сохраняет результат перевода в CSV с кодировкой для Excel
    """
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    logger.info(f"Файл успешно сохранён: {output_path} (строк: {len(df)})")