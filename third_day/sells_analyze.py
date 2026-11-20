import pandas as pd
import numpy as np

np.random.seed(42)
n = 500
days = pd.date_range("2026-09-01", "2026-09-30").strftime("%Y-%m-%d")
df = pd.DataFrame({
    "date": np.sort(np.random.choice(days, n)),
    "drink": np.random.choice(["капучино", "латте", "американо", "раф", "чай"], n),
    "size": np.random.choice(["S", "M", "L"], n, p=[0.3, 0.5, 0.2]),
    "price": np.random.randint(150, 450, n),
    "point": np.random.choice(["ТЦ Галерея", "Невский", "Петроградка"], n),
})
df.to_csv("coffee_sales.csv", index=False, encoding="utf-8")

print("/// Первичный осмотр ///")
print(df.head())
print()

print(df.dtypes)
print()

print("Пропуски данных")
print(df.isnull().sum())
print()

print("/// Основные метрики ///")
total_revenue = df["price"].sum()
avg_check = df["price"].mean()

most_popular_drink = df["drink"].value_counts().idxmax()
most_popular_count = df["drink"].value_counts().max()

revenue_by_drink = df.groupby("drink")["price"].sum()
most_profitable_drink = revenue_by_drink.idxmax()
most_profitable_sum = revenue_by_drink.max()

print(f"Общая выручка: {total_revenue:,.0f} Р".replace(",", " "))
print(f"Средний чек: {avg_check:.1f} Р")
print(f"Самый популярный: {most_popular_count} ({most_popular_count} чеков)")
print(f"Самый прибыльный: {most_profitable_drink} ({most_popular_count:,.0f} Р)".replace(",", " "))
print()

print("/// По точкам ///")
point_stats = df.groupby("point")["price"].agg(
    total_revenue="sum",
    checks_count="count",
    avg_check="mean"
)
point_stats = point_stats.sort_values(by="total_revenue", ascending=False)

for point, row in point_stats.iterrows():
    rev = f"{row["total_revenue"]:,.0f}".replace(",", " ")
    cnt = f"{row["checks_count"]:,.0f}"
    avg = f"{row["avg_check"]:,.1f}"
    print(f"{point}: {rev} Р, {cnt} чеков, ср. {avg} Р")
print()

print("/// Доля продаж по размерам ///")
size_shares = df["size"].value_counts(normalize=True) * 100

for size, share in size_shares.items():
    print(f"Размер {size}: {share:.1f}%")