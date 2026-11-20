import pandas as pd
import matplotlib.pyplot as plt


plt.style.use('ggplot')
df = pd.read_csv("coffee_clean.csv")

revenue_by_point = df.groupby("point")["price"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))

revenue_by_point.plot(kind="bar", color="skyblue", edgecolor="black")

plt.title("Общая выручка по точкам продаж")
plt.xlabel("Точка продаж")
plt.ylabel("Выручка (Руб)")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("sales_by_point.png", dpi=300)
plt.close()


df["date"] = pd.to_datetime(df["date"])
daily_revenue = df.groupby(df["date"].dt.date)["price"].sum()

plt.figure(figsize=(10, 5))

daily_revenue.plot(kind="line", color="green", marker="o", linewidth=2)

plt.title("Динамика выручки по дням")
plt.xlabel("Дата")
plt.ylabel("Выручка (Руб)")
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("sales_by_day.png", dpi=300)
plt.close()


drink_counts = df["drink"].value_counts()

plt.figure(figsize=(7, 7))

drink_counts.plot(kind="pie", autopct="%1.1f%%", startangle=90, cmap="Pastel1")

plt.title("Доля проданных напитков")
plt.ylabel("")

plt.tight_layout()
plt.savefig("drinks_share.png", dpi=300)
plt.close()