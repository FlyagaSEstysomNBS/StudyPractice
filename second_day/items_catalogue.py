from functools import reduce


products = [
    {"name": "Смартфон Samsung", "price": 25000, "category": "электроника"},
    {"name": "Наушники Sony", "price": 8000, "category": "электроника"},
    {"name": "Наушники JBL", "price": 3500, "category": "электроника"},
    {"name": "Кружка", "price": 350, "category": "посуда"},
    {"name": "Чехол для телефона", "price": 900, "category": "аксессуары"},
]


expensive_products = list(filter(lambda x: x["price"] > 1000, products))
print(f"Товары дороже 1000 Рублей: {expensive_products}")


headphones = list(filter(lambda x: "наушники" in x["name"].lower(), products))
print(f"Товары только с \"Наушники\": {headphones}")


prices = list(map(lambda x: x["price"], products))
print(f"Список цен: {prices}")


total_sum = reduce(lambda acc, x: acc + x["price"], products, 0)
print(f"Сумма корзины: {total_sum}")


def apply_twice(func, x):
    return func(func(x))

def discount_10(price):
    return price * 0.9

initial_price = products[0]["price"]
final_price = apply_twice(discount_10, initial_price)
print(f"Цена смартфонов до скидки: {initial_price}")
print(f"Цена смартфонов после скидки: {final_price}")