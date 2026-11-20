import pandas as pd
import numpy as np


df = pd.read_csv("coffee_dirty.csv")
missing_before = df.isnull().sum()

mean_price = df["price"].mean()
df["price"] = df["price"].fillna(mean_price)

df = df.dropna(subset=["point"])

duplicates_count = df.duplicated().sum()
df = df.drop_duplicates()

point_mapping = {
    "Неавский пр.": "Невский",
    "НЕВСКИЙ": "Невский"
}
df["point"] = df["point"].replace(point_mapping)
df["size"] = df["size"].str.upper()
df.to_csv("coffee_clean.csv", index=False, encoding="utf-8")

print(f"Пропуски до: price {missing_before["price"]}, point {missing_before["point"]}")
print(f"Дубликатов: {duplicates_count}")
print(f"Пропуски после: {df.isnull().sum().sum()}")

unique_points = sorted(df["point"].unique())
print(f"Уникальные точки: {unique_points}")