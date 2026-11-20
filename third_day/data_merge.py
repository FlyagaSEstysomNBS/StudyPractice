import pandas as pd


staff = pd.DataFrame({
    "point": ["Невский", "Невский", "ТЦ Галерея", "Петроградка"],
    "name": ["Анна", "Петр", "Мария", "Олег"],
    "role": ["бариста", "бариста", "управляющий", "бариста"]
})

print(staff)
print()

df = pd.read_csv("coffee_clean.csv")
merged_df = pd.merge(df, staff, on="point", how="left")

print(merged_df.head())
print()

revenue_by_point = df.groupby("point")["price"].sum().reset_index()
revenue_by_point.rename(columns={"price": "total_revenue"}, inplace=True)

staff_count = staff.groupby("point").size().reset_index(name="staff_count")

point_stats = pd.merge(revenue_by_point, staff_count, on="point")

point_stats["revenue_per_employee"] = point_stats["total_revenue"] / point_stats["staff_count"]

print(point_stats)
print()

new_sales = pd.DataFrame({
    "date": ["2026.10.01", "2026.10.02"],
    "drink": ["латте", "капучино"],
    "size": ["M", "L"],
    "price": [300, 350],
    "point": ["Невский", "Петроградка"]
})

all_sales = pd.concat([df, new_sales], ignore_index=True)

print(f"Было строк: {len(df)}")
print(f"Было строк: {len(all_sales)}")
print(all_sales.tail(3))