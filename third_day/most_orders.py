import pandas as pd

df = pd.read_csv("coffee_clean.csv")
sales_count = df.groupby(["point", "drink"]).size().reset_index(name="count")
sales_count_sorted = sales_count.sort_values(by=["point", "count"], ascending=[True, False])

top3_drinks = sales_count_sorted.groupby("point").head(3)
top3_drinks["rank"] = top3_drinks.groupby("point").cumcount() + 1
top3_drinks["ranked_drinks"] = top3_drinks["rank"].astype(str) + ", " + top3_drinks["drink"]

point_top_drinks = top3_drinks.groupby("point")["ranked_drinks"].apply(lambda x: ", ".join(x)).reset_index()

revenue_by_point = df.groupby("point")["price"].sum().reset_index(name="total_revenue")

final_res = pd.merge(point_top_drinks, revenue_by_point, on="point")
final_res = final_res.sort_values(by="total_revenue", ascending=False)
final_res = final_res.rename(columns={"ranked_drinks": "ranked_drinks"})

for index, row in final_res.iterrows():
    revenue_str = f"{row["total_revenue"]:,.0f}".replace(",", " ")
    print(f"{row["point"]} ({revenue_str} Р): {row["ranked_drinks"]}")