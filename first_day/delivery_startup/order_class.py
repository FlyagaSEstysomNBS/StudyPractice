class Order:
    def __init__(self, order_id, address, amount, status):
        self.order_id = order_id
        self.address = address
        self.amount = amount
        self.status = status
        self.discount_applied = 0
    
    def is_delivered(self):
        return self.status == "доставлен"

    def apply_discount(self, percent):
        if not isinstance(percent, (int, float)) or percent < 0 or percent > 100:
            raise ValueError("Скидка должна быть числом в области от 0 до 100")
        
        self.amount = self.amount * (1 - percent / 100)
        self.discount_applied = percent
    
    def __str__(self):
        formatted_amount = int(self.amount) if self.amount.is_integer() else round(self.amount, 2)
        res = f"Order #{self.order_id} | {self.address} | {formatted_amount} Р | {self.status}"

        if self.discount_applied > 0:
            res += f" (скидка {self.discount_applied}%)"
        
        return res


if __name__ == "__main__":
    order1 = Order("1001", "Ул. Ленина, 5", 850, "доставлен")
    order2 = Order("1002", "Ул. Мира, 12", 1200, "в пути")
    order3 = Order("1003", "Ул. Гагарина, 3", 450, "отменен")

    order1.apply_discount(10)

    print(order1)
    print(order2)
    print(order3)

    print(f"Заказ 1 доставлен? {order1.is_delivered()}")
    print(f"Заказ 2 доставлен? {order2.is_delivered()}")